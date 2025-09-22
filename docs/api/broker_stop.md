# broker_stop

The broker_stop interface will stop a specified broker.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| bname | name of the broker to stop |


## Request Sample

```
{
  "task": "broker_stop",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa",
  "bname": "broker1"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| note | if failed, a brief description will be given here |
| status | execution result, success or failed. |
| task | task name |

## Response Sample

```
    {
    "__EXEC_TIME" : "1200 ms",
    "note" : "none",
    "status" : "success",
    "task" : "broker_stop"
    }
```
