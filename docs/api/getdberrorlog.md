# getdberrorlog

Get the contents of the error log files of a database. The files are read from the
`$CUBRID/log/server` directory; a file is selected when its name starts with the database name
and ends with `.err`, and when its modification time is inside the requested period.

At most 2000 lines are returned. When the limit is reached, the reading stops and `overflow` is
returned with the value 1.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| dbname | database name |
| start_time | the beginning of the period, in the `YYYY/MM/DD HH:MM:SS` form. It is optional |
| end_time | the end of the period, in the `YYYY/MM/DD HH:MM:SS` form. It is optional |

## Request Sample

```
{
  "task": "getdberrorlog",
  "token": "4504b930fc1be99bf5dfd31fc5799faaa3f117fb903f397de087cd3544165d857926f07dd201b6aa",
  "dbname": "demodb",
  "start_time": "2026/08/01 00:00:00",
  "end_time": "2026/08/11 23:59:59"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| dbname | database name |
| start_time | the beginning of the requested period |
| end_time | the end of the requested period |
| result | the list of the error log files and of their contents |
| overflow | it is set to 1 when more than 2000 lines have been found |

### result

result is composed of objects with following structure

| **Key** | **Description** |
| --- | --- |
| file | the full path of the error log file |
| logs | the lines of that error log file |

## Response Sample

```
{
  "task": "getdberrorlog",
  "dbname": "demodb",
  "start_time": "2026/08/01 00:00:00",
  "end_time": "2026/08/11 23:59:59",
  "result": [
    {
      "file": "/home/cubrid/CUBRID/log/server/demodb_20260811_1022.err",
      "logs": [
        "Time: 08/11/26 10:22:31.682 - ERROR *** file ../../src/transaction/boot_sr.c, line 2841 ERROR CODE = -4 Tran = -1, EID = 1",
        "Has been interrupted."
      ]
    }
  ],
  "status": "success",
  "note": "none"
}
```
