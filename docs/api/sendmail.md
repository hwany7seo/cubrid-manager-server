# sendmail

Send an email through an SMTP server. It is used to check the mail configuration of the
automation jobs, and to send a report by hand.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| sender | the email address of the sender |
| receiver | the email address of the receiver |
| smtp_server | the address of the SMTP server |
| username | the user id used to authenticate on the SMTP server |
| password | the password used to authenticate on the SMTP server |
| authtype | the authentication type of the SMTP server: 0 (no authentication), 1 (PLAIN) or 2 (LOGIN). The default is 2 |
| msg_header | the subject of the email |
| msg_body | the body of the email |
| body_type | 0 for a plain text body, 1 for an HTML body. The default is 0 |

## Request Sample

```
{
  "task": "sendmail",
  "token": "4504b930fc1be99bf5dfd31fc5799faaa3f117fb903f397de087cd3544165d857926f07dd201b6aa",
  "sender": "cms@cubrid.org",
  "receiver": "admin@cubrid.org",
  "smtp_server": "smtp.cubrid.org",
  "username": "cms",
  "password": "cubrid",
  "authtype": 2,
  "msg_header": "CMS monitoring report",
  "msg_body": "demodb is running.",
  "body_type": 0
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| response | the result reported by the SMTP server |

### response

response is composed of objects with following structure

| **Key** | **Description** |
| --- | --- |
| receiver | the email address of the receiver |
| message | the message the SMTP server returned |

## Response Sample

```
{
  "task": "sendmail",
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
