# geterrorlogfiles

Get the list of the CMS error log files (`*.err`) stored in the `$CUBRID/log/manager` directory.
If no file is found, the default error log path is returned.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |

## Request Sample

```
{
  "task": "geterrorlogfiles",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| logfileslist | the list of the error log files |

### logfileslist

logfileslist is composed of objects with following structure

| **Key** | **Description** |
| --- | --- |
| logfile | the full path of an error log file |

## Response Sample

```
{
   "__EXEC_TIME" : "4 ms",
   "logfileslist" : [
      {
         "logfile" : "/home/cubrid/CUBRID/log/manager/cub_js.err"
      }
   ],
   "note" : "none",
   "status" : "success",
   "task" : "geterrorlogfiles"
}
```
