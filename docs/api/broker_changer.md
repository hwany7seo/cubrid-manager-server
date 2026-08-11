# broker_changer

Change a broker parameter dynamically by running the `broker_changer` utility. The change is
applied to the running broker, it is not written to `cubrid_broker.conf`.

When `casnum` is given, the parameter is changed only for that application server of the broker;
when it is omitted, the parameter is changed for the whole broker.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| bname | broker name |
| casnum | the id of the application server (CAS) of the broker. It is optional |
| confname | the name of the broker parameter to be changed |
| confvalue | the new value of the broker parameter |

## Request Sample

```
{
  "task": "broker_changer",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa",
  "bname": "query_editor",
  "confname": "SQL_LOG",
  "confvalue": "ON"
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
   "__EXEC_TIME" : "31 ms",
   "note" : "none",
   "status" : "success",
   "task" : "broker_changer"
}
```
