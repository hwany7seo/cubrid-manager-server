# loadaccesslog

Get accesslog file.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |


## Request Sample

```
{
  "task": "loadaccesslog",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| accesslog | the list of the entries of the CMS access log |
| errorlog | the list of the entries of the CMS error log |

### accesslog, errorlog

accesslog and errorlog are composed of objects with following structure

| **Key** | **Description** |
| --- | --- |
| user | the CM user which sent the request |
| taskname | the name of the requested task |
| time | the time the request was handled |
| errornote | the error message, it is only returned in errorlog |
| full_line | the whole log line, it is returned when the line cannot be parsed |

## Response Sample

```
{
   "__EXEC_TIME" : "9 ms",
   "accesslog" : [
      {
         "taskname" : "startinfo",
         "time" : "2026.08.11 10:22:31",
         "user" : "admin"
      }
   ],
   "errorlog" : [
      {
         "errornote" : "Undefined request - foo",
         "taskname" : "foo",
         "time" : "2026.08.11 10:24:02",
         "user" : "admin"
      }
   ],
   "note" : "none",
   "status" : "success",
   "task" : "loadaccesslog"
}
```
