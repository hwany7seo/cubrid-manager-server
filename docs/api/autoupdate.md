# autoupdate

Update CMS itself with a patch.

**This interface is no longer supported.** The task is still registered, but it always fails
with the message `We do not support autoupdate anymore`.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |

## Request Sample

```
{
  "task": "autoupdate",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, it is always failure |
| note | the reason of the failure |

## Response Sample

```
{
   "__EXEC_TIME" : "1 ms",
   "note" : "We do not support autoupdate anymore",
   "status" : "failure",
   "task" : "autoupdate"
}
```
