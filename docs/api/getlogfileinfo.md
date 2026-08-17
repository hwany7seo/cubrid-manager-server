# getlogfileinfo

Get logfile info.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| broker | target broker name |

## Request Sample

```
{
  "task": "getlogfileinfo",
  "token": "cdfb4c5717170c5edd00cbca92930b73c8960905fd00c5b4e359db6c8c0075367926f07dd201b6aa",
  "broker": "query_editor"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| note | if failed, a brief description will be given here |
| status | execution result, success or failed. |
| task | task name |
| broker | target broker name |
| from | |
| logfileinfo | list of log file groups |

### logfile group

| **Key** | **Description** |
| --- | --- |
| logfile | list of log file information |

### logfile information

| **Key** | **Description** |
| --- | --- |
| lastupdate | date of last update |
| owner | owner of the log file |
| path | stored path of log file |
| size | size of log file |
| type | type of the log file |



## Response Sample

```
{
   "__EXEC_TIME" : "2 ms",
   "broker" : "query_editor",
   "from" : "",
   "logfileinfo" : [
      {
         "logfile" : [
            {
               "lastupdate" : "2026.08.18",
               "owner" : "cubrid",
               "path" : "/home/cubrid/CUBRID-11.5.0.2441-6ba9522-Linux.x86_64/log/broker/sql_log/query_editor_1.sql.log",
               "size" : "5444",
               "type" : "script"
            },
            {
               "lastupdate" : "2026.08.14",
               "owner" : "cubrid",
               "path" : "/home/cubrid/CUBRID-11.5.0.2441-6ba9522-Linux.x86_64/log/broker/sql_log/query_editor_1.slow.log",
               "size" : "0",
               "type" : "script"
            },
            {
               "lastupdate" : "2026.08.18",
               "owner" : "cubrid",
               "path" : "/home/cubrid/CUBRID-11.5.0.2441-6ba9522-Linux.x86_64/log/broker/sql_log/query_editor_2.sql.log",
               "size" : "4414",
               "type" : "script"
            }
         ]
      }
   ],
   "note" : "none",
   "status" : "success",
   "task" : "getlogfileinfo"
}
```

> Lists are shortened to 3 entries here; the real response returned up to 10.
