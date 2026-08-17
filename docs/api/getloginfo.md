# getloginfo

Get database log file information.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| dbname | database name |

## Request Sample

```
{
  "task":"getloginfo",
  "token":"cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa",
  "dbname":"demodb"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| dbname | database name |
| loginfo | one entry holding a `log` array, one object per log file |

### log

log is composed of objects with following structure

| **Key** | **Description** |
| --- | --- |
| path | database log file path |
| @owner | database owner |
| size | the size of log file |
| lastupdate | update time |

## Response Sample

```
{
   "__EXEC_TIME" : "1 ms",
   "dbname" : "demodb",
   "loginfo" : [
      {
         "log" : [
            {
               "@owner" : "cubrid",
               "lastupdate" : "2026.08.14",
               "path" : "/home/cubrid/CUBRID-11.5.0.2441-6ba9522-Linux.x86_64/log/server/demodb_20260814_1250.err",
               "size" : "567156"
            },
            {
               "@owner" : "cubrid",
               "lastupdate" : "2026.08.18",
               "path" : "/home/cubrid/CUBRID-11.5.0.2441-6ba9522-Linux.x86_64/log/server/demodb_latest.err",
               "size" : "6453"
            },
            {
               "@owner" : "cubrid",
               "lastupdate" : "2026.08.14",
               "path" : "/home/cubrid/CUBRID-11.5.0.2441-6ba9522-Linux.x86_64/log/server/demodb_20260814_1513.err",
               "size" : "12239"
            }
         ]
      }
   ],
   "note" : "none",
   "status" : "success",
   "task" : "getloginfo"
}
```

> Lists are shortened to 3 entries here; the real response returned up to 15.
