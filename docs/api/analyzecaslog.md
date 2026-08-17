# analyzecaslog

The analyzecaslog interface will fetch a top list to parse broker SQL log(s) with the broker_log_top utility.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| logfilelist | the list of the broker SQL log files to be analyzed. Every element is an object which holds a `logfile` key |
| logfile | the full path of a broker SQL log file |
| option_t | yes or no, analyze the log by transaction |

## Request Sample

```
{
  "task": "analyzecaslog",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa",
  "logfilelist": [
    {
      "logfile": "$CUBRID/log/broker/sql_log/query_editor_1.sql.log"
    }
  ],
  "option_t": "yes"
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| resultlist | the list of the analysis results, one entry per query |
| resultfile | the full path of the temporary file which holds the analysis result. It is passed as the `filename` of [getcaslogtopresult](getcaslogtopresult.md) to read the query text of an entry |

### resultlist

resultlist is composed of `result` objects. The keys of a `result` object depend on `option_t`.

When `option_t` is `yes` (analysis by transaction):

| **Key** | **Description** |
| --- | --- |
| qindex | the query index, such as `[Q1]` |
| exec_time | the elapsed time of the transaction |

Otherwise (analysis by query):

| **Key** | **Description** |
| --- | --- |
| qindex | the query index, such as `[Q1]` |
| max | the maximum execution time of the query |
| min | the minimum execution time of the query |
| avg | the average execution time of the query |
| cnt | the number of times the query was executed |
| err | the number of executions which ended with an error |

## Response Sample

```
{
   "__EXEC_TIME" : "23 ms",
   "note" : "none",
   "resultfile" : "/home/cubrid/CUBRID-11.5.0.2441-6ba9522-Linux.x86_64/tmp/analyzelog_res_141_1787006473_176380_129",
   "resultlist" : null,
   "status" : "success",
   "task" : "analyzecaslog"
}
```
