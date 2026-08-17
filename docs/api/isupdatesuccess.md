# isupdatesuccess

Check the result of the previous [autoupdate](autoupdate.md) execution, by reading the
`cms_auto_update.log` and the `cms_auto_update.err` files of the temporary directory of CMS.

Since [autoupdate](autoupdate.md) is no longer supported, this interface normally fails with a
file open error because those files do not exist.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |

## Request Sample

```
{
  "task": "isupdatesuccess",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| autoupdate_success | it is set to `success` when the update log reports that CMS has been updated |
| autoupdate_result | it is set to `failure` when the update log does not report a successful update |

## Response Sample

What the task actually answers on a server where autoupdate was never run:

```
{
   "__EXEC_TIME" : "0 ms",
   "note" : "File(/home/cubrid/CUBRID-11.5.0.2441-6ba9522-Linux.x86_64/tmp/cms_auto_update.log) open error",
   "status" : "failure",
   "task" : "isupdatesuccess"
}
```

`autoupdate_success` / `autoupdate_result` are only present when the log file
exists, which needs an [autoupdate](autoupdate.md) run — no longer possible.
