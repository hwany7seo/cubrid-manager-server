# setautostart

Set the auto start configuration of one service. The configuration of the service given in
`service` is replaced by the value of the `auto_start` key, the configuration of the other
services is kept unchanged.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| service | the name of the service to be configured, such as `databases` or `brokers` |
| auto_start | the auto start configuration of that service |

## Request Sample

```
{
  "task": "setautostart",
  "token": "4504b930fc1be99bf5dfd31fc5799faaa3f117fb903f397de087cd3544165d857926f07dd201b6aa",
  "service": "databases",
  "auto_start": [
    {
      "dbname": "demodb"
    }
  ]
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
  "task": "setautostart",
  "status": "success",
  "note": "none"
}
```
