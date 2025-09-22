# checkfile

## Request JSON Syntax

| **Key** | **Description**         |
| ------- | ----------------------- |
| task    | task name               |
| token   | token string encrypted. |

## Request Sample

```
{
    "task":"checkfile",
    "token": "<token>"
}

```

## Response JSON Syntax

| **Key** | **Description**                                   |
| ------- | ------------------------------------------------- |
| note    | if failed, a brief description will be given here |
| status  | execution result, success or failed.              |
| task    | task name                                         |

## Response Sample

```
{
   "__EXEC_TIME" : "0 ms",
   "note" : "none",
   "status" : "success",
   "task" : "checkfile"
}
```
