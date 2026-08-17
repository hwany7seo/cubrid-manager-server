# getfolderswithkeyword

Get the sub folders of a folder. On Linux the `keyword` is matched as a sub string of the
folder name, on Windows it is used as a file search pattern, so wildcards such as `*` can be used.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| search_folder | the full path of the folder to be searched |
| keyword | the keyword the sub folder name must contain |

## Request Sample

```
{
  "task": "getfolderswithkeyword",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa",
  "search_folder": "$CUBRID_DATABASES",
  "keyword": "demo"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| folders | the list of the matched folders |

### folders

folders is composed of objects with following structure

| **Key** | **Description** |
| --- | --- |
| foldername | the name of a matched folder |

## Response Sample

```
{
   "__EXEC_TIME" : "0 ms",
   "folders" : null,
   "note" : "none",
   "status" : "success",
   "task" : "getfolderswithkeyword"
}
```
