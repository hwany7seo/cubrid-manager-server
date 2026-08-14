# CMS API 테스트 (test_tasks.py)

`test_tasks.py`는 실행 중인 CUBRID Manager Server(CMS)의 JSON API를 실제로 호출해,
각 task가 기대한 결과(성공/실패)를 내는지 검증하는 통합 테스트다. CMS가 노출하는
HTTPS 인터페이스(`cm_port`, `/cm_api`)를 그대로 사용한다.

---

## 1. 사전 조건

- CUBRID가 설치되어 있고 `CUBRID` / `CUBRID_DATABASES` 환경변수가 설정되어 있을 것
- CMS(`cub_manager`)가 실행 중일 것 (`cubrid manager start`)
- `python3` (표준 라이브러리만 사용, 추가 패키지 불필요)
- CM 관리자 계정 정보. 기본값은 `admin` / `admin`이며 `task_test_case_json/login.txt`에 들어 있다.

CMS는 `cm_port`에서 **HTTPS(자체 서명 인증서)** 로 서비스한다. 스크립트는 인증서를
검증하지 않도록 되어 있다(`ssl._create_unverified_context()`).

---

## 2. 실행 방법

```sh
cd server/test

# 전체 테스트 실행 (task_list.txt 순서대로)
make test
# 또는
python3 test_tasks.py

# JUnit XML 리포트까지 생성 (CI용)
make test          # log/test_cmserver.xml 생성
TEST_XML=log/result.xml python3 test_tasks.py

# 특정 목록 파일로 실행
python3 test_tasks.py my_list.txt

# 단건 응답을 실제 토큰으로 덤프 (문서 검증/작성용)
python3 test_tasks.py --dump getbrokersinfo checkfile
```

종료 코드: 하나라도 기대와 다르면 **1**, 전부 통과하면 **0** 이다.

출력은 task별로 색상 표시된다. 초록 = 기대대로, 빨강 = 기대와 다름
(`expected <A>, got <B>`).

---

## 3. 디렉터리 / 파일 구조

| 경로 | 역할 |
| --- | --- |
| `test_tasks.py` | 테스트 러너 본체 |
| `Makefile` | `make test` / `make lcov` / `make clean` |
| `task_list.txt` | **실행할 task와 기대 결과 목록** (테스트 시나리오) |
| `task_test_case_json/<name>.txt` | task별 **요청 JSON** (한 파일 = 한 케이스) |
| `task_test_config/` | 테스트가 참조하는 설정/픽스처 (`tmp_file_for_test/` 등) |
| `task_test_sql/` | 로드용 SQL (`import.sql`) |
| `task_test_case/` | (구) 라인 포맷 케이스. 현재 러너는 `task_test_case_json/`만 사용 |
| `log/` | 리포트 출력 (`make clean`으로 삭제, git 미추적) |

> 참고: `task_test_case/`는 소켓 프로토콜을 쓰던 옛 PHP 테스트(`test_tasks.php`, 삭제됨)의
> 코퍼스다. 현재 러너는 JSON 포맷인 `task_test_case_json/`만 읽는다. 두 디렉터리를
> 함께 유지하는 이유는 `task_test_case/`에만 있는 일부 부정(negative) 케이스의 참조값 때문이다.

---

## 4. 동작 방식

### 4.1 실행 흐름

1. **포트 탐색** — `findport()`가 `$CUBRID/conf/cm.conf`의 `cm_port`를 읽는다.
   (`cm_port 8001` / `cm_port=8001` 두 표기 모두 인식. 없으면 8001로 폴백)
2. **세션 준비** — `init_env()`
   - `task_test_case_json/login.txt`로 로그인 → **실제 토큰** 획득
     (실패 시 비밀번호를 대화식으로 입력받아 재시도)
   - `getenv`로 `CUBRID` / `CUBRID_DATABASES` 실제 경로를 받아 치환에 사용
3. **환경 구성** — `build_env()`
   - `copydb_advance`가 복사할 `destinationdb1` 디렉터리 생성
   - `getcaslogtopresult` / `removecasrunnertmpfile`가 읽을 픽스처를 `$CUBRID/tmp`로 복사
4. **본 실행** — `do_all_jobs()`가 `task_list.txt`를 순서대로 처리
5. **정리** — `clean_env()`가 생성한 임시 DB 디렉터리 삭제 (예외가 나도 실행)
6. **리포트** — `TEST_XML` 지정 시 JUnit XML 기록, 실패 수만큼 종료 코드 반영

### 4.2 토큰 처리 (중요)

케이스 파일(`task_test_case_json/*.txt`)에는 과거의 토큰 문자열이 하드코딩되어 있지만,
러너가 매 요청 직전에 **로그인으로 얻은 실제 토큰으로 덮어쓴다**(`send_one`의
`req["token"] = token`). 따라서 케이스 파일의 토큰 값은 그대로 두어도 되며(플레이스홀더),
실제 인증은 항상 유효 토큰으로 이뤄진다.

### 4.3 요청 파일 포맷

`task_test_case_json/<name>.txt`는 하나의 JSON 객체(또는 객체 배열)다.

```json
{
  "task": "getbrokerstatus",
  "token": "PLACEHOLDER",
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

`$AUTO_*`는 예약 작업(backup/exec query 등)을 “곧 실행되도록” 만들기 위한 것이다.

### 4.4 시나리오 파일: `task_list.txt`

한 줄에 케이스 하나. 문법:

```
<name>              # task_test_case_json/<name>.txt 를 실행, 성공을 기대
<name>,failure      # 실행 후 서버가 거부(status=failure)하기를 기대 (부정 테스트)
                    # 빈 줄은 무시 (가독성용 구분)
// ...              # '/'로 시작하면 주석/구분 헤더 (실행 안 함)
```

- `<name>`은 `task_test_case_json/<name>.txt`의 파일명(확장자 제외)과 일치해야 한다.
- 실행 **순서에 의미가 있다**. 예: `createdb` → `startdb` → … → `deletedb`.
  상태를 만드는 케이스가 그것을 쓰는 케이스보다 먼저 와야 한다.
- 현재 약 179개 항목(그중 부정 테스트 61개)을 담고 있다.

### 4.5 판정 방식

각 요청의 응답에서 `status`를 읽어 기대값과 비교한다.
- 기본 기대는 `success`
- `,failure`가 붙은 줄은 `failure`를 기대 (필수 파라미터 누락, 잘못된 값 등 검증)

응답이 JSON이 아니면 그 자체를 실패로 기록한다.

### 4.6 `--dump` 모드

```sh
python3 test_tasks.py --dump <name> [<name> ...]
```

로그인해 **실제 토큰**으로 각 케이스를 1회 실행하고, 원본 JSON 응답을 그대로 출력한다.
전체 목록은 실행하지 않는다. 실제 응답값을 확인하거나 `docs/api/*.md` 문서를 검증·갱신할 때 쓴다.

---

## 5. API를 추가하거나 변경할 때

새 CMS task를 추가/변경했다면 아래를 갱신한다.

### 5.1 새 API 추가

1. **요청 케이스 작성** — `task_test_case_json/<task>.txt`
   ```json
   {
     "task": "<task>",
     "token": "PLACEHOLDER",
     "...": "필요한 파라미터. 경로는 $CUBRID / $CUBRID_DATABASES 사용"
   }
   ```
2. **시나리오 등록** — `task_list.txt`의 알맞은 위치에 한 줄 추가
   - 성공 기대: `<task>`
   - 부정 케이스도 있으면 별도 파일(`<task>_nullxxx.txt`)을 만들고 `<task>_nullxxx,failure` 추가
   - **선후 관계 주의**: 선행 상태(예: DB 생성)가 필요하면 그 뒤에 배치하고,
     스스로 만든 자원은 뒤에서 정리하는 케이스도 함께 넣는다.
3. **검증** — `python3 test_tasks.py --dump <task>` 로 실제 응답 확인 후,
   `make test`로 목록 전체가 여전히 통과하는지 확인.

### 5.2 기존 API 변경

- **요청 파라미터 변경**: 해당 `task_test_case_json/<task>.txt` 수정.
- **성공/실패 조건 변경**: `task_list.txt`의 기대값(`,failure` 유무) 조정.
- **응답 구조 변경**: 러너는 `status`만 보므로 통과 여부엔 영향이 없지만,
  `docs/api/<task>.md`의 Response 규격/샘플을 실제 응답에 맞춰 갱신한다
  (`--dump`로 실제 값 확인).

### 5.3 API 제거/미지원

- 서버에서 제거된 task는 `task_list.txt`에서 삭제하거나 `//`로 주석 처리한다.
  (미등록 task를 남기면 `Undefined request`로 항상 실패한다)

### 5.4 지켜야 할 규칙

- `task_list.txt`는 **ASCII로 유지**한다. 러너가 UTF-8 로케일에서 텍스트로 읽으므로,
  비ASCII(예: 한글 주석 EUC-KR) 바이트가 섞이면 목록 파싱 단계에서 크래시한다.
  주석은 영문으로 작성한다.
- 케이스 파일에 **실제 토큰을 넣을 필요가 없다**. 러너가 항상 덮어쓴다.
- 새 픽스처가 필요하면 `task_test_config/`에 넣고 `build_env()`에서 배치하도록 한다.

---

## 6. 주의사항 / 한계

- `task_list.txt`에는 `createdb` / `deletedb` / `stopdb` 같은 **상태 변경·파괴적 작업**이
  포함된다. **테스트 전용 인스턴스**에서 실행할 것. 운영 DB에 돌리지 말 것.
- 일부 API는 환경 의존적이라 이 목록만으로는 검증되지 않을 수 있다:
  HA 미구성 시 `heartbeatlist` / `ha_*`, shard 미구성 시 `getshardinfo` 등.
- `--dump`도 대상 task에 따라 부작용이 있을 수 있다(예: `setsysparam`은 파일을 쓴다).
  읽기 전용 task에만 쓰는 것이 안전하다.

---

## 7. 관련 파일

- 서버측 task 등록표: `server/src/cm_server_util.cpp`의 `task_info[]`,
  `server/src/cm_server_extend_interface.cpp`의 `ext_task_info[]`
- API 문서: `docs/api/<task>.md` (요청/응답 규격)
- 커버리지: `make lcov` (lcov 필요)
