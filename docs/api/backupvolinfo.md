# backupvolinfo

The backupvolinfo interface will get database backup volume information.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| dbname | database name |
| level | backup level, 0, 1 or 2 |
| pathname | the full path of the backup volume |

## Request Sample

```
{
  "task": "backupvolinfo",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa",
  "dbname": "alatestdb",
  "level": "0",
  "pathname": "$CUBRID_DATABASES/alatestdb/backup/alatestdb_backup_lv0"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| line | a line of the output of the `cubrid backupdb -r` utility |

## Response Sample

```
{
   "__EXEC_TIME" : "36 ms",
   "line" : "Backup-Volume-Info: demodb_backup_lv0",
   "note" : "none",
   "status" : "success",
   "task" : "backupvolinfo"
}
```
