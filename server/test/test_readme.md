# CMS API 테스트 (test_tasks.py)

`test_tasks.py`는 실행 중인 CUBRID Manager Server(CMS)의 JSON API를 실제로 호출해,
각 task가 기대한 결과(성공/실패)를 내는지 검증하는 통합 테스트다. CMS가 노출하는
HTTPS 인터페이스(`cm_port`, `/cm_api`)를 그대로 사용한다.

---

## 1. 사전 조건

- `test_tasks.conf`에 접속 대상이 적혀 있을 것. **이 파일이 없으면 테스트는
  시작되지 않고 경고를 출력한 뒤 종료한다.**
- CUBRID가 설치되어 있고 `CUBRID` / `CUBRID_DATABASES` 환경변수가 설정되어 있을 것
- CMS(`cub_manager`)가 실행 중일 것 (`cubrid manager start`)
- `python3` (표준 라이브러리만 사용, 추가 패키지 불필요)
- CM 관리자 계정 정보. 기본값은 `admin` / `admin`이며 `task_test_case/<세트>/login`에 들어 있다.

CMS는 `cm_port`에서 **HTTPS(자체 서명 인증서)** 로 서비스한다. 스크립트는 인증서를
검증하지 않도록 되어 있다(`ssl._create_unverified_context()`).

접속 대상은 `test_tasks.conf`가 정한다. 테스트 대상 CMS가 이 호스트에 있으리라는
보장이 없으므로, 주소는 로컬 설치본에서 알아내는 것이 아니라 설정으로 둔다.
`key value` / `key=value` 두 표기를 모두 인식하고 `#`부터는 주석이다.

```
cmsip 192.168.2.80    # CMS가 떠 있는 호스트
port  8001            # 그 호스트 $CUBRID/conf/cm.conf의 cm_port
```

---

## 2. 실행 방법

```sh
cd server/test

# 기본 테스트 세트(task_status_check) 실행
./run_tests.sh

# 다른 세트 실행
./run_tests.sh task_result_check.txt

# 결과 파일 비교 모드 (.answer 대조). 버전을 생략하면 11.4
./run_tests.sh -fc task_result_check.txt
./run_tests.sh -fc 11.4 task_result_check.txt

# 기준값(.answer) 재생성 -- 이 옵션 없이는 생성되지 않는다
./run_tests.sh -a 11.4 task_result_check.txt

# task_test_case/ 의 모든 세트를 차례로 실행
./run_tests.sh --all

# 단건 응답을 실제 토큰으로 덤프 (문서 검증/작성용)
./run_tests.sh --dump getbrokersinfo checkfile

# 리포트와 .result 파일 정리
./run_tests.sh --clean
```

`run_tests.sh`는 인자를 그대로 `test_tasks.py`에 넘긴다. 러너를 직접 불러도 된다.

```sh
python3 test_tasks.py                          # task_status_check
python3 test_tasks.py task_result_check.txt
python3 test_tasks.py task_result_check.txt -fc
python3 test_tasks.py task_result_check.txt -fc 11.5
python3 test_tasks.py task_result_check.txt -a 11.4
```

`-fc`와 `-a`는 함께 쓸 수 없다. 하나는 기준값과 대조하고 하나는 기준값을 갈아치우므로,
같이 주면 오류로 끝난다.

JUnit XML은 항상 세트 이름으로 생성된다(`TEST_XML` 환경변수는 없어졌다).
`task_status_check.txt`를 돌리면 `log/task_status_check.xml`과
`log/task_status_check_detail.xml`이 나온다.

종료 코드: 하나라도 기대와 다르면 **1**, 전부 통과하면 **0** 이다.

출력은 task별로 색상 표시된다. 초록 = 기대대로, 빨강 = 기대와 다름
(`expected <A>, got <B>`).

---

## 3. 디렉터리 / 파일 구조

테스트는 **세트(test set)** 단위다. 세트 하나는 *목록 파일* 과 그 목록이 가리키는
*케이스 디렉터리* 로 이루어지고, 리포트도 세트 이름을 따른다.

```
server/test/
  run_tests.sh                        실행 스크립트 (옛 Makefile 대체)
  test_tasks.py                       러너 본체
  task_test_case/
    task_status_check.txt             세트 1: 목록 (status 필드로 판정)
    task_status_check/<case>          그 세트의 요청 JSON (확장자 없음)
    task_result_check.txt             세트 2: 목록 (.answer 대조로 판정)
    task_result_check/<case>          요청 JSON (버전 무관, 공통)
    task_result_check/11_4/           CUBRID 버전별 기준값 디렉터리
      <case>.answer                     기준 응답 (커밋 대상)
      <case>.result                     -fc 실행 결과 (git 미추적)
    task_result_check/11_5/  11_2/  11_0/  10_2/
  task_test_config/                   설정/픽스처 (`tmp_file_for_test/` 등)
  task_test_sql/                      로드용 SQL (`import.sql`)
  log/                                리포트 출력 (git 미추적)
    task_status_check.xml
    task_status_check_detail.xml
```

케이스 파일에 **확장자를 붙이지 않는다.** `<case>` / `<case>.answer` / `<case>.result`가
한 묶음으로 나란히 놓이도록 하기 위한 것이다.

목록 파일 이름이 곧 케이스 디렉터리 이름이다. 새 세트를 만들려면 목록 파일
`task_test_case/<이름>.txt`와 같은 이름의 디렉터리 `task_test_case/<이름>/`을 두면 된다.
러너에는 목록 파일 이름만 넘긴다.

---

## 4. 동작 방식

### 4.1 실행 흐름

1. **접속 정보 로드** — `load_config()`가 `test_tasks.conf`에서 `cmsip`과 `port`를
   읽는다. 파일이 없거나, 두 키 중 하나가 빠졌거나, `port`가 숫자가 아니거나,
   해석할 수 없는 줄이 있으면 **요청을 보내기 전에** 경고를 출력하고 종료한다.
   기본 호스트로 폴백하지 않는 것은, 그럴 경우 아무것도 검증하지 못하거나 더
   나쁘게는 남의 서버를 상대로 테스트를 돌리게 되기 때문이다.
2. **이전 실행 잔재 정리** — `reset_leftovers()` (전체 실행에서만)
   - `sweep_stale_helpers()`로 남아 있는 보조 프로세스 회수
   - `reset_test_dbs()`로 테스트가 만든 DB 디렉터리 · `databases.txt` 항목 ·
     살아남은 `cub_server <db>` 프로세스 정리
   - 마지막의 `clean_env()`와 같은 일을 **시작 시점에 먼저** 한 번 더 한다.
     `SIGKILL`로 죽은 실행은 `finally`에 도달하지 못해 잔재를 남기는데, 그것이
     다음 실행까지 번지지 않게 하려는 것이다.
   - **`restart_services()`보다 먼저** 도는 것이 중요하다. 남아 있는
     `cub_server <db>`는 `cubrid service stop` **전에** 죽어야 한다. 그러지 않으면
     곧 삭제될 볼륨을 붙든 채로 서비스가 다시 올라온다.
   - 이 시점에는 서버가 없어 `getenv`를 쓸 수 없으므로 경로를 환경변수에서 얻는다.
     `build_env()`가 `getenv`가 알려준 경로로 `reset_test_dbs()`를 한 번 더 부르는
     이유가 이것이다(둘이 다를 수 있다).
3. **서비스 재시작** — `restart_services()` (전체 실행에서만, `--dump`는 건너뜀)
   - `cubrid service stop` → `mon_data/*` 삭제 → `cubrid service start`
     → `cubrid server start demodb` → `cm_port` 응답 대기
   - 중단된 이전 실행이 남긴 클라이언트/서버/모니터링 메타 불일치를 한 번에 털어낸다.
     모니터링 파일은 정지 상태에서만 안전하게 지울 수 있고, 재기동 시 CMS가 다시 만든다.
4. **세션 준비** — `init_env()`
   - 그 세트의 `login` 케이스로 로그인 → **실제 토큰** 획득
     (실패 시 비밀번호를 대화식으로 입력받아 재시도)
   - `getenv`로 `CUBRID` / `CUBRID_DATABASES` 실제 경로를 받아 치환에 사용
5. **환경 구성** — `build_env()`
   - `reset_test_dbs()` 재실행 (2번 참고: 이번에는 `getenv`가 알려준 경로로)
   - `copydb_advance`가 복사할 `destinationdb1` 디렉터리 생성
   - `getcaslogtopresult` / `removecasrunnertmpfile`가 읽을 픽스처를 `$CUBRID/tmp`로 복사
   - `removelog`용 일회용 파일과 `runscript`용 스크립트(`$CUBRID/tmp/test_runscript.sh`) 생성
   - `make_loaddb_input()`이 `loaddb`가 소비할 일회용 덤프를 만든다
     (`loaddb`는 `delete_orignal_files:"y"`라 입력을 지운다. 예전에는 demodb의 원본
     덤프를 가리켜서 직전 실행의 `unloaddb` 결과에 의존했다)
   - **`null` 응답을 피하기 위한 사전 데이터**를 만든다 (4.7 참고):
     `analyzecaslog`용 CAS 로그 픽스처와 `getfolderswithkeyword`가 찾을 디렉터리
   - 중단된 실행이 남긴 dbmt 사용자 `yifan`을 best-effort로 제거
   - `wait_for_mon_data()`가 첫 모니터링 수집이 끝날 때까지 대기
     (그 전에는 `vol_mon`이 없어 `set_mon_interval`이 실패한다)
   - `start_kill_targets()`가 `killprocess` / `killtransaction`의 대상을 만들고
     실제 id를 플레이스홀더에 채운다 (4.3 참고)
6. **본 실행** — `do_all_jobs()`가 세트의 목록 파일을 순서대로 처리
7. **정리** — `clean_env()`가 보조 프로세스를 종료하고 임시 DB를 정리
   (`finally` + `atexit` + `SIGTERM`/`SIGHUP` 핸들러로 비정상 종료에서도 실행)
8. **리포트** — JUnit XML 기록, 실패 수만큼 종료 코드 반영
   - 세트 이름으로 **두 개**가 나온다. `log/<세트>.xml`은 통과/실패만 담은 간단한
     리포트(CI용), `log/<세트>_detail.xml`은 각 `<testcase>`에 **서버 응답 원문**을
     `<system-out>`으로 담는다.
   - 응답은 재직렬화하지 않고 **서버가 보낸 그대로** 저장한다. `docs/api/*.md`의
     Response Sample이 서버의 출력 형식을 그대로 인용하고 있어서, 다시 찍으면
     비교가 안 되기 때문이다.

> 실행이 `kill -9`로 죽으면 `clean_env()`가 돌지 못한다. 이때 csql 세션은 파이프가 닫혀
> 스스로 종료하므로 트랜잭션은 남지 않지만, 더미 `sleep`은 남는다. `start_kill_targets()`가
> `log/helper_pids`에 pid와 커맨드라인을 적어 두고, 다음 실행의 `reset_leftovers()`가
> 커맨드라인이 일치하는 경우에만 회수한다. 정리가 시작과 끝 양쪽에 있는 이유가 이것이다.

### 4.2 토큰 처리 (중요)

러너가 매 요청 직전에 **로그인으로 얻은 실제 토큰을 채워 넣는다**(`send_one`과
`dump_one`의 `req["token"] = token`). 따라서 케이스 파일의 토큰 값은 전송되지 않으며,
`"token": ""`로 비워 둔다. 과거에는 실행할 때마다 달라지는 만료된 토큰 문자열이
파일마다 하드코딩돼 있었는데(30가지), 아무 의미가 없어 전부 빈 문자열로 정리했다.
새 케이스를 만들 때도 `"token": ""`로 두면 된다(키를 생략해도 동작한다).

### 4.3 요청 파일 포맷

`task_test_case/<세트>/<name>`은 하나의 JSON 객체(또는 객체 배열)다. 확장자는 없다.

```json
{
  "task": "getbrokerstatus",
  "token": "",
  "bname": "query_editor"
}
```

객체 **배열**이면 배열의 각 요청을 순서대로 보낸다(다단계 시나리오).

다음 플레이스홀더는 전송 전에 치환된다(`replace_env_vars`):

| 플레이스홀더 | 치환 값 |
| --- | --- |
| `$CUBRID` | `getenv`가 반환한 CUBRID 설치 경로 |
| `$CUBRID_DATABASES` | `getenv`가 반환한 databases 경로 |
| `$AUTO_DATE` | 다음 1분의 날짜 `YYYY-MM-DD` |
| `$AUTO_TIME` | 다음 1분의 시각 `HHMM` |
| `$AUTO_QUERY_TIME` | 다음 1분 `YYYY/MM/DD HH:MM` |
| `$TEST_KILL_PID` | `build_env()`가 띄운 더미 프로세스의 pid (`killprocess`용) |
| `$TEST_TRANINDEX` | `build_env()`가 demodb에 열어 둔 트랜잭션의 인덱스 (`killtransaction`용) |

`$AUTO_*`는 예약 작업(backup/exec query 등)을 “곧 실행되도록” 만들기 위한 것이다.
`$TEST_*`는 고정 id(pid `99999`, tranindex `2(+)`)로는 어느 호스트에서도 통과할 수 없던
두 케이스를 결정적으로 만들기 위한 것이다.

### 4.4 시나리오 파일: `task_test_case/<세트>.txt`

한 줄에 케이스 하나. 문법:

```
<name>              # 결과 비교 대상. -fc 에서 <name>.answer 와 대조한다
<name>,success      # status 만 검사 (success 기대). 기준값을 갖지 않는다
<name>,failure      # status 만 검사 (failure 기대). 부정 테스트
                    # 빈 줄은 무시 (가독성용 구분)
// ...              # '/'로 시작하면 주석/구분 헤더 (실행 안 함)
```

**`,<status>`가 붙으면 그 케이스는 status 검사 전용이다.** `-a`로도 기준값을 만들지 않고,
`-fc`에서도 선언한 status로만 판정한다. 쓰는 경우는 두 가지다.

- **부정 테스트** — `userverify_fail,failure` 처럼 서버가 거부해야 하는 케이스
- **기준값을 가질 수 없는 케이스** — 응답이 실행과 함께 자라는 것들 (4.5 참고)

- `<name>`은 그 세트의 케이스 디렉터리에 있는 파일명과 일치해야 한다
  (`task_test_case/<세트>/<name>`, 확장자 없음).
- 실행 **순서에 의미가 있다**. 예: `createdb` → `startdb` → … → `deletedb`.
  상태를 만드는 케이스가 그것을 쓰는 케이스보다 먼저 와야 한다.
- 두 세트(`task_status_check`, `task_result_check`)는 같은 목록으로 시작한다.
  판정 방식만 다르다(4.5 참고).

### 4.5 판정 방식 — status 검사와 결과 파일 검사

판정 방식이 두 가지 있고, `-fc` / `--file-check` 옵션으로 고른다.

**(1) status 검사 (기본)**

각 요청의 응답에서 `status`를 읽어 기대값과 비교한다.
- 목록에 `,<status>`가 없으면 `success`를 기대
- `,failure`가 붙은 줄은 `failure`를 기대 (필수 파라미터 누락, 잘못된 값 등 검증)

응답이 JSON이 아니면 그 자체를 실패로 기록한다.

기본 실행은 **파일을 아무것도 쓰지 않는다.** 기준값 생성은 `-a` / `--answer`를 줘야
일어난다. 오늘의 응답을 내일의 기준값으로 삼는 일은 명시적으로 요청해야 한다는 원칙이다.

**(2) 결과 파일 검사 (`-fc`, `--file-check`)**

각 케이스의 응답을 `<case>.result`로 쓰고, 앞서 만들어 둔 `<case>.answer`와 비교한다.
- 내용이 같으면 **success**
- 다르면 **failed** (첫 번째로 달라진 줄을 함께 출력한다)
- `.answer`가 없으면 **failed**. 비교 대상으로 올려놨는데 기준값이 없는 것은 메워야 할
  구멍이므로 조용히 넘기지 않는다. `-a`로 만들면 된다

이 모드에서는 `status` 값이 아니라 **비교 결과가 판정**이다. 따라서 `status`는 그대로인데
응답 내용이 바뀌는 회귀를 잡을 수 있고, 반대로 부정 케이스가 같은 이유로 계속 거부되는
것도 통과로 본다.

**status 전용 케이스** — 목록에 `,<status>`가 붙은 줄은 이 모드에서도 비교하지 않고
(1)의 status 판정을 그대로 쓴다. 출력에 `(status only)`가 붙고, 마지막에 그 건수를
따로 알려준다. 비교할지 status로 볼지는 **`.answer` 파일의 유무가 아니라 목록의 선언**이
결정한다.

**기준값 생성 (`-a`, `--answer`)**

```sh
./run_tests.sh -a 11.4 task_result_check.txt
```

`,<status>`가 없는 케이스만 `<case>.answer`를 새로 쓴다. status 전용 케이스는 건너뛴다.
`-fc`와 동시에 줄 수 없다.

**버전별 기준값**

같은 요청이라도 엔진 버전이 다르면 응답이 다르다. 그래서 기준값은 **CUBRID 버전 디렉터리**
안에 둔다.

```
task_test_case/task_result_check/11_4/<case>.answer
task_test_case/task_result_check/11_4/<case>.result
```

버전은 `-a` / `-fc`에 **맨 인자**로 준다. `11.4`와 `11_4` 둘 다 인식하고, 생략하면
`DEFAULT_VERSION`(현재 `11_4`)을 쓴다. 목록 파일은 `.txt`로 끝나고 버전은 `숫자_숫자`
꼴이라 순서에 상관없이 구분된다. 모르는 버전은 거부한다.

```sh
./run_tests.sh -a  11.4 task_result_check.txt   # 11_4/ 에 기준값 생성
./run_tests.sh -fc 11.5 task_result_check.txt   # 11_5/ 기준값과 대조
```

디렉터리는 `KNOWN_VERSIONS`(`10_2`, `11_0`, `11_2`, `11_4`, `11_5`)에 선언되어 있다.
새 버전을 추가하려면 여기에 넣고 그 버전 엔진에서 `-a`를 한 번 돌리면 된다.

버전을 나눈 이유가 되는 실제 사례가 있다. `dbmtuserlogin`은 11.4에서는 성공하지만
11.5에서는 실패한다. CMS가 던지는 고정 SQL이 `db_user.groups`의 원소를 객체로 보고
`SET{t.g.name}`을 쓰는데, 11.5에서는 그 원소가 이름(varchar)이라 타입 오류가 난다
(`cm_job_task.cpp:10173`). 하나의 기준값으로는 두 버전을 함께 담을 수 없다.

배열 케이스(요청 여러 건)는 응답을 순서대로 이어 붙여 한 파일에 담는다.
케이스 하나가 결과 파일 하나에 대응한다.

**정규화** — 실행마다 달라지는 값은 비교 전에 걸러낸다. 그대로 비교하면 서버 동작이
같아도 매번 실패한다.

| 대상 | 처리 |
| --- | --- |
| `__EXEC_TIME` | 응답에서 제거 |
| CUBRID 설치 경로 | `$CUBRID`로 환원 |
| databases 경로 | `$CUBRID_DATABASES`로 환원 |
| 호스트 이름 | `$HOSTNAME`으로 환원 |
| `VOLATILE_KEYS`의 키 | 값을 `<volatile>`로 치환 |
| `VOLATILE_PATTERNS`에 걸리는 문자열 | `<timestamp>` / `<date>` / `_<tmpid>`로 치환 |

`VOLATILE_KEYS`는 **키 이름**으로 가린다. 값 전체가 실행마다 바뀌는 것들이다:
`pid`, `as_pid`, `as_psize`, `as_lat`, `time`, `tran_time`, `tranindex`,
`cpu_*`, `mem_*`, `free_size`, `freespace`, `size`, `total`, `token`.

`VOLATILE_PATTERNS`는 **모양**으로 가린다. 긴 문자열 안에 박혀 있어서 키 단위로는
못 거르는 것들이다.

| 예 | 나오는 곳 |
| --- | --- |
| `Fri Aug 21 08:11:54 2026` | `backupvolinfo`의 백업 볼륨 헤더 |
| `demodb_20260821_0813.err` | `paramdump`의 `error_log` |
| `2026/08/21 08:12:27`, `2026.08.21.08.12` | `getbrokerdiagdata`, `backupdbinfo` |
| `2026.08.21` | 로그 목록의 `lastupdate` |
| `log_run_res_142_1787267549_943250_982` | `executecasrunner`, `analyzecaslog`의 임시 파일 |

새 케이스를 넣고 `-fc`가 계속 실패하면, 출력된 "첫 번째로 달라진 줄"을 보고 키를
`VOLATILE_KEYS`에 넣거나 모양을 `VOLATILE_PATTERNS`에 추가한다.

**같은 케이스가 목록에 두 번 나오는 경우** — `startinfo`처럼 시나리오의 앞뒤에서 두 번
실행되면 응답이 서로 다르다. 두 번째부터는 `<case>.2.answer` / `<case>.2.result`로
따로 기준값을 갖는다.

**기준값을 가질 수 없는 케이스** — 아무리 마스킹해도 두 실행이 같아지지 않는 것들이다.
응답이 실행 자체와 함께 자란다. 목록에서 `,success`를 붙여 status 전용으로 선언한다.

| 케이스 | 이유 |
| --- | --- |
| `loadaccesslog,success` | 이 테스트가 계속 append 하는 매니저 access 로그를 그대로 돌려준다 |
| `getloginfo,success` | 실행마다 새로 생기는 서버 error 로그 파일이 목록에 추가된다 |
| `get_mon_statistic,success` | 그때까지 수집된 모니터링 샘플 개수만큼 돌려준다 |
| `getautoexecqueryerrlog,success` | auto exec query 에러 로그가 영구 누적된다. 게다가 요청이 아니라 **스케줄러**가 append 하므로(목록의 `setautoexecquery`가 다음 1분에 실행될 질의를 등록한다) 기준값을 쓴 실행과 검사하는 실행 사이에 잡이 발동했는지가 타이밍 문제다. 매번이 아니라 **간헐적**으로 틀어졌다 |
| `getautoexecqueryerrlog_optional,success` | 위와 같은 로그를 읽는다 |

정규화로 해결되는 것과 그렇지 않은 것의 차이는, 달라지는 부분이 **값 하나인지 구조인지**다.
값 하나면 `VOLATILE_KEYS` / `VOLATILE_PATTERNS`로 가릴 수 있고, 배열의 길이나 항목 수가
달라지면 가릴 방법이 없다.

### 4.6 `--dump` 모드

```sh
python3 test_tasks.py --dump <name> [<name> ...]
```

로그인해 **실제 토큰**으로 각 케이스를 1회 실행하고, 원본 JSON 응답을 그대로 출력한다.
전체 목록은 실행하지 않는다. 실제 응답값을 확인하거나 `docs/api/*.md` 문서를 검증·갱신할 때 쓴다.

### 4.7 `null` 응답을 만들지 않기 위한 사전 데이터

응답에 목록이 비어 있으면 서버는 `[]`가 아니라 **`null`**을 돌려준다
(`nv_to_json`, `cm_server_interface.cpp:359` — 빈 섹션은 기본값 `Json::Value`로 대입된다).
`status`만 보는 판정에서는 통과하지만, 정작 그 목록을 만드는 코드는 한 줄도 실행되지
않는다. 그래서 아래 항목은 `build_env()`가 미리 데이터를 만들어 둔다.

| 케이스 | `null`이던 필드 | 사전 작업 |
| --- | --- | --- |
| `analyzecaslog`, `analyzecaslog_option_no` | `resultlist` | 질의 2건이 담긴 CAS 로그 픽스처(`task_test_config/test_analyzecaslog.sql.log`)를 `$CUBRID/tmp`로 복사하고 케이스가 그것을 분석하게 한다 |
| `killtransaction` | `transactioninfo` | demodb에 트랜잭션을 **두 개** 연다. 하나를 죽이고 남은 하나가 목록에 잡힌다 |
| `getfolderswithkeyword` | `folders` | `$CUBRID/tmp/test_result_folder`를 만들고 케이스의 패턴을 `*result*`로 둔다 |
| `adddbmtuser`, `setdbmtpasswd` | `dbauth` | `adddbmtuser` 케이스에 `dbauth`(demodb) 항목을 넣어 CM 사용자에게 DB 권한을 준다 |

주의할 점 두 가지.

- `analyzecaslog`를 살아 있는 CAS 로그로 겨누면 안 된다. 이 목록에는 브로커를 거쳐 SQL을
  보내는 케이스가 없어서 CAS 로그에 질의 기록이 남지 않고, `broker_log_top`이 빈 리포트를
  써서 다시 `null`이 된다. 픽스처를 쓰는 이유가 이것이다.
- `getfolderswithkeyword`의 `keyword`는 부분 문자열이 아니라 **glob 패턴**이다
  (`fnmatch`). `res`는 `res`라는 이름의 디렉터리만 찾는다.

남아 있는 `null` 두 가지는 데이터 성격상 정상이라 그대로 둔다.

- `userinfo`의 DBA `authorization`/`groups`와 PUBLIC `groups` — DBA는 권한을 암묵적으로
  가지므로 `db_auth`에 행이 없다. 같은 응답의 `INFORMATION_SCHEMA` 항목이 두 필드의
  비어 있지 않은 경우를 이미 보여준다.
- `adddbmtuser` 응답의 **첫 번째** `userlist` — 이 task는 사용자 목록을 두 번 담는데,
  앞쪽이 `dbauth`가 채워지기 전 상태다. 뒤쪽은 채워져 있다.

---

## 5. API를 추가하거나 변경할 때

새 CMS task를 추가/변경했다면 아래를 갱신한다.

### 5.1 새 API 추가

1. **요청 케이스 작성** — `task_test_case/<세트>/<task>` (확장자 없음)
   ```json
   {
     "task": "<task>",
     "token": "",
     "...": "필요한 파라미터. 경로는 $CUBRID / $CUBRID_DATABASES 사용"
   }
   ```
2. **시나리오 등록** — 그 세트의 목록 파일 알맞은 위치에 한 줄 추가
   - 성공 기대: `<task>`
   - 부정 케이스도 있으면 별도 파일(`<task>_nullxxx.txt`)을 만들고 `<task>_nullxxx,failure` 추가
   - **선후 관계 주의**: 선행 상태(예: DB 생성)가 필요하면 그 뒤에 배치하고,
     스스로 만든 자원은 뒤에서 정리하는 케이스도 함께 넣는다.
3. **검증** — `./run_tests.sh --dump <task>` 로 실제 응답 확인 후,
   `./run_tests.sh`로 목록 전체가 여전히 통과하는지 확인.
   `task_result_check`에도 넣었다면 `-a <버전>`으로 그 버전의 `.answer`를 만든다.

### 5.2 optional 파라미터 커버리지 (`_optional` 케이스)

기본 케이스는 필수 파라미터만 보내는 경우가 많다. 문서(`docs/api/<task>.md`)의
Request 표에는 있는데 케이스가 보내지 않는 선택 파라미터가 있으면,
**기존 케이스 이름 뒤에 `_optional`을 붙인 케이스**를 따로 만들어 그 값들을 모두 채운다.
기존 케이스는 그대로 둔다 — 필수 파라미터만으로도 동작하는지가 별도의 검증이기 때문이다.

```
task_test_case/task_status_check/unloaddb           # 기본
task_test_case/task_status_check/unloaddb_optional  # as-dba 등 선택 파라미터까지
```

목록 파일에는 기본 케이스 바로 다음 줄에 등록한다.

상태를 만드는 task는 자기 DB를 따로 쓴다. `createdb_optional` / `loaddb_optional`은
`optionaldb`를 만들어 쓰고 `deletedb_for_optional`로 지운다. 새 DB 이름은
`TEST_DBS`에 추가해야 중단된 실행의 잔재가 다음 실행에서 정리된다.

적용할 수 없는 값은 이 목록의 다른 케이스처럼 `"none"`으로 채워 키 자체는 보낸다
(예: `loaddb_optional`의 `trigger`, `schema-file-list` — demodb 덤프에는 해당 파일이 없다).

### 5.3 새 테스트 세트 추가

1. 목록 파일 `task_test_case/<이름>.txt` 생성
2. 같은 이름의 케이스 디렉터리 `task_test_case/<이름>/` 생성, 요청 JSON을 확장자 없이 배치
3. 실행: `./run_tests.sh <이름>.txt`
4. 리포트는 `log/<이름>.xml`, `log/<이름>_detail.xml`로 나온다

기준값을 쓰고 싶으면 `-a`로 만든다. 세트 이름과는 무관하다(4.5 참고).

### 5.4 기존 API 변경

- **요청 파라미터 변경**: 해당 `task_test_case/<세트>/<task>` 수정.
- **성공/실패 조건 변경**: 목록 파일의 기대값(`,failure` 유무) 조정.
- **응답 구조 변경**: 러너는 `status`만 보므로 통과 여부엔 영향이 없지만,
  `docs/api/<task>.md`의 Response 규격/샘플을 실제 응답에 맞춰 갱신한다.

### 5.5 문서 샘플을 실제 응답과 맞추기

`./run_tests.sh` 한 번이면 `log/<세트>_detail.xml`에 모든 케이스의 **응답 원문**이 남는다.
`docs/api/<task>.md`의 Response Sample은 이 값을 기준으로 갱신한다.
(`--dump`도 쓸 수 있지만 `deletedb` / `setsysparam` 같은 파괴적 task에는 부작용이 있다.)

두 가지 규칙이 있다.

- **Request Sample과 Response Sample은 같은 요청/응답 한 쌍이어야 한다.** 서버가 요청 값을
  그대로 되돌려 주는 필드(`addvoldb`의 `dbname`, `kill_process`의 `name` 등)는 Request
  Sample 쪽 값에 맞춘다. 테스트가 쓰는 `alatestdb` 같은 이름을 그대로 옮기면 문서만 보고
  따라 할 수 없다.
- **서버가 값을 가공하는 필드는 실제 응답을 그대로 둔다.** 예: `getaddbrokerinfo`는
  `brokerconf` 요청에 `broker`로 답하고, `getcmsenv`는 `task`를 `getversion`으로 답한다.
  요청에 맞춰 고치면 오히려 틀린 문서가 된다.

### 5.6 API 제거/미지원

- 서버에서 제거된 task는 세트의 목록 파일에서 삭제하거나 `//`로 주석 처리한다.
  (미등록 task를 남기면 `Undefined request`로 항상 실패한다)

### 5.7 지켜야 할 규칙

- 목록 파일(`task_test_case/<세트>.txt`)은 **ASCII로 유지**한다. 러너가 UTF-8 로케일에서
  텍스트로 읽으므로, 비ASCII(예: 한글 주석 EUC-KR) 바이트가 섞이면 목록 파싱 단계에서
  크래시한다. 주석은 영문으로 작성한다.
- 케이스 파일에는 **확장자를 붙이지 않는다.** `.answer` / `.result`가 같은 이름 옆에
  붙기 때문이다.
- 케이스 파일의 `token`은 **빈 문자열로 둔다**. 러너가 항상 실제 토큰을 채워 넣는다.
- 새 픽스처가 필요하면 `task_test_config/`에 넣고 `build_env()`에서 배치하도록 한다.
- `.answer`는 커밋한다(기준값). `.result`는 `.gitignore`에 걸려 있다.
- 기준값은 **버전 디렉터리 안**에 있다. 다른 엔진에서 만든 것을 옮겨 쓰지 말 것.
- 기준값은 **`-a`를 줄 때만** 갱신된다. 서버 응답이 바뀐 것을 확인하고 의도적으로
  받아들일 때만 실행할 것. 그렇지 않으면 회귀를 기준값으로 굳혀 버린다.

---

## 6. 주의사항 / 한계

- 목록 파일에는 `createdb` / `deletedb` / `stopdb` 같은 **상태 변경·파괴적 작업**이
  포함된다. **테스트 전용 인스턴스**에서 실행할 것. 운영 DB에 돌리지 말 것.
- 일부 API는 환경 의존적이라 이 목록만으로는 검증되지 않을 수 있다:
  HA 미구성 시 `heartbeatlist` / `ha_*`, shard 미구성 시 `getshardinfo` 등.
- `--dump`도 대상 task에 따라 부작용이 있을 수 있다(예: `setsysparam`은 파일을 쓴다).
  읽기 전용 task에만 쓰는 것이 안전하다.
- **기준값은 엔진 버전에 묶여 있다.** `$CUBRID`가 가리키는 설치를 바꾼 뒤 `-fc`를 돌리면
  대부분의 케이스가 실패한다. 실패가 아니라 버전이 바뀐 것일 수 있으니, 먼저
  `cubrid_rel`로 버전을 확인하고 그 버전 디렉터리를 쓰고 있는지 볼 것.

---

## 7. 관련 파일

- 서버측 task 등록표: `server/src/cm_server_util.cpp`의 `task_info[]`,
  `server/src/cm_server_extend_interface.cpp`의 `ext_task_info[]`
- API 문서: `docs/api/<task>.md` (요청/응답 규격)
- 실행 스크립트: `run_tests.sh` (옛 `Makefile`은 제거됨. `lcov` 타깃도 함께 정리했다)

## 추가 할일
- 아래 목록의 할일을 할때마다 변경사항에 대해서 이 문서도 업데이트 해야 합니다.

### 2026-08-21 — 적용 완료

원문 요청과 적용 결과. 문서 본문(2, 3, 4.1, 4.3, 4.4, 4.5, 5.1~5.7, 6, 7절)은 모두
새 구조에 맞춰 갱신했다.

| 요청 | 적용 |
| --- | --- |
| Makefile을 bash shell script로 변경, 불필요한 사항 제거 | `Makefile` 삭제, `run_tests.sh` 추가. `lcov` 타깃과 `TEST_XML` 환경변수는 함께 제거 |
| 케이스 파일의 `.txt` 확장자 제거 | 208개 전부 확장자 없이 배치. 러너의 경로 조립도 `case_path()`로 통일 |
| `task_test_case_json` 폴더를 `task_test_case`로 변경 | 완료. 이름을 쓰던 옛 소켓 코퍼스는 이미 삭제된 상태였다 |
| `task_list.txt`을 `task_test_case` 안으로 이동하고 `task_status_check.txt`로 개명 | 완료 |
| 케이스 json을 `task_test_case/task_status_check/`로 이동 | 완료 |
| `test_tasks.py <목록>.txt`로 실행, 목록을 읽어 하위 폴더의 json으로 테스트 | 완료. 목록 이름이 곧 케이스 디렉터리 이름이다 (`resolve_test_set()`) |
| `task_result_check.txt` 세트를 동일하게 생성, 1차 테스트 후 `.answer` 생성 | 완료. 생성은 `-a` / `--answer` 전용으로 바꿨다 (기본 실행은 파일을 쓰지 않는다) |
| `-fc` / `--file-check`로 `.result` 생성 후 `.answer`와 비교, 다르면 failed | 완료. 비교할지 status로 볼지는 목록의 `,<status>` 선언이 결정한다 (4.5 참고) |
| log 이름을 테스트 세트 이름으로 | `log/<세트>.xml`, `log/<세트>_detail.xml` |

구현하면서 요청에 없던 판단을 세 가지 했다. 근거는 4.5에 적어 두었다.

1. **정규화** — 응답을 그대로 비교하면 213건 중 33건이 매번 실패한다. 전부 pid·경과
   시간·여유 공간·임시 파일명처럼 실행마다 바뀌는 값이었다. `VOLATILE_KEYS`(키 단위)와
   `VOLATILE_PATTERNS`(모양 단위)로 걸러낸다.
2. **기준값을 가질 수 없는 케이스 5건** — `loadaccesslog`, `getloginfo`,
   `get_mon_statistic`, `getautoexecqueryerrlog`와 그 `_optional`은 응답이 실행 자체와
   함께 자라 기준값을 가질 수 없다. 목록에서 `,success`를 붙여 status 전용으로 선언했다.
   `getautoexecqueryerrlog`는 스케줄러가 로그를 append 하는 탓에 매번이 아니라
   간헐적으로 틀어져서 늦게 드러났다.
3. **중복 등장 케이스** — `startinfo`는 목록에 두 번 나오고 두 응답이 다르다. 두 번째
   이후는 `<case>.2.answer`로 따로 기준값을 갖는다.
