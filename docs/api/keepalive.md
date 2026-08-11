# keepalive

Keep the session alive. The request is held by CMS for 10 seconds and then it returns success,
which refreshes the token of the client without executing any job.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |

## Request Sample

```
{
  "task": "keepalive",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | it is returned empty when the request succeeds |

## Response Sample

```
{
   "__EXEC_TIME" : "10001 ms",
   "note" : "",
   "status" : "success",
   "task" : "keepalive"
}
```
