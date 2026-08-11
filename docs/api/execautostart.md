# execautostart

Execute the auto start configuration at once: the brokers and the databases registered by
[setautostart](setautostart.md) are started. It is the job CMS runs by itself when it starts,
this interface makes it possible to run it on demand.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |

## Request Sample

```
{
  "task": "execautostart",
  "token": "4504b930fc1be99bf5dfd31fc5799faaa3f117fb903f397de087cd3544165d857926f07dd201b6aa"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| brokers | the result of the brokers which have been started |
| databases | the result of the databases which have been started |

## Response Sample

```
{
  "task": "execautostart",
  "databases": [
    {
      "dbname": "demodb",
      "result": "success"
    }
  ],
  "status": "success",
  "note": "none"
}
```
