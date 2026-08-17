# userinfo

Get database user information in CUBRID.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted |
| dbname | database name |

## Request Sample

```
{
  "task":"userinfo",
  "token":"cdfb4c5717170c5ed30ef86644baf8151531ce5adff4a1f9a54711c51e0f50767926f07dd201b6aa",
  "dbname":"demodb"
 }
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed |
| note | if failed, a brief description will be given here |
| dbname | database name |
| @name | user name |
| @id | user id number |
| user | user information list |
| groups | user group |
| authorization | user authorization |

## Response Sample

```
{
   "__EXEC_TIME" : "34 ms",
   "dbname" : "demodb",
   "note" : "none",
   "status" : "success",
   "task" : "userinfo",
   "user" : [
      {
         "@id" : "",
         "@name" : "INFORMATION_SCHEMA",
         "authorization" : [
            {
               "_db_attribute" : "1",
               "_db_auth" : "1",
               "_db_authorization" : "1",
               "_db_charset" : "1",
               "_db_class" : "1",
               "_db_collation" : "1",
               "_db_data_type" : "1",
               "_db_domain" : "1",
               "_db_ha_apply_info" : "1",
               "_db_index" : "1",
               "_db_index_key" : "1",
               "_db_meth_arg" : "1",
               "_db_meth_file" : "1",
               "_db_meth_sig" : "1",
               "_db_method" : "1",
               "_db_partition" : "1",
               "_db_query_spec" : "1",
               "_db_serial" : "1",
               "_db_server" : "1",
               "_db_stored_procedure" : "1",
               "_db_stored_procedure_args" : "1",
               "_db_stored_procedure_code" : "1",
               "_db_synonym" : "1",
               "_db_trigger" : "1",
               "_db_user" : "1",
               "db_root" : "1",
               "dual" : "1"
            }
         ],
         "groups" : [
            {
               "group" : [ "PUBLIC" ]
            }
         ]
      }
   ]
}
```

> Lists are shortened to 1 entry here; the real response returned up to 3.
