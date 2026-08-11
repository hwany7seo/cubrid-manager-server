# writeandsaveconf

Write a configuration file. If the file already exists it is first copied to
`<confpath>.bak`, then it is overwritten with the lines given in `confdata`.
Every element of `confdata` is written as one line.

## Request JSON Syntax

| **Key** | **Description** |
| --- | --- |
| task | task name |
| token | token string encrypted. |
| confpath | the full path of the configuration file to be written |
| confdata | the lines of the configuration file |

## Request Sample

```
{
  "task": "writeandsaveconf",
  "token": "cdfb4c5717170c5e9c6856b4d1c61ee8132bcc7d82bd609066ed9ece2554c47f7926f07dd201b6aa",
  "confpath": "$CUBRID/conf/cubrid.conf",
  "confdata": [
    "[service]",
    "service=server,broker,manager",
    "",
    "[common]",
    "data_buffer_size=512M"
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
   "__EXEC_TIME" : "7 ms",
   "note" : "none",
   "status" : "success",
   "task" : "writeandsaveconf"
}
```
