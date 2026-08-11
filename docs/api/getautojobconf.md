# getautojobconf

Get the configuration of one automation job of CMS. When `service` is `mail_config`, the stored
password is decrypted before it is returned.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| service | the name of the automation job, such as `auto_start`, `mail_config` or `mail_report` |

## Request Sample

```
{
  "task": "getautojobconf",
  "token": "4504b930fc1be99bf5dfd31fc5799faaa3f117fb903f397de087cd3544165d857926f07dd201b6aa",
  "service": "mail_config"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| jobconf | the configuration of the requested automation job |

## Response Sample

```
{
  "task": "getautojobconf",
  "jobconf": {
    "smtp_server": "smtp.cubrid.org",
    "sender": "cms@cubrid.org",
    "username": "cms",
    "password": "cubrid"
  },
  "status": "success",
  "note": "none"
}
```
