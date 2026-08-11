# runscript

Run a script file (`*.sh` on Linux, `*.bat` on Windows) on the host of CMS.
The script path must be accessible by CMS. The standard output and the standard error of the
script are written to temporary files which are removed when the script ends, so the output of
the script is not returned to the client.

Environment variables can be passed with the `envvar` key, in the `NAME=VALUE` form.
For security reasons only `LANG`, `TZ` and `CUBRID_TMP` are allowed, any other name makes the
request fail.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| script_path | the full path of the script to be run |
| envvar | an environment variable in the `NAME=VALUE` form, it can be given several times. Only `LANG`, `TZ` and `CUBRID_TMP` are permitted |

## Request Sample

```
{
  "task": "runscript",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa",
  "script_path": "$CUBRID/scripts/collect_stat.sh",
  "envvar": "LANG=en_US.utf8"
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
   "__EXEC_TIME" : "84 ms",
   "note" : "none",
   "status" : "success",
   "task" : "runscript"
}
```
