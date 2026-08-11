# readprivatedata

Read a file of the `$CUBRID/log/manager` directory line by line. It is used by the client to
keep its own data, such as the query editor history, on the host of CMS.
The file is written with [writeprivatedata](writeprivatedata.md).

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| confname | the name of the file, relative to `$CUBRID/log/manager` |

## Request Sample

```
{
  "task": "readprivatedata",
  "token": "4504b930fc1be99bf5dfd31fc5799faaa3f117fb903f397de087cd3544165d857926f07dd201b6aa",
  "confname": "query_editor.dat"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| confdata | the lines of the file |

## Response Sample

```
{
  "task": "readprivatedata",
  "confdata": [
    "select * from code",
    "select * from athlete"
  ],
  "status": "success",
  "note": "none"
}
```
