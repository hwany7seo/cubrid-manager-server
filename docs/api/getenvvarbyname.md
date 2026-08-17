# getenvvarbyname

Get the value of the environment variables of the CMS process. Every `envvar` value of the
request is looked up and returned as a key of the response. A variable which is not set is
returned with an empty value.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| envvar | the name of an environment variable, it can be given several times |

## Request Sample

```
{
  "task": "getenvvarbyname",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa",
  "envvar": "CUBRID"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| <envvar> | the value of the requested environment variable, the key is the variable name itself |

## Response Sample

```
{
   "CUBRID" : "/home/cubrid/CUBRID-11.5.0.2441-6ba9522-Linux.x86_64",
   "__EXEC_TIME" : "0 ms",
   "note" : "none",
   "status" : "success",
   "task" : "getenvvarbyname"
}
```
