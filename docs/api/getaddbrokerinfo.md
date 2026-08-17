# getaddbrokerinfo

Get broker configurations from a cubrid_broker.conf file.

## Request JSON Syntax

| **Key**  | **Description**                |
| -------- | ------------------------------ |
| task     | task name                      |
| token    | token string encrypted.        |
| confname | name of the configuration file |

## Request Sample

```
{
  "task": "getaddbrokerinfo",
  "token": "cdfb4c5717170c5e237a227a2ceeccc6ae9e10c16754fb85371c0d74fa0d9d577926f07dd201b6aa",
  "confname": "brokerconf"
}
```

## Response JSON Syntax

| **Key**  | **Description**                                   |
| -------- | ------------------------------------------------- |
| conflist | content of the configuration file                 |
| confname | name of the configuration file. The server answers with the normalized name, so a request for `brokerconf` comes back as `broker` |
| note     | if failed, a brief description will be given here |
| status   | execution result, success or failed.              |
| task     | task name                                         |

## Response Sample

```
{
   "__EXEC_TIME" : "0 ms",
   "conflist" : [
      {
         "confdata" : [
            "[broker]",
            "MASTER_SHM_ID             =30001",
            "ADMIN_LOG_FILE            =/home/cubrid/CUBRID-11.5.0.2441-6ba9522-Linux.x86_64/log/broker/cubrid_broker.log"
         ]
      }
   ],
   "confname" : "broker",
   "note" : "none",
   "status" : "success",
   "task" : "getaddbrokerinfo"
}
```

> Lists are shortened to 3 entries here; the real response returned up to 56.
