# getbrokerlog

Get the contents of the broker log file, `$CUBRID/log/broker/cubrid_broker.log`.
A line is returned when the date and the time at its beginning are inside the requested period.

At most 2000 lines are returned. When the limit is reached, the reading stops and `overflow` is
returned with the value 1. The request fails when the broker log file does not exist.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| start_time | the beginning of the period, it is compared with the date and the time of the log line. It is optional |
| end_time | the end of the period, it is compared with the date and the time of the log line. It is optional |

## Request Sample

```
{
  "task": "getbrokerlog",
  "token": "4504b930fc1be99bf5dfd31fc5799faaa3f117fb903f397de087cd3544165d857926f07dd201b6aa",
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
| file | the full path of the broker log file |
| start_time | the beginning of the requested period |
| end_time | the end of the requested period |
| log | the lines of the broker log file |
| overflow | it is set to 1 when more than 2000 lines have been found |

## Response Sample

```
{
  "task": "getbrokerlog",
  "file": "/home/cubrid/CUBRID/log/broker/cubrid_broker.log",
  "start_time": "2026/08/01 00:00:00",
  "end_time": "2026/08/11 23:59:59",
  "log": [
    "2026/08/11 10:20:31 query_editor broker is started"
  ],
  "status": "success",
  "note": "none"
}
```
