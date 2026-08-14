# test_tasks.py 실패 분석

`task_list.txt` 전체를 로컬 CUBRID 11.5 + 실행 중인 CMS(admin/admin)에서 돌린 결과를
분석한 문서다.

- 최초 실패: **43건** / 193 케이스
- 테스트 케이스 문제를 고친 뒤: **19건**
- 재확인 요청 항목(트리거 `;`, compactdb 전용 DB, renamedb advanced off)을 반영한 뒤:
  **14건 / 196 케이스** (연속 2회 실행 결과 동일 — 재현 가능)
- CMS를 현재 소스에서 새로 빌드하고(보안 강화 커밋 포함) `dbmtuserlogin` 수정을 적용한
  서버로 다시 돌린 뒤: **10건 / 196 케이스** — 남은 10건은 전부 환경 제약(5장)이다.

즉 **서버 버그 4건은 해소**되었고, 새 빌드에서 드러난 테스트 케이스 문제 3건
(`runscript`, `backupdb_rep`, `updateuser_nopasswd`)도 고쳤다 → **6장** 참고.

검증 환경(최초): `CUBRID 11.5.0 (11.5.0.2405-a2c3e03)`, non-HA, shard 미구성,
`support_mon_statistic=NO`.
검증 환경(현재): `CUBRID 11.5.0 (11.5.0.2441-6ba9522)` + 현재 소스에서 빌드한
`cub_manager`(`a2393c2` 보안 강화, `90e82a2` 포함). 나머지 조건은 동일.

---

## 1. 서버 버그 (확인됨)

테스트 케이스는 정상인데 서버/유틸리티가 실패시키는 항목. CMS 소스 수정이 필요하다.

> **현재 상태(재검증 완료)** — 실행 중인 `cub_manager`(08-14 빌드)에는 1-1 수정이 들어가
> 있다. 바이너리에 `SET{t.g.name}`과 `SET{t.g}` 두 문자열이 모두 있으므로 버전 분기가
> 추가된 것으로 보인다. 그 결과 `dbmtuserlogin` + 연쇄 3건(1-2)은 **모두 success**다.
> 단, 이 저장소의 소스(`cm_job_task.cpp:10173`)에는 아직 반영돼 있지 않다.
> 1-3(트리거 `;`)은 새 바이너리에도 **반영되지 않았다** — 포맷 문자열이
> `create trigger\t%s\n` / `drop trigger\t%s\n` 그대로여서 테스트 측 `;` 우회가 여전히
> 필요하다.

### 1-1. `dbmtuserlogin` — db_user 조회 SQL이 CUBRID 11.5와 비호환 (재확인 완료: 버그 확정)

- 증상: `t.g is a varchar type, not an object type.`
- 원인: `cmd_dbmt_user_login()`(`server/src/cm_job_task.cpp:10173`)의 검증 쿼리가
  `db_user.groups`를 **객체 집합**으로 가정해 `SET{t.g.name}`을 쓴다.

  ```sql
  -- 현재 (실패)
  ... COALESCE(SUM(SET{t.g.name}), SET{}) from db_user u, TABLE(groups) AS t(g) ...
  -- 수정안 (csql로 동작 확인)
  ... COALESCE(SUM(SET{t.g}),      SET{}) from db_user u, TABLE(groups) AS t(g) ...
  ```

#### 재확인 결과 — "실제 서버 정보를 읽어 정상 분기된다"는 지적에 대해

코드에 분기가 있는 것은 맞지만, **분기 지점이 모두 SQL 실행 이후**라서 이 오류를 막지
못한다. 분기는 두 곳이다.

1. `run_csql_statement()`(`cm_job_task.cpp:10562`) — `uDatabaseMode()`로 실제 DB 상태를
   읽어 `--SA-mode` / `--CS-mode`를 골라 붙인다. 즉 "실제 서버 정보를 읽어 분기"하는 것은
   **csql 실행 모드**뿐이고, SQL 문자열은 건드리지 않는다.
2. `dbmt_user_is_dba()`(`cm_job_task.cpp:10106`) — `dbuser`가 `DBA`면 파일을 읽지 않고
   바로 1을 반환한다. 하지만 이 호출은 `run_csql_statement()`가 `ERR_NO_ERROR`를 준
   **다음**(`cm_job_task.cpp:10204`)이라, SQL이 깨지면 도달하지 못한다.

문제의 SQL은 `const char *statement`로 **버전 분기 없이 하드코딩**돼 있다.
(`cubrid_version_major/minor`, `CUBRID_VERS()` 분기 인프라는 있으나 이 쿼리에는 적용 안 됨.)

증거 4가지:

- **csql 직접 실행**: `t.g.name` → 파싱 오류, `t.g` → `count(*) = 1` 정상.
- **11.5의 `db_user` 스키마**: `db_attribute`에서 `groups`는 `SET`이고
  `domain_class_name`이 `NULL`(= 객체 집합 아님).
- **`db_user`가 클래스가 아니라 뷰**이고, 뷰 정의 자체가 groups를 이름 집합으로 평탄화한다:

  ```sql
  -- db_vclass.vclass_def (발췌)
  (SELECT COALESCE(SUM(SET{[g].[name]}), SET{}) FROM TABLE([u].[groups]) AS [t]([g]))
      AS [groups]
  ... FROM [_db_user] AS [u]
  ```

  즉 `.name` 조회는 기반 테이블 `_db_user`에서만 유효하다. CMS 쿼리는 `db_user`가
  뷰로 바뀌기 전 스키마를 기준으로 작성된 것이다.
  (`_db_user`로 바꾸는 건 답이 아니다 — 비 DBA는 `_db_user`를 못 읽으므로 이 검사의
  목적 자체가 깨진다.)
- **설치된 바이너리도 동일**: `$CUBRID/bin/cub_manager`(11.5.0.2405) 안에 같은
  `SET{t.g.name}` 문자열이 그대로 들어 있고, 실행 중인 CMS에 요청하면 재현된다.

  ```
  $ python3 test_tasks.py --dump dbmtuserlogin
  "note": "... t.g is a varchar type, not an object type.<end>",
  "status": "failure"
  ```

- 조치: `SET{t.g}`로 수정. CMS는 엔진 10.x 이상을 지원하므로(`cm_cmd_exec.cpp:213`),
  10.x에서 `db_user`가 아직 클래스라면 `CUBRID_VERS()` 분기가 필요하다 — 이 부분만
  엔진 10.x 환경에서 추가 확인이 필요하다.
- 영향(연쇄): dbmtuserlogin이 실패하면 demodb의 DBA 접속정보가 등록되지 않아,
  demodb에 DBA 권한이 필요한 아래 케이스가 함께 실패한다 → **1-2 참고**.

### 1-2. `createuser` / `updateuser` / `deleteuser` — 1-1의 연쇄

- 증상:
  - `createuser`, `deleteuser`: `Operation "add_user"/"drop_user" can only be performed by the DBA ...`
  - `updateuser`: `User "yifan" is invalid.` (선행 createuser 실패로 yifan 미생성)
- 원인: 이 task들은 `conlist`에 저장된 demodb 접속정보(사용자/비밀번호)로 CSQL을 실행하는데,
  그 정보는 `dbmtuserlogin`이 등록한다. 1-1로 등록이 안 되면 비 DBA로 접속돼 권한 오류가 난다.
- 확인: `dbmtuserlogin`(실패) 직후 `createuser`를 직접 호출 → 동일하게 "must be DBA"로 실패.
- 조치: 1-1을 고치면 함께 해소될 것으로 판단.

### 1-3. `addtrigger` / `altertrigger` / `droptrigger` — 생성 SQL에 문장 종료자 누락

- 증상: `Syntax error: unexpected 'commit', expecting ';'`
- 원인: `op_make_triggerinput_file_add/alter/drop()`
  (`server/src/cm_job_task.cpp:13506`, `13595`, `13568`)이 만드는 DDL이 **`;` 종료자 없이**
  곧바로 `commit;`을 붙인다. `alter`는 status와 priority가 둘 다 오면 두 개의
  `alter trigger` 문을 구분자 없이 연달아 쓰기까지 한다.
- 서버 수정안: 각 생성 함수에서 문장 끝에 `;`를 출력.
- **테스트 측 우회(적용 완료)**: 요청대로 각 케이스의 **마지막으로 출력되는 값**에 `;`를
  붙였다. 생성 순서상 그 값 뒤가 곧바로 `commit;`이므로 문장이 정상 종료된다.

  | 케이스 | 수정한 필드 | 생성되는 마지막 줄 |
  | --- | --- | --- |
  | `addtrigger` | `"action":"REJECT;"` | `execute	REJECT;` |
  | `altertrigger` | `"status":"INACTIVE;"`, `"priority":"00.00;"` | `alter trigger example status INACTIVE; alter trigger example priority 00.00;` |
  | `droptrigger` | `"triggername":"example;"` | `drop trigger	example;` |

  `droptrigger`는 필드가 `triggername` 하나뿐이라 그쪽에 붙일 수밖에 없다.
  이 우회는 **서버 버그를 감추는 것이 아니라 우회**하는 것이므로, 서버가 `;`를 붙이도록
  고치면 이 `;`들을 되돌려야 한다. 의도는 `task_list.txt`에 주석으로 남겼다.
- 결과: `addtrigger` / `altertrigger` / `droptrigger` 모두 success.

---

## 2. 재확인으로 해소된 항목

### 2-1. `compactdb` — 전용 DB를 만들어 실행하도록 변경 (해소)

- 기존 증상: `status=failure`인데 `note`에 compactdb 정상 진행 로그가 담김.
- 기존 원인: `compactdb`가 `alatestdb`를 대상으로 하는데, 그 DB는 같은 목록에서
  `addvoldb` → `backupdb` → `optimizedb` → `stopdb` → `loaddb` → `restoredb`를
  모두 거친 상태였다. 즉 앞선 태스크들의 상태에 오염된 DB를 대상으로 했다.
- 확인: 새로 만든 빈 DB(정지 상태)에 유틸리티를 직접 실행하면 정상이다 —
  `cubrid compactdb --verbose --SA-mode <newdb>` → exit 0, stderr 없음.
  따라서 `ts_compactdb()`의 stdout/stderr 처리 자체는 문제가 아니었다.
- 조치(적용 완료): 요청대로 compactdb 전용 DB를 쓰도록 분리했다.

  ```
  createdb_for_compactdb   # compactdbtest 생성
  compactdb                # dbname: compactdbtest
  deletedb_for_compactdb   # compactdbtest 제거
  ```
- 결과: 3건 모두 success.

### 2-2. `renamedb` — advanced off로 테스트 (해소)

- 기존 증상: `File ".../tmp/DBMT_task_..." does not have enough entries: 3 entries expected.`
  (오류 문자열은 CMS가 아니라 `cubrid renamedb` 유틸리티가 낸다)
- 기존 원인: advanced 모드에서 `tsRenameDB()`가 `"%d %s %s\n"`(index, from, to) 형식으로
  맵 파일을 쓰는데 `cubrid renamedb -i <map>`이 기대하는 형식과 어긋난다.
  → **advanced on 경로는 여전히 미해결이며, 별도 확인이 필요하다.**
- 조치(적용 완료): 요청대로 `renamedb.txt`를 `advanced:"off"`, `exvolpath:"none"`으로
  바꾸고 `volume` 매핑을 제거했다. 실패를 기대하는 3개 케이스
  (`renamedb_nullrename`, `renamedb_adoff`, `renamedb_erropen`)는 `destinationdb`가
  아직 존재해야 하므로 **성공 케이스보다 앞으로** 옮겼다.
- 뒷정리: renamedb는 `destinationdb`를 `anotherdb`로 바꾸므로,
  `deletedb_for_renamedb`(dbname `anotherdb`)를 추가해 등록정보까지 정리한다.
  이게 없으면 다음 실행에서 `anotherdb`가 이미 존재해 실패한다.
- 결과: `renamedb` success, 실패 기대 3건도 기대대로 failure, `deletedb_for_renamedb` success.

---

## 3. 테스트 로그 개선 (적용 완료)

같은 task를 여러 케이스가 공유해서(`renamedb`, `renamedb_adoff`, `renamedb_nullrename`,
`renamedb_erropen`이 모두 task `renamedb`) 로그만 보고는 어느 케이스가 깨졌는지 알 수
없었다. `test_tasks.py`를 다음과 같이 고쳤다.

- 한 줄의 맨 앞이 **케이스(파일) 이름**, 대괄호 안이 실제 task 이름이 되도록 변경.

  ```
  renamedb_adoff [renamedb] : failure
  compactdb [compactdb] : success
  ```
- 실패한 줄 아래에 **케이스 파일 경로**를 함께 출력.

  ```
  dbmtuserlogin [dbmtuserlogin] : expected success, got failure (...)
      case file: task_test_case_json/dbmtuserlogin.txt
  ```
- 실행 끝에 실패 목록을 케이스 이름 + 파일 경로 + note로 요약 출력.
- JUnit XML의 `<testcase>`에 `file="..."` 속성 추가.

### 실행 반복 가능성

`reset_test_dbs()`를 추가해, 실행 전/후에 **테스트가 만든 DB만**
(`alatestdb`, `compactdbtest`, `destinationdb`, `anotherdb`, `copydb`, `destinationdb1`)
디렉터리와 `databases.txt` 등록정보를 함께 정리한다. `demodb`는 대상이 아니다.
기존 `clean_env()`는 디렉터리만 지우고 `databases.txt` 항목을 남겨서, 중간에 죽은 실행이
다음 실행을 깨뜨렸다(이번에 실제로 `destinationdb` 잔여 항목을 발견).

---

## 4. 고친 테스트 케이스 문제 (참고)

| 케이스 | 문제 | 조치 |
| --- | --- | --- |
| `createdb`, `createdb_for_copydb`, `createdb_fail_with_dup_name` | 서버가 필수로 요구하는 `charset` 누락 → `alatestdb` 생성 실패가 후속 ~15건으로 연쇄 | `"charset":"en_US"` 추가 |
| `viewlog`, `removelog` | 존재하지 않는 옛 로그 경로(`cub_js.access.log`) 참조 | viewlog는 실제 파일(`cub_manager.log`)로, removelog는 `build_env`가 만드는 일회용 파일로 변경 |
| `getfolderswithkeyword` | 존재하지 않는 `$CUBRID/tmp1` | `$CUBRID/tmp`로 수정 |
| `unloaddb` | `code`가 PUBLIC 소유라 CUBRID 11.5에서 `dba.code`로 해석돼 not found | `"classname":"public.code"`로 수정 |
| `optimizedb`(2번째, db-api 섹션) | 앞서 `deletedb`로 삭제된 `alatestdb`를 참조하는 중복 항목 | `task_list.txt`에서 주석 처리 |
| `addtrigger`, `altertrigger`, `droptrigger` | 서버가 `;`를 붙이지 않음 | 마지막 값에 `;` 추가 (1-3) |
| `compactdb` | 앞선 태스크로 오염된 `alatestdb` 사용 | 전용 DB 생성/삭제로 분리 (2-1) |
| `renamedb` | advanced on 경로가 맵 파일 형식 불일치로 실패 | `advanced:"off"`로 변경 + 뒷정리 추가 (2-2) |

`build_env()`에 removelog용 일회용 파일 생성 로직(`$CUBRID/tmp/test_removelog.log`)을 추가했다.

---

## 5. 환경 제약 / 비결정적 케이스 (남은 10건)

이 검증 환경(non-HA, shard 미구성, 모니터링 통계 비활성, 특정 프로세스/트랜잭션 부재)에서는
성공할 수 없다. 서버 버그가 아니며, 테스트 케이스만으로는 결정적으로 통과시킬 수 없다.

| 케이스 | 증상 | 성격 |
| --- | --- | --- |
| `changemode` | `The server was not configured for HA.` | HA 미구성 |
| `rolechange` | `'deact' command is invalid.` | HA 미구성 |
| `set_mon_interval` | `Set monitoring interval for monitoring statistic failed!` | `support_mon_statistic=NO` |
| `get_mon_statistic` (16건 중 5건) | `Can't find dbname_vol[demodb] in meta[k_db_rrd]`, `read rrd file failed [...]` | 모니터링 통계 미수집(rrd 없음) |
| `killprocess` | `No such process` | 하드코딩된 pid를 kill → 비결정적 |
| `killtransaction` | `Invalid tranindex(2(+))` | 하드코딩된 tranindex를 kill → 활성 트랜잭션 없으면 실패 |

### 참고
- HA 계열(`changemode`, `rolechange`)과 모니터링 통계 계열은, HA를 구성하고
  `cm.conf`의 `support_mon_statistic=YES` + 데이터 수집 후에만 검증 가능하다.
- `killprocess` / `killtransaction`은 실행 시점에 실제로 존재하는 pid/tranindex가 있어야
  성공한다. 현재 케이스는 고정 값(`2(+)` 등)을 써서 항상 실패한다. 결정적으로 만들려면
  테스트가 대상 프로세스/트랜잭션을 스스로 만들고 그 id를 넣도록 재설계해야 한다.

---

## 6. 새 CMS 빌드에서 드러난 테스트 케이스 문제 (수정 완료)

`dbmtuserlogin`이 고쳐지고 보안 강화 커밋(`a2393c2` / `90e82a2`)이 들어간 빌드로 돌리자,
이전 실행에서는 보이지 않던 3건이 새로 실패했다. 셋 다 **서버 버그가 아니라 케이스가
낡은 것**이라 테스트 쪽에서 고쳤다.

### 6-1. `runscript` — `script_path`가 인가된 경로 밖

- 증상: `path is not authorized (allowed paths are $CUBRID, $CUBRID/databases): ls`
- 원인: `a2393c2`가 `ts_run_script()`에 `is_authorized_filename()` 검사를 추가했다
  (`cm_job_task.cpp:11522`, `cm_server_util.cpp:4198`). 케이스는 `script_path`로 `"ls"`를
  넘기는데, 상대 경로라 `$CUBRID` / `$CUBRID_DATABASES` 밑으로 해석되지 않아 거부된다.
- 조치: `build_env()`가 `$CUBRID/tmp/test_runscript.sh`(0755)를 만들고, 케이스가 그 경로를
  가리키도록 변경. `run_child()`가 스크립트를 직접 exec하므로 실행 권한과 shebang이 필요하다.

### 6-2. `backupdb_rep` — `safereplication`이 서버에서 제거됨

- 증상: `expected failure, got success`
- 원인: 이 케이스는 `backupdb`와 `safereplication:"y"` 하나만 다르고, 그 값 때문에 실패하는
  것을 기대했다. 예전 `ts_backupdb()`는 이 값이 `y`면
  ``--safe-page-id `repl_safe_page <db>` `` 를 인자로 덧붙였고, 백틱이 확장되지 않은 채
  `cubrid backupdb`에 전달돼 실패했다. `a2393c2`가 이 백틱 명령 삽입 경로를 제거해서
  이제 `safereplication` 키는 **아무 데서도 읽히지 않는다**(`ts_backupdb()`,
  `cm_job_task.cpp:4538`).
- 조치: 기대값을 success로 변경(`task_list.txt`). 같은 볼륨명으로 백업을 두 번 수행하는
  커버리지는 그대로 남는다.

### 6-3. `updateuser_nopasswd` — `userpass` 생략은 원래 정상

- 증상: `expected failure, got success`
- 원인: `ts_update_user()`(`cm_job_task.cpp:830`)는 `userpass`가 **있는데** 값이
  `__NULL__`이거나 빈 문자열일 때만 거부한다. 키 자체가 없으면 "비밀번호는 그대로 두고
  groups/authorization만 갱신"이 정상 동작이다.
- 이전 실행에서 이 케이스가 통과했던 것은 **우연**이다. 1-1 때문에 선행 `createuser`가
  실패해 `yifan`이 없었고, 그래서 `User "yifan" is invalid.`로 실패했을 뿐이다.
  1-1이 고쳐져 `yifan`이 실제로 생기자 갱신이 정상 성공한다.
- 조치: 기대값을 success로 변경(`task_list.txt`).

---

## 7. 재현 방법

```sh
cd server/test
python3 test_tasks.py                      # 전체 실행, 실패는 빨간색 "expected ... got ..."
TEST_XML=log/result.xml python3 test_tasks.py   # JUnit XML 리포트

# 개별 확인 (실제 토큰으로 원본 응답 출력)
python3 test_tasks.py --dump dbmtuserlogin
```

---

## 8. 남은 서버 측 확인 과제

| 항목 | 상태 | 내용 |
| --- | --- | --- |
| 1-1 | 실행 서버 반영됨 / **소스 미반영** | `SET{t.g.name}` → `SET{t.g}`. 실행 중인 바이너리에는 두 쿼리가 모두 들어 있어 버전 분기가 된 것으로 보인다. 같은 수정을 이 저장소 소스(`cm_job_task.cpp:10173`)에도 반영해야 한다 |
| 1-3 | **미반영** | `op_make_triggerinput_file_add/alter/drop()`에서 문장 끝 `;` 출력. 새 빌드에도 안 들어갔음(포맷 문자열 확인). 고치면 테스트의 `;` 우회 되돌리기 |
| 2-2 | 미확인 | `tsRenameDB()`의 advanced on 경로: `"%d %s %s\n"` 맵 파일 형식이 CUBRID 11.5 `cubrid renamedb -i`와 불일치. 현재 테스트는 advanced off로만 검증 중 |
