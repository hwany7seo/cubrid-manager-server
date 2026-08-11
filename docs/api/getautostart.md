# getautostart

Get the auto start configuration of CMS, which tells CMS which databases and which brokers must
be started automatically. When the configuration file does not exist, `auto_start` is returned
as null.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |

## Request Sample

```
{
  "task": "getautostart",
  "token": "4504b930fc1be99bf5dfd31fc5799faaa3f117fb903f397de087cd3544165d857926f07dd201b6aa"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| auto_start | the auto start configuration, grouped by service name |

## Response Sample

```
{
  "task": "getautostart",
  "auto_start": {
    "databases": [
      {
        "dbname": "demodb"
      }
    ],
    "brokers": [
      {
        "bname": "query_editor"
      }
    ]
  },
  "status": "success",
  "note": "none"
}
```
