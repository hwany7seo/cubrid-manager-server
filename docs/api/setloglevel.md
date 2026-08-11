# setloglevel

Change the log level of CMS at runtime. The level is applied immediately, it is not written to
`cm.conf`, so it goes back to the configured level when CMS restarts.

The valid levels, from the least to the most verbose, are 0 (ERROR), 1 (WARN), 2 (INFO) and
3 (DEBUG). A value greater than 3 makes the request fail with `invalid log level!`.
When `log_level` is omitted, INFO is used.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| log_level | the new log level, from 0 to 3 |

## Request Sample

```
{
  "task": "setloglevel",
  "token": "4504b930fc1be99bf5dfd31fc5799faaa3f117fb903f397de087cd3544165d857926f07dd201b6aa",
  "log_level": 3
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| log_level | the log level which has been set |

## Response Sample

```
{
  "task": "setloglevel",
  "log_level": 3,
  "status": "success",
  "note": "none"
}
```
