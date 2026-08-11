# gettriggerinfo

Get trigger information.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| dbname | database name |

## Request Sample

```
{
  "task": "gettriggerinfo",
  "token": "cdfb4c5717170c5ed30ef86644baf8151531ce5adff4a1f9a54711c51e0f50767926f07dd201b6aa",
  "dbname": "demodb"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| triggerinfo | the list of the triggers of the database |

### triggerinfo

triggerinfo is composed of `trigger` objects whose keys are the ones of
[addtrigger](addtrigger.md): name, conditiontime, eventtype, eventtarget, condition, action,
status and priority.

## Response Sample

```
{
   "__EXEC_TIME" : "42 ms",
   "note" : "none",
   "status" : "success",
   "task" : "gettriggerinfo",
   "triggerinfo" : [
      {
         "trigger" : [
            {
               "action" : "REJECT",
               "condition" : "1=1",
               "conditiontime" : "BEFORE",
               "eventtarget" : "history(score)",
               "eventtype" : "STATEMENT UPDATE",
               "name" : "example",
               "priority" : "0.00",
               "status" : "ACTIVE"
            }
         ]
      }
   ]
}
```
