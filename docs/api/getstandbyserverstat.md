# getstandbyserverstat

Returns insert_counter, update_counter, delete_counter, commit_counter, fail_counter and replication delay on replica database.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |

| task | Task name |
| token | Token string encrypted. |
| dbname | Database name |
| dbid | DBA user ID |
| dbpasswd | DBA user Password |

## Request Sample

```
{
  "task": "getstandbyserverstat",
  "token": "cdfb4c5717170c5e673cf07a9b448162c895920ae8799faa2fbe13c787b4cbbd7926f07dd201b6aa",
  "dbname": "demodb",
  "dbid": "dba",
  "dbpasswd": ""
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| dbname | database name |
| delay_time | the replication delay of the standby server, in seconds |
| insert_counter | the number of the replicated insert statements |
| update_counter | the number of the replicated update statements |
| delete_counter | the number of the replicated delete statements |
| commit_counter | the number of the replicated commits |
| fail_counter | the number of the replications which failed |

## Response Sample

```
{
   "__EXEC_TIME" : "26 ms",
   "commit_counter" : "1024",
   "dbname" : "demodb",
   "delay_time" : "0",
   "delete_counter" : "12",
   "fail_counter" : "0",
   "insert_counter" : "512",
   "note" : "none",
   "status" : "success",
   "task" : "getstandbyserverstat",
   "update_counter" : "48"
}
```
