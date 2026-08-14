# CMS API 사용 현황 (cubrid-webmanager / cubrid-manager)

`docs/api`에 문서화된 CMS API 총 **156개**를, 두 클라이언트가 실제로 호출하는지 소스에서 대조한 결과다.

- **WM** = cubrid-webmanager (`apps`,`libs` 의 `task: '<name>'` 호출, 테스트 제외)
- **CM** = cubrid-manager (`.java` 의 `super("<name>"...)` / `"task","<name>"` 호출)
- 판정 기준: 문서 파일명(=task 이름) 단위. `viewlog/viewlog2`는 병합 문서 1건으로 계산.

## 요약

| 구분 | 개수 |
| --- | --- |
| 두 클라이언트 모두 사용 | 42 |
| WM만 사용 | 31 |
| CM만 사용 | 31 |
| 둘 다 미사용 | 52 |
| **WM 사용 합계** | **73** |
| **CM 사용 합계** | **73** |

## 두 클라이언트 모두 사용 (42개)

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

## 둘 다 미사용 (52개)

어느 클라이언트도 호출하지 않는 API. 서버 내부용, 자동화 잡 전용, 확장 인터페이스(ext), 또는 신규/레거시로 클라이언트 미대응인 것들이다.

- `adddbmtuser_new`
- `automail`
- `autoupdate`
- `broker_changer`
- `changemode`
- `copyfolder`
- `dbspace`
- `deleteaccesslog`
- `deleteerrorlog`
- `deletefolder`
- `execautostart`
- `get_mon_statistic`
- `getaccesslogfiles`
- `getautojobconf`
- `getautostart`
- `getbrokerdiagdata`
- `getbrokerlog`
- `getdberrorlog`
- `getdbmtuserinfo_new`
- `getdbprocstat`
- `getenvvarbyname`
- `geterrorlogfiles`
- `getfiletotallinenum`
- `getfolderswithkeyword`
- `gethaapplyinfo`
- `getinitbrokersinfo`
- `getprocstat`
- `getshardstatus`
- `getstandbyserverstat`
- `getstatustemplate`
- `getsysdiskinfo`
- `ha_applylogdb`
- `ha_copylogdb`
- `ha_status`
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
- `start_statdump`
- `stop_statdump`
- `updateattribute`
- `updatedbmtuser_new`
- `writeandsaveconf`
- `writeprivatedata`
