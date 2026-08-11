# changemode

Change active status on broker.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| dbname | database name |
| modify | the new HA mode of the database server: standby, maintenance or active. When it is omitted, the current mode is returned without being changed |
| force | yes or no, change the mode even when the transactions are not finished |

## Request Sample

```
{
  "task": "changemode",
  "token": "cdfb4c5717170c5e6f12e5b1643a2b67132bcc7d82bd6090e92a55cddd5950db7926f07dd201b6aa",
  "dbname": "demodb",
  "modify": "active",
  "force": "y"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| server_mode | the HA mode of the database server after the request: standby, maintenance or active |

## Response Sample

```
{
   "__EXEC_TIME" : "121 ms",
   "note" : "none",
   "server_mode" : "active",
   "status" : "success",
   "task" : "changemode"
}
```
