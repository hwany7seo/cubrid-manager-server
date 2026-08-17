# getfiletotallinenum

Get the total number of the lines of a file. It is normally used together with
[viewlog/viewlog2](viewlogviewlog2.md) to read a log file page by page.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| filepath | the full path of the file |

## Request Sample

```
{
  "task": "getfiletotallinenum",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa",
  "filepath": "$CUBRID/log/manager/cub_js.access.log"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| totalnum | the total number of the lines of the file |

## Response Sample

```
{
   "__EXEC_TIME" : "0 ms",
   "note" : "none",
   "status" : "success",
   "task" : "getfiletotallinenum",
   "totalnum" : "21"
}
```
