# copyfolder

Copy a folder and its contents to another location. Both paths must be accessible by CMS.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| srcdir | the full path of the source folder |
| destdir | the full path of the destination folder |

## Request Sample

```
{
  "task": "copyfolder",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa",
  "srcdir": "$CUBRID_DATABASES/demodb",
  "destdir": "$CUBRID_DATABASES/demodb_bak"
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
   "__EXEC_TIME" : "112 ms",
   "note" : "none",
   "status" : "success",
   "task" : "copyfolder"
}
```
