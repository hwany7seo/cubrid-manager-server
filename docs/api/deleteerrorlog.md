# deleteerrorlog

Delete error log files.


**This interface is no longer supported.** The `deleteerrorlog` task is not registered by the current
manager server, a request which uses it fails with `Undefined request - deleteerrorlog`.
Use [removelog](removelog.md) to delete the error log files instead.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |

## Request Sample

```
{
  "task": "deleteerrorlog",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |

## Response Sample

Because the task is not registered, the server rejects it. There is no
`__EXEC_TIME` in the answer, the request never reaches a handler.

```
{
   "note" : "Undefined request - deleteerrorlog",
   "status" : "failure",
   "task" : "deleteerrorlog"
}
```
