# removecasrunnertmpfile

Remove a temporary file which [executecasrunner](executecasrunner.md) created.

Only files located under the temporary directory of CMS can be removed, and their name must
contain `log_converted`, `cas_log_tmp` or `log_run`. Any other file makes the request fail with
a permission error.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| filename | the full path of the temporary file to be removed |

## Request Sample

```
{
  "task": "removecasrunnertmpfile",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa",
  "filename": "$CUBRID/tmp/log_run_1.res.0"
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
   "task" : "removecasrunnertmpfile"
}
```
