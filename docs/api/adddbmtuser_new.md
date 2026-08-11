# adddbmtuser_new

Add a CM/CWM user. It is the extended version of [adddbmtuser](adddbmtuser.md): the authorities
are given as a structured `authoritylist` instead of the single `casauth`, `dbcreate` and
`statusmonitorauth` keys.

`targetid`, `password`, `authoritylist` and `dbauth` are all required. The user information is
read back with [getdbmtuserinfo_new](getdbmtuserinfo_new.md).

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| targetid | the id of the CM user to be added |
| password | the password of the CM user |
| authoritylist | the authorities granted to the CM user |
| dbauth | the databases the CM user takes in charge of |

### authoritylist

| **Key** | **Description** |
| --- | --- |
| dbc | yes or no, database creation authority |
| dbo | yes or no, database operation authority |
| brk | yes or no, broker authority |
| mon | yes or no, monitoring authority |
| job | yes or no, automation authority |
| var | yes or no, show variable authority |

### dbauth

dbauth is composed of objects with following structure

| **Key** | **Description** |
| --- | --- |
| dbname | database name |
| dbid | the database user id used to connect to that database |
| dbpassword | the password of that database user |
| dbbrokeraddress | the address of the broker used to connect to that database, in the `<ip>,<port>` form |

## Request Sample

```
{
  "task": "adddbmtuser_new",
  "token": "4504b930fc1be99bf5dfd31fc5799faaa3f117fb903f397de087cd3544165d857926f07dd201b6aa",
  "targetid": "cmuser1",
  "password": "cmuser1pwd",
  "authoritylist": {
    "dbc": "no",
    "dbo": "yes",
    "brk": "yes",
    "mon": "no",
    "job": "no",
    "var": "no"
  },
  "dbauth": [
    {
      "dbname": "demodb",
      "dbid": "dba",
      "dbpassword": "",
      "dbbrokeraddress": "localhost,30000"
    }
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
  "task": "adddbmtuser_new",
  "status": "success",
  "note": "none"
}
```
