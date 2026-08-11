# removelog

Delete the log files given in the `files` list. Every path is checked before it is removed:
a path that CMS is not allowed to access, or that does not exist, makes the request fail.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| files | the list of the log files to be removed |

### files

files is composed of objects with following structure

| **Key** | **Description** |
| --- | --- |
| path | the full path of a log file |

## Request Sample

```
{
  "task": "removelog",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa",
  "files": [
    {
      "path": "$CUBRID/log/manager/cub_js.access.log"
    }
  ]
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
   "__EXEC_TIME" : "3 ms",
   "note" : "none",
   "status" : "success",
   "task" : "removelog"
}
```
