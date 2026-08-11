# getshardstatus

Get the status of the application servers of one shard broker by running
`cubrid shard status <shardname>`.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| shardname | the name of the shard broker |

## Request Sample

```
{
  "task": "getshardstatus",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa",
  "shardname": "shard1"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| name | the name of the shard broker given in the request |
| shard | the list of the application servers of the shard broker |

### shard

shard is composed of objects with following structure

| **Key** | **Description** |
| --- | --- |
| proxy_id | the id of the proxy |
| shard_id | the id of the shard |
| cas_id | the id of the application server |
| pid | the process id of the application server |
| qps | queries per second |
| lqs | long queries per second |
| psize | the size of the process, in KB |
| status | the status of the application server, such as IDLE or BUSY |

## Response Sample

```
{
   "__EXEC_TIME" : "44 ms",
   "name" : "shard1",
   "note" : "none",
   "shard" : [
      {
         "cas_id" : "1",
         "lqs" : "0",
         "pid" : "18240",
         "proxy_id" : "1",
         "psize" : "51360",
         "qps" : "0",
         "shard_id" : "0",
         "status" : "IDLE"
      }
   ],
   "status" : "success",
   "task" : "getshardstatus"
}
```
