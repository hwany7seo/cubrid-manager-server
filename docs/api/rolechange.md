# rolechange

Change a role of instance in HA.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |

## Request Sample

```
{
  "task": "rolechange",
  "token": "cdfb4c5717170c5e4e44dd87fc920466e9afaa2d6744dab135d4017831048f927926f07dd201b6aa"
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
   "__EXEC_TIME" : "12 ms",
   "note" : "none",
   "status" : "success",
   "task" : "rolechange"
}
```
