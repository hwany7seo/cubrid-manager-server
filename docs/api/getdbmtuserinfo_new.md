# getdbmtuserinfo_new

Get CM/CWM user information

## Request Json Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |

## Request Sample

```
{
  "task": "getdbmtuserinfo_new",
  "token": "4504b930fc1be99bf5dfd31fc5799faaa3f117fb903f397de087cd3544165d857926f07dd201b6aa"
}
```

## Response Json Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| dblist | a list of databases which is taken in charge by this user |
| dbname | database name |
| userlist | the list path |
| user | user information list |
| id | user name |
| auth_info | authority information |
| dbid | database dba id |
| dbbrokerport | broker port |
| user_auth | a value indicating user authorities |
| authority_list | the authorities granted to this user, including dbo,brk,mon,job,var,dbc and admin |

## Response Sample

```
{
   "dblist" : 
      {
         "dbs" : [
            {
               "dbname" : "demodb"
            }
      }
   ],
   "note" : "none",
   "status" : "success",
   "task" : "adddbmtuser_new",
   "userlist" : 
      {
         "user" : [
            {
               "@id" : "admin",
               "authority_list" : [ null ,
               "dbauth" : 
                  {
                     "auth_info" : [
                        {
                           "@dbid" : "dba",
                           "dbbrokeraddress" : "10.34.135.62,30000",
                           "dbname" : "demodb"
                        }
                  }
               ],
               "user_auth" : "admin"
            },
            {
               "@id" : "hqy_admin225",
               "authority_list" : 
                  {
                     "brk" : "yes",
                     "dbc" : "no",
                     "dbo" : "yes",
                     "job" : "no",
                     "mon" : "no",
                     "var" : "no"
                  }
               ,
               "dbauth" : 
                  {
                     "auth_info" : [
                        {
                           "@dbid" : "dba",
                           "dbbrokeraddress" : "localhost, 33000",
                           "dbname" : "db_3"
                        },
                        {
                           "@dbid" : "dba",
                           "dbbrokeraddress" : "localhost, 33000",
                           "dbname" : "db_5"
                        }
                  }
               ],
               "user_auth" : "6"
            }
         ]
      }
   ]
}
```
