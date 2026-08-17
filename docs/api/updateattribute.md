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
| classinfo | the class after the update, in the form [classinfo](classinfo.md) returns it |

## Response Sample

```
{
   "__EXEC_TIME" : "27 ms",
   "classinfo" : [
      {
         "attribute" : [
            {
               "default" : "",
               "indexed" : "y",
               "inherit" : "public.athlete",
               "name" : "code",
               "notnull" : "y",
               "shared" : "n",
               "type" : "integer(10)",
               "unique" : "y"
            },
            {
               "default" : "",
               "indexed" : "n",
               "inherit" : "public.athlete",
               "name" : "name",
               "notnull" : "y",
               "shared" : "n",
               "type" : "character varying(40)",
               "unique" : "n"
            }
         ],
         "classname" : "public.athlete",
         "constraint" : [
            {
               "attribute" : [ "code" ],
               "name" : "pk_athlete_code",
               "type" : "PRIMARY KEY"
            },
            {
               "attribute" : [ "code" ],
               "name" : "n_athlete_code",
               "type" : "NOT NULL"
            }
         ],
         "dbname" : "demodb",
         "owner" : "PUBLIC",
         "type" : "user",
         "virtual" : "normal"
      }
   ],
   "note" : "none",
   "status" : "success",
   "task" : "updateattribute"
}
```

> Lists are shortened to 2 entries here; the real response returned up to 5.
