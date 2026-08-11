# removestatustemplate

Remove a monitoring status template from the status template configuration file.
Removing a name which does not exist is not treated as an error.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| name | the name of the status template to be removed |

## Request Sample

```
{
  "task": "removestatustemplate",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa",
  "name": "dbserver_clier_requet"
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
   "__EXEC_TIME" : "4 ms",
   "note" : "none",
   "status" : "success",
   "task" : "removestatustemplate"
}
```
