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
| <volname> | the information of an existing backup volume, the key is the name of the volume |

### <volname>

Every backup volume is composed of objects with following structure

| **Key** | **Description** |
| --- | --- |
| path | the full path of the backup volume |
| size | the size of the backup volume, in bytes |

## Response Sample

```
{
   "__EXEC_TIME" : "8 ms",
   "dbdir" : "/home/cubrid/CUBRID/databases/demodb/backup",
   "demodb_backup_lv0" : [
      {
         "path" : "/home/cubrid/CUBRID/databases/demodb/backup/demodb_backup_lv0",
         "size" : "1148928"
      }
   ],
   "freespace" : "51234",
   "note" : "none",
   "status" : "success",
   "task" : "backupdbinfo"
}
```
