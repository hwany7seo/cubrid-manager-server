# updateattribute

Update the attribute definition of a class. The database must be running, and the database
user information registered by [dbmtuserlogin](dbmtuserlogin.md) is used to connect to it.

The attribute definition follows the same structure as the one returned by the
[class](class.md) interface.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| dbname | database name |
| classname | the name of the class whose attribute is updated |

## Request Sample

```
{
  "task": "updateattribute",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa",
  "dbname": "demodb",
  "classname": "athlete"
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
   "__EXEC_TIME" : "26 ms",
   "note" : "none",
   "status" : "success",
   "task" : "updateattribute"
}
```
