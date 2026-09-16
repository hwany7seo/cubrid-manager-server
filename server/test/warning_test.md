# 컴파일 경고 수정 검증 세트 (task_warning_result)

`cubridmanager` 컴파일 경고 247건(중복 제거 184건)을 제거하면서 손댄 코드가
**실제 동작을 바꾸지 않았는지**, 그리고 경고가 가리키던 결함이 **정말로 없어졌는지**를
CMS JSON API로 확인하는 테스트 세트다.

수정 내역과 결함 분석은 엔진 저장소 루트의 `warning.md`에 있다. 이 문서는 그 문서의
항목 번호(§2.x / §3.x)를 그대로 인용한다.

```
server/test/
  task_test_case/
    task_warning_result.txt        이 세트의 목록 (33 케이스)
    task_warning_result/           요청 JSON 35개
      login, getenv                  init_env()가 직접 읽는 것 (목록에는 없음)
      <나머지 33개>                  목록에 등장하는 케이스
```

---

## 1. 실행 방법

세트 실행 규칙은 `README.md`와 같다. 목록 파일 이름만 넘기면 된다.

```sh
cd server/test

# status 판정만 (빠름)
./run_tests.sh task_warning_result.txt

# 결과 파일 대조
./run_tests.sh -a  11.5 task_warning_result.txt   # 기준값 생성
./run_tests.sh -fc 11.5 task_warning_result.txt   # 기준값과 대조
```

### 회귀 검증 절차

이 세트의 목적은 "수정 전후 응답이 같아야 한다"이므로, 기준값을 **수정 전 빌드**에서
뜨고 **수정 후 빌드**에서 대조한다.

```sh
# 1. 경고 수정이 들어가지 않은 cub_manager를 띄운다
./run_tests.sh -a  11.5 task_warning_result.txt

# 2. 경고 수정이 들어간 cub_manager로 교체하고 재기동한 뒤
./run_tests.sh -fc 11.5 task_warning_result.txt
```

전부 통과하면 "버퍼를 넓히고, 루프 변수를 `size_t`로 바꾸고, `strncpy`/`strncat`을
교체한 것이 응답을 한 바이트도 바꾸지 않았다"가 성립한다.

### 전제 조건

- `test_tasks.conf`에 대상 CMS의 주소가 있을 것
- `demodb`가 **기동 중**일 것 — `lockdb`, `gettransactioninfo` 두 케이스가 서버에
  접속한다. 러너의 `restart_services()`가 `cubrid server start demodb`를 수행하므로
  세트를 통째로 돌리면 자동으로 충족된다
- CM 관리자 계정 `admin` / `admin`

### 세트가 남기는 것

없다. CM 사용자 `warnuser` 하나와 `$CUBRID/tmp/warn_deep_dir_01/...` 디렉터리 하나를
만들었다가 세트 안에서 지운다. 데이터베이스는 만들지 않는다.
중간에 중단했다면 다음 두 가지만 정리하면 된다.

```sh
cm_admin deluser warnuser
rm -rf $CUBRID/tmp/warn_deep_dir_01
```

---

## 2. 커버리지

| warning.md 항목 | 대상 코드 | 케이스 | 판정 |
| --- | --- | --- | --- |
| §2.1 `make_temp_filepath` / `run_child` const화 | `src/cm_common/` | `paramdump`, `start_statdump`, `lockdb` | 회귀 |
| §2.1 `ts_start_statdump`의 `const char *argv[]` | `cm_job_task.cpp` | `start_statdump` / `stop_statdump` | 회귀 |
| §2.2 `ts2_get_logfile_info` `buf[1024]` | `cm_job_task.cpp` | `getlogfileinfo` | 회귀 |
| §2.2 `ts_get_log_info` `buf` | 〃 | `getloginfo` | 회귀(status) |
| §2.2 `ts_get_dbsize` `strbuf` | 〃 | `getdbsize` | 회귀 |
| §2.2 `ts_backupdb_info` `vinf` / `db_backup_dir` | 〃 | `backupdbinfo` | 회귀 |
| §2.2 `ts_list_dir` `full_path` | 〃 | `list_dir_conf`, `list_dir_deep` | 회귀 |
| §2.2 `_backup_cert` / `_recover_cert` / `_is_exist_default_backup_cert` | 〃 | `getcmsenv` | **직접** |
| §2.2 `folder_copy` `src_path` / `dest_path` | `cm_server_util.cpp` | `copyfolder_deep` | 회귀 |
| §2.2 `CLog::_remove_oldest_file` / `_backup_log_files` | `cm_log.h` | 로그 롤오버 시 (전 케이스가 로그를 남긴다) | 간접 |
| §2.4 `_hash_cert()` MD5 hex 조립 재작성 | `cm_job_task.cpp` | `getcmsenv` | **직접** |
| §2.4 `T_USER_TOKEN_INFO` 필드 널 종료 | `cm_user.cpp` | `keepalive` 및 인증이 필요한 모든 케이스 | 회귀 |
| §2.4 `get_sql_text` / `get_next_sqltext` | `cm_job_task.cpp` | `gettransactioninfo` | 회귀(status) |
| §2.5 `SpaceDbResult*`의 `size_t` 루프 | `cm_cmd_exec.cpp` | `dbspaceinfo`, `getdbsize` | 회귀 |
| §2.5 `_validate_token_active_time` | `cm_server_extend_interface.cpp` | 인증이 필요한 모든 케이스 | 회귀 |
| §2.6 `new (int[n])` → `new int[n]` | `cm_mon_stat.cpp` | `get_mon_statistic` | 회귀(status) |
| §3.1 `uRemoveCRLF` 언더플로 | `cm_server_util.cpp` | `viewlog_blankline`, `getallsysparam_cubridconf`, `getaddbrokerinfo`, `unloadinfo` | 회귀 + valgrind |
| §3.3 `uDecrypt`의 `sizeof(포인터)` memset | `cm_text_encryption.c` | `login`(admin), `login_shortpw` 외 | 회귀 + valgrind |
| §3.4 `read_stdout_stderr_as_err` NULL / `fclose(NULL)` | `cm_job_task.cpp` | `lockdb` | 회귀(status) |
| §3.7 `ts_list_dir`의 `name_temp` | 〃 | `copyfolder_deep` → `list_dir_deep` | 회귀 |
| §3.8 `uEncrypt`의 미초기화 패딩 | `cm_text_encryption.c` | `adddbmtuser_shortpw` → `login_shortpw` 왕복 | 회귀 + valgrind |
| §3.2 `colon_idx` npos 절단 | `cm_mon_stat.cpp` | — | **도달 불가** (4장) |
| §3.5 `THREAD_BEGIN`의 `free()` | `cm_porting.h` | — | **도달 불가** (4장) |
| §3.6 `parseaddress` 조건식 | `cm_mailer.h` | — | **판정 불가** (4장) |

---

## 3. 케이스 설명

### 3.1 세션 (`login`, `getenv`, `keepalive`)

`login`과 `getenv`는 목록에 없다. 러너의 `init_env()`가 직접 읽어서 세션 토큰과
`$CUBRID` 경로를 얻는다. **목록에 `login`을 넣으면 안 된다.** 같은 계정으로 두 번째
로그인을 하면 서버가 토큰을 새로 발급하면서 앞의 토큰을 무효화하고, 그 뒤의 모든 요청이
`Request is rejected due to invalid token`으로 떨어진다. 같은 이유로 admin의 비밀번호를
틀리는 케이스도 넣지 않았다 — **실패한 로그인도 그 계정의 토큰을 지운다.**
비밀번호 오류 검증은 아래의 `warnuser` 쪽에서 한다.

`login`은 그 자체가 §3.3의 시험이기도 하다. 배포본 `conf/cm.pass`의 admin 항목은

```
admin:6e85f0f80f030451dc9e98851098dfb2
```

처럼 **32자리** 16진수인데, `uDecrypt(PASSWD_LENGTH=32, ...)`는 64자리를 기대한다.
수정 전에는 `memset(hexacode, 0, sizeof(hexacode))`가 포인터 크기인 8바이트만 지웠기
때문에 33~64번째 문자가 초기화되지 않은 힙이었다.

`keepalive`는 토큰 레코드(§2.4의 `T_USER_TOKEN_INFO` 필드 널 종료)와 토큰 유효시간
검사(§2.5 `_validate_token_active_time`)만 지나가는 가장 가벼운 인증 요청이다.

### 3.2 `getcmsenv` — 이 세트에서 유일하게 값이 갈리는 케이스

응답의 `is_default_cert`는 `_hash_cert()`가 계산한 인증서 MD5를 컴파일 타임 상수
`CMS_DEFAULT_CERT_MD5`와 비교한 결과다.

```json
"is_default_cert" : "yes"
```

수정에서 이 함수의 hex 문자열 조립 방식을 바꿨다.

```c
/* before: 16바이트 버퍼에 2글자씩 만들고 strncat */
char md5_final_hex[MD5_DIGEST_LENGTH];
snprintf (md5_final_hex, 3, "%02x", md5_final[i]);
strncat (hash_value, md5_final_hex, 3);

/* after: 결과 버퍼에 직접, 포인터를 2씩 전진 */
hash_p = hash_value + strlen (hash_value);
snprintf (hash_p, 3, "%02x", md5_final[i]);
hash_p += 2;
```

조립이 한 글자라도 틀어지면 32자리 해시가 상수와 달라져 `"no"`로 뒤집힌다.
즉 이 한 필드가 재작성이 정확했는지를 그대로 알려준다.

### 3.3 암복호 왕복 (§3.3, §3.8)

```
adddbmtuser_shortpw          비밀번호 "a" (1자)
login_shortpw,success        → 저장된 암호문을 풀어 평문 비교
login_shortpw_wrongpw,failure  틀린 비밀번호는 계속 거부되어야 한다
setdbmtpasswd_maxpw          비밀번호를 32자(PASSWD_LENGTH)로 변경
login_maxpw,success          → 새 비밀번호로 로그인
login_oldpw,failure          → 옛 비밀번호는 더 이상 통하지 않는다
deletedbmtuser_warnuser
login_deleted,failure
```

비밀번호 길이를 두 극단으로 잡은 것이 핵심이다.

- **1자** — `uEncrypt`가 암호화하는 32바이트 중 31바이트가 패딩이다. 수정 전에는
  `array_init_random_value(encstr, sizeof(encstr))`가 포인터 크기 8바이트만 채워서
  9~32번째 바이트가 **초기화되지 않은 힙 내용**인 채로 암호화됐다(§3.8).
- **32자** — 패딩이 전혀 없는 경계.

두 경우 모두 저장 → 복호 → 평문 비교가 성립해야 한다. 비밀번호 검증은 저장된 암호문을
복호화해 평문끼리 비교하므로(`cm_cmd_task.cpp`의 `uStringEqual`), 패딩 초기화 방식이
바뀌어도 **기존에 저장된 비밀번호는 그대로 동작한다.** `login_oldpw`가 그 반대편,
즉 "바뀐 비밀번호가 실제로 반영되었는지"를 확인한다.

### 3.4 `uRemoveCRLF` (§3.1)

네 케이스 모두 파일을 `fgets`로 한 줄씩 읽고 `uRemoveCRLF()`로 줄 끝을 다듬는다.

| 케이스 | 읽는 파일 |
| --- | --- |
| `viewlog_blankline` | `$CUBRID/conf/cubrid.conf` (빈 줄 다수) |
| `getallsysparam_cubridconf` | 같은 파일을 파라미터 목록으로 파싱 |
| `getaddbrokerinfo` | `cubrid_broker.conf` |
| `unloadinfo` | unload 로그 |

**빈 줄이 문제였다.** `fgets`가 `"\n"` 하나만 돌려주면 `strlen(str) - 1`이 0이고,
루프가 `str[0]`을 지운 뒤 `i--`로 내려가는데 `i`가 `size_t`라 `SIZE_MAX`가 된다.
`i >= 0`은 항상 참이므로 `str[(size_t) -1]`, 실질적으로 버퍼 **앞** 1바이트를 읽는다.

```c
/* before */
size_t i;
for (i = strlen (str) - 1; (i >= 0) && (str[i] == 10 || str[i] == 13); i--)
  str[i] = '\0';

/* after */
len = strlen (str);
while (len > 0 && (str[len - 1] == 10 || str[len - 1] == 13))
  str[--len] = '\0';
```

응답은 수정 전후가 같다(5장 참고). 이 네 케이스는 **회귀 방지**가 목적이다.
빈 줄이 있는 설정 파일을 파싱한 결과가 그대로여야 한다.

### 3.5 경로 조합 버퍼 (§2.2)

`getlogfileinfo` / `getloginfo` / `getdbsize` / `dbspaceinfo` / `backupdbinfo` /
`paramdump`는 각각 `"<디렉터리>/<이름>"`을 조합하던 버퍼를 `COMPOSED_PATH_MAX`
(`PATH_MAX + NAME_MAX + 2`)로 넓힌 함수를 지나간다. 응답이 그대로여야 한다.

`paramdump_nodbname,failure`는 파라미터 누락 경로를 확인한다. `ts_paramdump`에서
`_dbmt_error`에 널 종료 없이 복사하던 `strncpy`를 `snprintf`로 바꿨으므로(§2.4),
오류 메시지가 깨지지 않는지도 함께 본다.

### 3.6 깊은 경로 (`copyfolder_deep` → `list_dir_deep` → `deletefolder_deep`)

`copyfolder_deep`이 `$CUBRID/tmp` 아래에 **679자**짜리 디렉터리 경로를 만들고
(`warn_deep_dir_01/.../warn_deep_dir_40`) `$CUBRID/conf`의 파일을 그 안에 복사한다.
`list_dir_deep`이 그 디렉터리를 나열하고, `deletefolder_deep`이 지운다.

- `copyfolder` → `folder_copy()`의 `src_path` / `dest_path` (§2.2)
- `list_dir` → `ts_list_dir()`의 `full_path`와 `name_temp` (§2.2, §3.7)

`ts_list_dir()`은 `strcpy(name_temp, full_path); strcat(name_temp, entry->d_name)`으로
1024바이트 버퍼를 채우고 있었다. 이번 수정에서 다음처럼 바뀌었다.

```c
char name_temp[sizeof (full_path) + NAME_MAX + 1];
snprintf (name_temp, sizeof (name_temp), "%s%s", full_path, entry->d_name);
```

679자를 고른 이유는 4장에 적었다.

`list_dir_traversal,failure`와 `viewlog_outside,failure`는 `full_path`를 넓힌 뒤에도
경로 검증(`../` 차단, `$CUBRID` 밖 차단)이 그대로 동작하는지 확인한다.

### 3.7 나머지

- `get_mon_statistic` — `cm_mon_stat.cpp`에서 `new (int[n])`을 `new int[n]`으로 고친
  8개 샘플러 중 3개(os / db / broker)를 요청한다. 응답 표본 수가 서버 가동 시간에 따라
  늘어나므로 status 판정만 한다.
- `start_statdump` / `stop_statdump` — `ts_start_statdump()`의 `char *argv[10]`을
  같은 파일의 다른 함수들과 같은 `const char *argv[10]`으로 바꾼 부분. 두 케이스는
  붙어 있어야 한다(`stop`은 방금 띄운 프로세스가 있어야 성공한다).
- `lockdb` — `_run_child()`를 쓰는 task. 자식이 0이 아닌 코드로 끝나면
  `read_stdout_stderr_as_err(out, NULL, ...)`가 호출되는 경로(§3.4)로 들어간다.
- `gettransactioninfo` — `get_sql_text()` / `get_next_sqltext()`를 지나간다.
  전자는 `strncpy(dst, src, strlen(src))`를 `snprintf`로, 후자는 문자열 복사가 아니라
  블록 복사였던 `strncpy`를 `memcpy`로 바꾼 곳이다(§2.4).

---

## 4. API로 판정할 수 없는 것

솔직하게 적어 둔다. 아래 항목은 이 세트가 **코드 경로는 지나가지만 응답만으로는
수정 전후를 구분하지 못하거나**, 아예 API에서 도달할 수 없다.

### 4.1 응답으로는 구분되지 않는 것 → valgrind로 확인

`uDecrypt`(§3.3), `uEncrypt`(§3.8), `uRemoveCRLF`(§3.1)의 결함은 모두
**초기화되지 않은 메모리를 읽거나 버퍼 밖을 읽는** 종류다. 읽은 값이 결과에 반영되지
않기 때문에 JSON 응답은 수정 전후가 같다. 차이는 메모리 검사기에서만 보인다.

실측한 결과다. `cm_text_encryption.c`만 떼어 내 배포본 `cm.pass`의 admin 항목
(32자리 = 기대 길이의 절반)을 복호화시켰다.

```sh
gcc -g -O0 -I<src> -I<builddir> -DLINUX -o dec_test dec_test.c cm_text_encryption.c
valgrind ./dec_test
```

```
# 수정 전
==293139== Conditional jump or move depends on uninitialised value(s)
==293139==    at ut_get_hexval (cm_text_encryption.c:241)
==293139==    by uDecrypt (cm_text_encryption.c:130)
   ... 4건
decrypted=[admin] match=yes        <- 결과는 정상

# 수정 후
==293256== ERROR SUMMARY: 0 errors from 0 contexts
decrypted=[admin] match=yes
```

`uEncrypt`는 1자 비밀번호를 암호화시켰다.

```
# 수정 전
==293278== Use of uninitialised value of size 8
==293278==    at _itoa_word / vfprintf / vsprintf (sprintf 안)
==293282== ERROR SUMMARY: 252 errors from 4 contexts

# 수정 후
==293288== ERROR SUMMARY: 0 errors from 0 contexts
```

**서버 전체를 검사기 아래에서 돌리려면** 다음처럼 하고 이 세트를 실행한다.

```sh
cubrid manager stop
valgrind --trace-children=yes --log-file=$CUBRID/log/manager/vg.%p.log \
         $CUBRID/bin/cub_manager
# 다른 셸에서
cd server/test && ./run_tests.sh task_warning_result.txt
```

수정 전 빌드에서는 `uDecrypt` / `uEncrypt` / `uRemoveCRLF` 프레임이 로그에 남고,
수정 후 빌드에서는 사라진다.

### 4.2 API에서 도달할 수 없는 것

| 항목 | 이유 |
| --- | --- |
| §3.2 `colon_idx` npos 절단 (`cm_mon_stat.cpp`) | HA 모니터링 수집 스레드에서, `copylogdb` 값에 콜론이 없을 때만 들어간다. HA 구성과 잘못된 설정값이 동시에 필요해 이 세트로는 만들 수 없다. `task_ha_result_check` 세트에서도 정상 값만 오므로 마찬가지다. |
| §3.5 `THREAD_BEGIN`의 `free()` | `pthread_create` 실패 분기인데, 그 판정이 `< 0`이었다. `pthread_create`는 실패해도 errno 값(양수)을 돌려주므로 **원래 실행될 수 없는 코드**였다. 요청으로 스레드 생성을 실패시킬 방법도 없다. |
| §3.6 `parseaddress` (`cm_mailer.h`) | `sendmail` task로 호출되기는 하나, 수정 전후 결과가 같다. `@`가 없는 주소는 수정 전에도 함수 끝의 폴백에서 같은 값(`address = 입력값`)을 돌려줬다. 게다가 실제 판정에는 SMTP 서버가 필요하다. |
| §2.2 `get_my_time()`의 128바이트 `strbuf` | 유일한 호출부(`cm_autojob.cpp:333`)가 `mytime = all_volumes->get_my_time(dbloca); mytime = time(&mytime);`으로 **반환값을 바로 덮어쓴다.** 결과가 쓰이지 않으므로 절단돼도 관측되지 않는다. |
| §2.4 `T_USER_TOKEN_INFO.user_id` 널 종료 | `user_id`는 64바이트인데 CM 사용자 이름은 서버가 **32자로 제한**한다(33자부터 `Invalid user name!`). 필드를 꽉 채울 수 없어 널 종료 누락이 발생하지 않는다. `user_ip[20]` / `user_port[10]`도 클라이언트 주소·포트라 채울 방법이 없다. |
| §3.4 `read_stdout_stderr_as_err`의 `fclose(NULL)` | `access()`가 성공한 직후 `fopen()`이 실패해야 하는데(권한 변경 등), 그 파일은 매니저가 방금 만든 임시 파일이라 요청으로 그 상황을 만들 수 없다. NULL 인자 경로(`access(NULL, ...)`) 자체는 `lockdb`가 실패할 때 지나간다. |

### 4.3 경로 절단(§2.2)이 실제로 재현되지 않는 이유

경로 조합 버퍼는 대부분 `PATH_MAX`(4096)였고, 잘리려면 원본 디렉터리가 4000자를
넘어야 한다. 그런데 매니저에서 디렉터리를 만드는 유일한 통로인 `uCreateDir()`이
`char path[1024]`에 `strncpy(path, new_dir, 1023)`로 복사한다. **API로 만들 수 있는
디렉터리 경로는 1023자가 상한**이라 4096바이트 버퍼를 넘길 수 없다.

`list_dir_deep`의 깊이를 679자로 잡은 것도 여기서 나온다.

```
$CUBRID(≈50) + "/tmp/" + 679 ≈ 735   < 1023   → uCreateDir 성공
full_path ≈ 737, + d_name(≤22) ≈ 759 < 1024   → name_temp 오버플로 없음
```

679자를 더 늘리면 `name_temp[1024]`를 넘겨 **수정 전 빌드에서 스택을 깨뜨릴 수 있지만**,
성립 여부가 `$CUBRID` 경로 길이에 좌우되고 성공하면 `cub_manager`가 죽는다. 커밋해 두는
테스트로는 부적절해서 안전한 깊이로 두고, 오버플로는 위 계산으로 문서화만 한다.
직접 확인하려면 셸에서 `$CUBRID` 아래에 1000자 이상 경로를 만든 뒤 `list_dir`을 부르면 된다.

따라서 §2.2는 대부분 **살아 있는 버그의 수정이 아니라 방어적 강화**다. 예외는 목적지가
`PATH_MAX`보다 훨씬 작았던 두 곳이고, 그 중 `get_my_time`은 위처럼 결과가 버려진다.

---

## 5. 검증 기록

이 세트는 수정이 반영된 `cub_manager`(11.4.0.0083 / 엔진 11.5.0.2549)에 대해
33개 케이스를 전부 실행해 확인했다.

- 31개: 목록에 선언한 status와 일치
- 2개(`lockdb`, `gettransactioninfo`): 검증 환경에서 `demodb` 서버가 떠 있지 않아
  `Failed to connect to database server`로 실패. 러너가 `restart_services()`에서
  `cubrid server start demodb`를 수행하는 정상 실행에서는 해당하지 않는다
  (두 task는 `task_result_check` 세트에도 들어 있고 그쪽에서 통과한다).

세트를 만들며 확인한 러너 관련 사실 두 가지도 남겨 둔다.

- 목록에 `login`을 넣으면 안 된다 (3.1 참고).
- 세션 계정의 로그인이 **실패해도** 그 계정의 토큰이 지워진다. admin 비밀번호 오류
  케이스를 목록 중간에 두면 그 뒤가 전부 `invalid token`으로 떨어진다.
