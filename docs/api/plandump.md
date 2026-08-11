# plandump

Run plandump utility.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| dbname | database name |
| plandrop | y : drop plans |

## Request Sample

```
{
  "task": "plandump",
  "token": "cdfb4c5717170c5e2d40a680732333064610bcfeec1c0d870c43c1586a92dd1f7926f07dd201b6aa",
  "dbname": "demodb",
  "plandrop": "y"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| log | the lines of the query plan cache of the database server |

## Response Sample

```
{
   "__EXEC_TIME" : "37 ms",
   "log" : [
      {
         "line" : "Query Plan Cache Information"
      },
      {
         "line" : "Max_entries:1000 Num_entries:12"
      }
   ],
   "note" : "none",
   "status" : "success",
   "task" : "plandump"
}
```
