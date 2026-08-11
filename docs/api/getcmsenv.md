# getcmsenv

Get the CUBRID Manager server environment variables.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |


## Request Sample

```
{
 "task":"getcmsenv",
 "token":"4504b930fc1be99bf5dfd31fc5799faaa3f117fb903f397de087cd3544165d857926f07dd201b6aa"
 }
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| CMS_VER | the build number of CMS |
| CUBRIDVER | the version of the CUBRID engine |
| PLATFORM | the processor architecture of the host |
| cm_port | the port CMS listens on |
| is_default_cert | yes or no, the SSL certificate in use is still the default one shipped with CMS |

## Response Sample

```
{
   "__EXEC_TIME" : "6 ms",
   "CMS_VER" : "11.4.0.0001",
   "CUBRIDVER" : "11.4",
   "PLATFORM" : "x86_64",
   "cm_port" : "8003",
   "is_default_cert" : "yes",
   "note" : "none",
   "status" : "success",
   "task" : "getcmsenv"
}
```
