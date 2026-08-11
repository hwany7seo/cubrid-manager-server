# resetlog

Empty the specified log file. The file is truncated to zero length, it is not deleted.
The path must point to a file that CMS is allowed to access, otherwise the request fails.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| path | the full path of the log file to be emptied |

## Request Sample

```
{
  "task": "resetlog",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa",
  "path": "$CUBRID/log/broker/cubrid_broker.log"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |

## Response Sample

```
{
   "__EXEC_TIME" : "2 ms",
   "note" : "none",
   "status" : "success",
   "task" : "resetlog"
}
```
