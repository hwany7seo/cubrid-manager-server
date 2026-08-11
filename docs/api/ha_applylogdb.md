# ha_applylogdb

Start or stop the `applylogdb` process of an HA group by running
`cubrid heartbeat applylogdb <start|stop> <dbname> <peer_node>`.

The request fails with a request format error when `on_off` is neither `start` nor `stop`.
The output of the utility is not returned to the client, use [ha_status](ha_status.md) to check
the result.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| dbname | database name |
| on_off | start or stop |
| peer_node | the host name of the peer node of the HA group |

## Request Sample

```
{
  "task": "ha_applylogdb",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa",
  "dbname": "demodb",
  "on_off": "start",
  "peer_node": "node2"
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
   "__EXEC_TIME" : "56 ms",
   "note" : "none",
   "status" : "success",
   "task" : "ha_applylogdb"
}
```
