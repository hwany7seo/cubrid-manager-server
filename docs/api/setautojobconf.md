# setautojobconf

Set the configuration of one automation job of CMS. When `service` is `mail_config`, `jobconf`
must be an object which contains a `password` key, otherwise the request fails with
`error mail_config format!`; the password is encrypted before it is stored.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| service | the name of the automation job, such as `auto_start`, `mail_config` or `mail_report` |
| jobconf | the configuration of that automation job |

## Request Sample

```
{
  "task": "setautojobconf",
  "token": "4504b930fc1be99bf5dfd31fc5799faaa3f117fb903f397de087cd3544165d857926f07dd201b6aa",
  "service": "mail_config",
  "jobconf": {
    "smtp_server": "smtp.cubrid.org",
    "sender": "cms@cubrid.org",
    "username": "cms",
    "password": "cubrid"
  }
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
  "task": "setautojobconf",
  "status": "success",
  "note": "none"
}
```
