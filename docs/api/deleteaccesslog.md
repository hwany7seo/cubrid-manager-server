# deleteaccesslog

Delete access log files.


**This interface is no longer supported.** The `deleteaccesslog` task is not registered by the current
manager server, a request which uses it fails with `Undefined request - deleteaccesslog`.
Use [removelog](removelog.md) to delete the access log files instead.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |

## Request Sample

```
{
  "task": "deleteaccesslog",
  "token": "4504b930fc1be99bf5dfd31fc5799faaa3f117fb903f397de087cd3544165d857926f07dd201b6aa"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, it is always failure on the current manager server |
| note | if failed, a brief description will be given here |

## Response Sample

```
{
   "note" : "Undefined request - deleteaccesslog",
   "status" : "failure",
   "task" : "deleteaccesslog"
}
```
