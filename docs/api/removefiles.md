# removefiles

Delete temporary files located in the `$CUBRID/tmp` directory.

Only file names are accepted, not paths: a name that is shorter than three characters or
that contains `..`, `/` or `\` is rejected. Each name must start with the `+T` prefix,
which stands for the `$CUBRID/tmp` directory, so `+Ttest.err` removes `$CUBRID/tmp/test.err`.
Removing a file that does not exist is not treated as an error.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| files | the list of the files to be removed |

### files

files is composed of objects with following structure

| **Key** | **Description** |
| --- | --- |
| path | the name of a file in `$CUBRID/tmp`, prefixed with `+T` |

## Request Sample

```
{
  "task": "removefiles",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa",
  "files": [
    {
      "path": "+Ttest.err"
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
   "__EXEC_TIME" : "2 ms",
   "note" : "none",
   "status" : "success",
   "task" : "removefiles"
}
```
