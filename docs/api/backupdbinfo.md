# backupdbinfo

The backupdbinfo interface will get database backup information.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| dbname | database name |

## Request Sample

```
{
  "task": "backupdbinfo",
  "token": "cdfb4c5717170c5e237a227a2ceeccc6ae9e10c16754fb85371c0d74fa0d9d577926f07dd201b6aa",
  "dbname": "alatestdb"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| dbdir | the default backup directory of the database |
| freespace | the free space of the database directory, in MB |
| level\<n\> | the backup volumes of that backup level, one key per level (`level0`, `level1`, ...) |

### level\<n\>

Every backup level is composed of objects with following structure

| **Key** | **Description** |
| --- | --- |
| path | the full path of the backup volume |
| size | the size of the backup volume, in bytes |
| data | the moment the backup was taken, `YYYY.MM.DD.HHMM` |

## Response Sample

```
{
   "__EXEC_TIME" : "29 ms",
   "dbdir" : "/home/cubrid/CUBRID-11.5.0.2441-6ba9522-Linux.x86_64/databases/alatestdb/backup",
   "freespace" : "446128",
   "level0" : [
      {
         "data" : "2026.08.18.07.40",
         "path" : "/home/cubrid/CUBRID-11.5.0.2441-6ba9522-Linux.x86_64/databases/alatestdb/backup/alatestdb_backup_lv0/alatestdb_bk0v000",
         "size" : "2110464"
      }
   ],
   "note" : "none",
   "status" : "success",
   "task" : "backupdbinfo"
}
```
