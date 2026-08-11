# getinitbrokersinfo

Get information of brokers. It is executed by the same handler as
[getbrokersinfo](getbrokersinfo.md) and it returns the same response; it is provided as a
separate task name so that a client can distinguish the first call, made when the connection to
CMS is initialized, from the calls made later to refresh the broker list.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| bname | broker name. When it is omitted, every broker is returned |

## Request Sample

```
{
  "task": "getinitbrokersinfo",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| brokersinfo | list of broker info |
| brokerstatus | status of broker service, ON or OFF |

See [getbrokersinfo](getbrokersinfo.md) for the description of the broker items.

## Response Sample

```
{
   "__EXEC_TIME" : "12 ms",
   "brokersinfo" : [
      {
         "broker" : [
            {
               "access_list" : "0",
               "appl_server_shm_id" : "30000",
               "name" : "query_editor",
               "port" : "30000",
               "source_env" : "0"
            }
         ]
      }
   ],
   "brokerstatus" : "OFF",
   "note" : "none",
   "status" : "success",
   "task" : "getinitbrokersinfo"
}
```
