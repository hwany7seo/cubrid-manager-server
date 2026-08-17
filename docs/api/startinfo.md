# startinfo

Get information about all databases and their active status.

## Request JSON Syntax


| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |


## Request Sample

```
{
  "task":"startinfo",
  "token":"4504b930fc1be99bf5dfd31fc5799faaa3f117fb903f397de087cd3544165d857926f07dd201b6aa"
}
```

## Response JSON Syntax


| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| dblist | the whole databases in the cubrid, including its name and path.  |
| activelist | get the database's name in active status. |

### activelist

activelist is composed of objects with following structure

| **Key** | **Description** |
| --- | --- |
| active | list of dbname |


## Response Sample

```
{
   "__EXEC_TIME" : "22 ms",
   "activelist" : [
      {
         "active" : [
            {
               "dbname" : "demodb"
            }
         ]
      }
   ],
   "dblist" : [
      {
         "dbs" : [
            {
               "dbdir" : "/home/cubrid/CUBRID-11.5.0.2441-6ba9522-Linux.x86_64/databases/destinationdb",
               "dbname" : "destinationdb"
            },
            {
               "dbdir" : "/home/cubrid/CUBRID-11.5.0.2441-6ba9522-Linux.x86_64/databases/alatestdb",
               "dbname" : "alatestdb"
            },
            {
               "dbdir" : "/home/cubrid/CUBRID-11.5.0.2441-6ba9522-Linux.x86_64/databases/demodb",
               "dbname" : "demodb"
            }
         ]
      }
   ],
   "note" : "none",
   "status" : "success",
   "task" : "startinfo"
}
```
