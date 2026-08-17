# viewlog/viewlog2

View specified log file.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| path | log file path |
| start | the line number at the beginning |
| end | the line number at the end |

## Request Sample

```
{
  "task":"viewlog",
  "token":"cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa",
  "dbname":"demodb",
  "path":"$CUBRID/log/manager/cub_manager.log",
  "start":"1",
  "end":"1000"
}
```

`viewlog2` takes the same request and answers the same way.

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| path | the full path of the log file that was read |
| start | the first line number that was returned |
| end | the last line number that was requested |
| total | the number of lines the file has |
| log | one entry holding a `line` array, one string per log line |

## Response Sample

```
{
   "__EXEC_TIME" : "2 ms",
   "end" : "1000",
   "log" : [
      {
         "line" : [
            "[20260814 12:33:50] [ INFO] [1102235] [main:917] started 'cub_manager' with Engine Version: 11.5",
            "[20260814 12:47:15] [ INFO] [1102235] [write_manager_access_log:642] access_log admin 127.0.0.1 login before add token into token list.",
            "[20260814 12:47:15] [ INFO] [1102235] [write_manager_access_log:642] access_log - - - user_token_info is null."
         ]
      }
   ],
   "note" : "none",
   "path" : "/home/cubrid/CUBRID-11.5.0.2441-6ba9522-Linux.x86_64/log/manager/cub_manager.log",
   "start" : "1",
   "status" : "success",
   "task" : "viewlog",
   "total" : "2873"
}
```

> Lists are shortened to 3 entries here; the real response returned 1000
> lines (`end` - `start` + 1, capped at what the file has).
