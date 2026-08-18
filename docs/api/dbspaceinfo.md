# dbspaceinfo

Get specified database space information.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted |
| dbname | database name |

## Request Sample

```
{
  "task":"dbspaceinfo",
  "token":"cdfb4c5717170c5e237a227a2ceeccc6ae9e10c16754fb85371c0d74fa0d9d577926f07dd201b6aa",
  "dbname":"alatestdb"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| note | if failed, a brief description will be given here |
| status | execution result, success or failed. |
| task | task name |
| dbinfo | list of information about storage volume |
| dbname | name of database |
| fileinfo | |
| freespace | size of available space |
| logpagesize | size of log page |
| pagesize | size of each page |
| spaceinfo | list of information about space of volumes |

### dbinfo
dbinfo is composed of objects with following structure 

| **Key** | **Description** |
| --- | --- |
| free_size | size of available space |
| purpose | purpose of the volume |
| total_size | total size of the volume |
| type | type of the volume | 
| used_size | size of the used space |
| volume_count | number of the volume |

### fileinfo
fileinfo is composed of objects with following structure 

| **Key** | **Description** |
| --- | --- |
| data_type | data type |
| file_count | number of the files |
| file_table_size | size of file_table |
| reserved_size | size of reserved space |
| total_size | total size of the file |
| used_size | used size of the file |


### spaceinfo
spaceinfo is composed of objects with following structure

| **Key** | **Description** |
| --- | --- |
| data | creation date of volume | 
| freepage | the total of avaliable pages |
| location | path of volume file |
| purpose | purpose of the volume |
| spacename | name of the volume |
| totalpage | number of total pages |
| type | type of the volume |
| usedpage | number of used page |
| volid | id of the volume |


## Response Sample

```
{
   "__EXEC_TIME" : "57 ms",
   "dbinfo" : [
      {
         "free_size" : "15616",
         "purpose" : "PERMANENT",
         "total_size" : "20480",
         "type" : "PERMANENT",
         "used_size" : "4864",
         "volume_count" : "3"
      }
   ],
   "dbname" : "alatestdb",
   "fileinfo" : [
      {
         "data_type" : "INDEX",
         "file_count" : "30",
         "file_table_size" : "30",
         "reserved_size" : "1828",
         "total_size" : "1920",
         "used_size" : "62"
      }
   ],
   "freespace" : "445676",
   "logpagesize" : "4096",
   "note" : "none",
   "pagesize" : "4096",
   "spaceinfo" : [
      {
         "date" : "20260818",
         "freepage" : "7552",
         "location" : "/home/cubrid/CUBRID-11.5.0.2441-6ba9522-Linux.x86_64/databases/alatestdb/alatestdb",
         "purpose" : "PERMANENT",
         "spacename" : "/home/cubrid/CUBRID-11.5.0.2441-6ba9522-Linux.x86_64/databases/alatestdb/alatestdb",
         "totalpage" : "12288",
         "type" : "PERMANENT",
         "usedpage" : "4736",
         "volid" : "0"
      }
   ],
   "status" : "success",
   "task" : "dbspaceinfo"
}
```

> Lists are shortened to 1 entry here; the real response returned up to 5.
