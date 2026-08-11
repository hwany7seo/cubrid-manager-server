# runsqlstatement

Execute an SQL statement with the `csql` utility. The statement can be given inline with the
`command` key, or read from a file with the `infile` key. The database is accessed in CS mode
when it is running, and in SA mode when it is stopped.

The output of `csql` is not returned to the client. When `csql` reports an error, the request
fails and the error message is returned in the `note` key.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| dbname | database name |
| command | the SQL statement to be executed |
| infile | the full path of a file which contains the SQL statements to be executed |
| uid | database user id |
| passwd | the password of the database user |
| error_continue | y or n, continue the execution when an error occurs |

## Request Sample

```
{
  "task": "runsqlstatement",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa",
  "dbname": "demodb",
  "command": "select * from code",
  "uid": "dba",
  "passwd": "",
  "error_continue": "y"
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
   "__EXEC_TIME" : "213 ms",
   "note" : "none",
   "status" : "success",
   "task" : "runsqlstatement"
}
```
