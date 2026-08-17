# getstatustemplate

Get the monitoring status templates. When `name` is given, only that template is returned,
otherwise every template of the configuration file is returned. When the configuration file
does not exist, the request succeeds and returns no template.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| name | the name of the status template. When it is omitted, every template is returned |

## Request Sample

```
{
  "task": "getstatustemplate",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| templatelist | the list of the status templates |

### templatelist

templatelist is composed of objects with following structure

| **Key** | **Description** |
| --- | --- |
| name | the name of the status template |
| desc | the description of the status template |
| db_name | the name of the database which is monitored |
| sampling_term | the sampling interval, in seconds |
| target_config | the monitoring items of the template. The key is the name of the monitoring item, its color and its magnification are returned as the values of that key |

## Response Sample

```
{
   "__EXEC_TIME" : "0 ms",
   "note" : "none",
   "status" : "success",
   "task" : "getstatustemplate",
   "templatelist" : [
      {
         "template" : [
            {
               "cas_st_active_session" : "0.1",
               "cas_st_request" : "0.1",
               "cas_st_transaction" : "0.1",
               "close" : "target_config",
               "db_name" : " ",
               "desc" : "status monitor template of broker",
               "name" : "broker_template",
               "sampling_term" : "1"
            },
            {
               "_PROGNAME" : "ager",
               "close" : "target_config",
               "db_name" : "demodb",
               "desc" : "status monitor template of demodb",
               "name" : "dbserver_clier_requet",
               "sampling_term" : "1",
               "server_conn_cli_request" : "1",
               "task" : "tatustemplate",
               "token" : "a91333c783363ed09353f515b95f07f"
            }
         ]
      }
   ]
}
```
