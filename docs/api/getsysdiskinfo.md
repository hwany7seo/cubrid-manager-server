# getsysdiskinfo

Get the size and the free space of the file systems of the host.
On Linux the root file system (`/`) is reported, on Windows every fixed drive is reported.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |

## Request Sample

```
{
  "task": "getsysdiskinfo",
  "token": "4504b930fc1be99bf5dfd31fc5799faaa3f117fb903f397de087cd3544165d857926f07dd201b6aa"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| disk_info | the list of the file systems |

### disk_info

disk_info is composed of objects with following structure

| **Key** | **Description** |
| --- | --- |
| name | the mount point on Linux, the drive letter on Windows |
| total_size | the total size of the file system, in bytes |
| free_size | the free space of the file system, in bytes |

## Response Sample

```
{
   "disk_info" : [
      {
         "free_size" : "467456258048",
         "name" : "/",
         "total_size" : "1832296755200"
      }
   ],
   "note" : "none",
   "status" : "success",
   "task" : "getsysdiskinfo"
}
```
