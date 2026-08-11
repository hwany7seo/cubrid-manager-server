# automail

Send the monitoring mail report at once, using the `mail_report` configuration which
[setautojobconf](setautojobconf.md) stores. It is the job CMS runs on its own schedule, this
interface makes it possible to run it on demand. The request fails when the mail report
configuration cannot be read.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |

## Request Sample

```
{
  "task": "automail",
  "token": "4504b930fc1be99bf5dfd31fc5799faaa3f117fb903f397de087cd3544165d857926f07dd201b6aa"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| response | the result reported by the SMTP server for every receiver |

## Response Sample

```
{
  "task": "automail",
  "response": [
    {
      "receiver": "admin@cubrid.org",
      "message": "250 OK"
    }
  ],
  "status": "success",
  "note": "none"
}
```
