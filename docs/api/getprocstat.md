# getprocstat

Get the CPU and the memory usage of a process of the host.
When `pid` is omitted, the statistics of the CMS process itself are returned.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| pid | the id of the process. It is optional, the CMS process is used by default |

## Request Sample

```
{
  "task": "getprocstat",
  "token": "4504b930fc1be99bf5dfd31fc5799faaa3f117fb903f397de087cd3544165d857926f07dd201b6aa",
  "pid": 24513
}
```

## Response JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| status | execution result, success or failed. |
| note | if failed, a brief description will be given here |
| pid | the id of the process |
| cpu_kernel | the cpu time the process spent in kernel mode |
| cpu_user | the cpu time the process spent in user mode |
| mem_physical | the physical memory the process uses |
| mem_virtual | the virtual memory the process uses |

## Response Sample

```
{
   "cpu_kernel" : 4,
   "cpu_user" : 3,
   "mem_physical" : 13299712,
   "mem_virtual" : 613793792,
   "note" : "none",
   "pid" : 1873795,
   "status" : "success",
   "task" : "getprocstat"
}
```
