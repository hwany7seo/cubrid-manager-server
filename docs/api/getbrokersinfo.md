# getbrokersinfo

Get information of brokers.

## Request JSON syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |

## Request Sample

```
    {
        "task":"getbrokersinfo",        "token":"300ea42877b8fd414644196bb44e7a8bea3164a1a5a348c5381b47766536a56664ec74a35eeb28dd7926f07dd201b6aa7926f07dd201b6aa7926f07dd201b6aa7926f07dd201b6aa7926f07dd201b6aa7926f07dd201b6aa7926f07dd201b6aa7926f07dd201b6aa7926f07dd201b6aa7926f07dd201b6aa7926f07dd201b6aa"
    }
```


## Response JSON Syntax


| **Key** | **Description** |
| --- | --- |
| brokersinfo | list of broker info |
| brokerstatus | status of broker service. |
| note | if failed, a brief description will be given here |
| status | execution result, success or failed. |
| task | task name |


### Brokers Info

| **Key** | **Description** |
| --- | --- |
| broker | list of brokers |

#### Broker

| **Key** | **Description** |
| --- | --- |
| access_list | |
| appl_server_shm_id | server shared memory id |
| name | name of the broker |
| port | port number |
| source_env | |
| state | state of the broker |
| type | type |



## Response Sample

```

    {
    "__EXEC_TIME" : "2 ms",
    "brokersinfo" : [
        {
            "broker" : [
                {
                "access_list" : "0",
                "appl_server_shm_id" : "30000",
                "name" : "query_editor",
                "port" : "30000",
                "source_env" : "0",
                "state" : "OFF",
                "type" : "CAS"
                },
                {
                "access_list" : "0",
                "appl_server_shm_id" : "33120",
                "name" : "broker1",
                "port" : "33120",
                "source_env" : "0",
                "state" : "OFF",
                "type" : "CAS"
                }
            ]
        }
    ],
    "brokerstatus" : "ON",
    "note" : "none",
    "status" : "success",
    "task" : "getbrokersinfo"
    }

```