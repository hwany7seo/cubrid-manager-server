# getallsysparam

Get configuration files.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| confname | cubridconf, cmconf, haconf, databases |

## Request Sample

```
{
  "task": "getallsysparam",
  "token": "cdfb4c5717170c5e237a227a2ceeccc6ae9e10c16754fb85371c0d74fa0d9d577926f07dd201b6aa",
  "confname": "cubridconf"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| note | if failed, a brief description will be given here |
| status | execution result, success or failed. |
| task | task name |
| confname | name of the configuration file |
| conflist | list of configuration file data |

### conflist
conflist is composed of objects with following structure

| **Key** | **Description** |
| --- | --- |
| confdata | content of configuration file |

## Response Sample

```json
{
   "__EXEC_TIME" : "1 ms",
   "conflist" : [
      {
         "confdata" : [
            "#",
            "#  Copyright 2008 Search Solution Corporation",
            "#  Copyright 2016 CUBRID Corporation"
         ]
      }
   ],
   "confname" : "cubridconf",
   "note" : "none",
   "status" : "success",
   "task" : "getallsysparam"
}
```

> Lists are shortened to 3 entries here; the real response returned up to 75.
