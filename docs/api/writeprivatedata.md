# writeprivatedata

Write a file of the `$CUBRID/log/manager` directory. Every element of `confdata` is written as
one line and the previous contents of the file are overwritten. The file is read back with
[readprivatedata](readprivatedata.md).

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| confname | the name of the file, relative to `$CUBRID/log/manager` |
| confdata | the lines to be written |

## Request Sample

```
{
  "task": "writeprivatedata",
  "token": "4504b930fc1be99bf5dfd31fc5799faaa3f117fb903f397de087cd3544165d857926f07dd201b6aa",
  "confname": "query_editor.dat",
  "confdata": [
    "select * from code",
    "select * from athlete"
  ]
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |

## Response Sample

```
{
  "task": "writeprivatedata",
  "status": "success",
  "note": "none"
}
```
