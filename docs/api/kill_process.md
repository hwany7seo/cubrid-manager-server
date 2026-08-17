# kill_process

Send the SIGTERM signal to a process of the host. It is normally used to stop a process which
[monitorprocess](monitorprocess.md) or [getdbprocstat](getdbprocstat.md) reports.
The database information file of CMS is rewritten after the signal is sent.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| pid | the id of the process to be killed |
| name | the name of the process, it is only returned back in the response |

## Request Sample

```
{
  "task": "kill_process",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa",
  "pid": "24513",
  "name": "cub_server demodb"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| name | the name of the process given in the request |

## Response Sample

```
{
   "__EXEC_TIME" : "25 ms",
   "name" : "cub_server demodb",
   "note" : "none",
   "status" : "success",
   "task" : "kill_process"
}
```
