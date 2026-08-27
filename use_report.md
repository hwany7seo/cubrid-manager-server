# CMS API 사용 현황 (cubrid-webmanager / cubrid-manager / scouter-agent-cubrid)

세 클라이언트가 CMS API를 실제로 호출하는지 소스에서 대조한 결과다. 대조 시점의 문서 **154개**가
대상이었고, 그중 어느 클라이언트도 쓰지 않는 **43개는 이 브랜치에서 `docs/api`에서 제거**했다.
따라서 현재 `docs/api`에 남아 있는 API 문서는 **111개**다.

- **WM** = cubrid-webmanager (`apps`,`libs` 의 `task: '<name>'` 호출, 테스트 제외)
- **CM** = cubrid-manager (`.java` 의 `super("<name>"...)` / `"task","<name>"` 호출)
- **SC** = scouter-agent-cubrid (`src/.../data/CubridTask.java` 의 task 상수)
- 판정 기준: 문서 파일명(=task 이름) 단위. `viewlog/viewlog2`는 병합 문서 1건으로 계산.

## 요약

| 구분 | 개수 |
| --- | --- |
| WM·CM 모두 사용 | 42 |
| WM만 사용 | 31 |
| CM만 사용 | 31 |
| SC만 사용 | 7 |
| 어느 클라이언트도 미사용 (문서 제거됨) | 43 |
| **WM 사용 합계** | **73** |
| **CM 사용 합계** | **73** |
| **SC 사용 합계** | **20** |
| **`docs/api` 잔존 문서** | **111** |

## WM·CM 모두 사용 (42개)

- `adddbmtuser`
- `addvoldb`
- `backupdb`
- `backupdbinfo`
- `broker_setparam`
- `broker_start`
- `broker_stop`
- `checkfile`
- `classinfo`
- `copydb`
- `createdb`
- `dbmtuserlogin`
- `deletebackupinfo`
- `deletedbmtuser`
- `getaddbrokerinfo`
- `getallsysparam`
- `getautoexecquery`
- `getbackupinfo`
- `getbackuplist`
- `getdbmtuserinfo`
- `getdbsize`
- `getenv`
- `heartbeatlist`
- `loadaccesslog`
- `loaddb`
- `login`
- `paramdump`
- `plandump`
- `renamedb`
- `restoredb`
- `setautoaddvol`
- `setautoexecquery`
- `setdbmtpasswd`
- `setsysparam`
- `startbroker`
- `startinfo`
- `stopbroker`
- `unloaddb`
- `unloadinfo`
- `updatedbmtuser`
- `userverify`
- `viewlog/viewlog2`

## WM(webmanager)만 사용 (31개)

- `addbackupinfo`
- `checkdb`
- `compactdb`
- `createuser`
- `dbspaceinfo`
- `deletedb`
- `deleteuser`
- `getaddvolstatus`
- `getadminloginfo`
- `getautoaddvol`
- `getautoaddvollog`
- `getautobackupdberrlog`
- `getautoexecqueryerrlog`
- `getbrokersinfo`
- `getbrokerstatus`
- `gethoststat`
- `getlogfileinfo`
- `getloginfo`
- `gettransactioninfo`
- `ha_reload`
- `ha_start`
- `ha_stop`
- `killtransaction`
- `lockdb`
- `optimizedb`
- `setbackupinfo`
- `startdb`
- `statdump`
- `stopdb`
- `updateuser`
- `userinfo`

## CM(manager)만 사용 (31개)

- `addstatustemplate`
- `addtrigger`
- `altertrigger`
- `analyzecaslog`
- `backupvolinfo`
- `broker_restart`
- `checkdir`
- `class`
- `deletebroker`
- `droptrigger`
- `errortrace`
- `executecasrunner`
- `generatecert`
- `get_mon_interval`
- `getcaslogtopresult`
- `getcmsenv`
- `getdbmode`
- `getdiagdata`
- `getshardinfo`
- `gettriggerinfo`
- `logout`
- `removecasrunnertmpfile`
- `removefiles`
- `removelog`
- `removestatustemplate`
- `resetlog`
- `rolechange`
- `set_mon_interval`
- `shard_start`
- `shard_stop`
- `updatestatustemplate`

## SC(scouter-agent-cubrid)만 사용 (7개)

WM·CM 은 호출하지 않고 scouter 에이전트만 쓰는 API. 모니터링 수집용이다.

- `dbspace`
- `getbrokerdiagdata`
- `getdbprocstat`
- `gethaapplyinfo`
- `ha_status`
- `start_statdump`
- `stop_statdump`

## SC가 WM·CM 과 함께 쓰는 API (13개)

위 분류에 이미 포함된 것들. scouter 사용 합계 20개는 이 13개와 위 7개의 합이다.

- `dbspaceinfo`
- `getaddbrokerinfo`
- `getbrokersinfo`
- `getbrokerstatus`
- `gethoststat`
- `getlogfileinfo`
- `getloginfo`
- `gettransactioninfo`
- `login`
- `plandump`
- `startinfo`
- `statdump`
- `viewlog/viewlog2`

## 어느 클라이언트도 미사용 (43개) — 문서 제거됨

WM·CM·SC 어디에서도 호출하지 않는 API. 서버 내부용, 자동화 잡 전용, 확장 인터페이스(ext), 또는 신규/레거시로 클라이언트 미대응인 것들이다.

**`docs/api/<name>.md` 와 README 표의 해당 행을 제거했다.** 서버 task 테이블에는 그대로 등록되어 있어
호출 자체는 되고, `server/test` 의 테스트 케이스도 유지된다. 아래는 제거된 문서의 목록이다.
복구가 필요하면 이 브랜치의 직전 커밋에서 되살릴 수 있다.

- `adddbmtuser_new`
- `automail`
- `autoupdate`
- `broker_changer`
- `changemode`
- `copyfolder`
- `deletefolder`
- `execautostart`
- `get_mon_statistic`
- `getaccesslogfiles`
- `getautojobconf`
- `getautostart`
- `getbrokerlog`
- `getdberrorlog`
- `getdbmtuserinfo_new`
- `getenvvarbyname`
- `geterrorlogfiles`
- `getfiletotallinenum`
- `getfolderswithkeyword`
- `getinitbrokersinfo`
- `getprocstat`
- `getshardstatus`
- `getstandbyserverstat`
- `getstatustemplate`
- `getsysdiskinfo`
- `ha_applylogdb`
- `ha_copylogdb`
- `isupdatesuccess`
- `keepalive`
- `kill_process`
- `list_dir`
- `monitorprocess`
- `readprivatedata`
- `runscript`
- `runsqlstatement`
- `sendmail`
- `setautojobconf`
- `setautostart`
- `setloglevel`
- `updateattribute`
- `updatedbmtuser_new`
- `writeandsaveconf`
- `writeprivatedata`
