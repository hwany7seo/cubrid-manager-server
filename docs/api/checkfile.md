# checkfile

## Request JSON Syntax

| **Key** | **Description**         |
| ------- | ----------------------- |
| task    | task name               |
| token   | token string encrypted. |

## Request Sample

```
{
    "task":"checkfile",
    "token": "<token>"
}

```

## Response JSON Syntax

| **Key** | **Description**                                   |
| ------- | ------------------------------------------------- |
| note    | if failed, a brief description will be given here |
| status  | execution result, success or failed.              |
| task    | task name                                         |
| existfile | a file of the request which exists. It is returned once per existing file |

## Response Sample

```
{
   "__EXEC_TIME" : "0 ms",
   "existfile" : "/home/cubrid/CUBRID-11.5.0.2405-a2c3e03-Linux.x86_64/log/manager/cub_manager.log",
   "note" : "none",
   "status" : "success",
   "task" : "checkfile"
}
```
