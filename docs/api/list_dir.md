# list_dir

Get the sub directories and the files of a directory. The `path` is interpreted as a path
relative to the `$CUBRID` directory, and it must not contain `..`.
The password files, `cm.pass` and `cmdb.pass`, and the hidden files are never listed.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| path | the directory to be listed, relative to `$CUBRID` |

## Request Sample

```
{
  "task": "list_dir",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa",
  "path": "conf"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| path | the requested directory, a slash is appended to it |
| dir | the list of the sub directories |
| file | the list of the files |

### dir, file

dir and file are composed of objects with following structure

| **Key** | **Description** |
| --- | --- |
| group | the name of a sub directory or of a file |

## Response Sample

```
{
   "__EXEC_TIME" : "3 ms",
   "dir" : [
      {
         "group" : "backup"
      }
   ],
   "file" : [
      {
         "group" : "cubrid.conf"
      },
      {
         "group" : "cubrid_broker.conf"
      },
      {
         "group" : "cm.conf"
      }
   ],
   "note" : "none",
   "path" : "conf/",
   "status" : "success",
   "task" : "list_dir"
}
```
