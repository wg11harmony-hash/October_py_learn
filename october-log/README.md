# Python日志统计工具学习项目

本目录对应2026年10月剩余计划中的日志项目v0.1。源码和测试文件目前是待填写的练习模板；三份样例已准备好。先从文件读取和单行解析开始，再完成统计、JSON、命令行和测试。

## 目录

```text
october-log/
├── log_tool.py
├── samples/
│   ├── valid.log
│   ├── mixed.log
│   └── empty.log
├── tests/
│   └── test_log_tool.py
├── docs/
├── README.md
└── .gitignore
```

统计报告保存为项目根目录的report.json，程序运行日志保存为tool_run.log。月底HTTP实验统一放在上一级的03_HTTP练习中，学到该任务时再创建public网页目录。

## 样例格式

```text
2026-10-13T10:00:00 192.0.2.10 GET /login 200
```

依次为时间、IP、方法、路径、状态码。先strip再split()；字段须恰好5个。状态码须为三位ASCII数字，范围100至599；路径须以/开头。时间、IP、方法先保留文本，不做语义校验。查询参数保留在路径中。

- 空白行返回None。
- 坏行由解析函数抛ValueError，上层记录行号与原因。
- 有效行才参与IP、路径和状态码频次统计。
- 状态码校验时为整数，统计映射的键统一为字符串。
- Top按次数降序，平局按原键字符串升序。

## 三份样例的预期结果

| 文件 | 总物理行 | 有效 | 坏行 | 空白 | 不同IP |
| --- | ---: | ---: | ---: | ---: | ---: |
| valid.log | 7 | 7 | 0 | 0 | 3 |
| mixed.log | 13 | 7 | 4 | 2 | 3 |
| empty.log | 0 | 0 | 0 | 0 | 0 |

valid.log与mixed.log具有相同的有效记录。mixed.log第8行为空，第13行仅含空格；第9行少字段，第10行状态码abc，第11行状态码700，第12行多字段。所有13行均有结束换行。empty.log是零字节文件。

有效记录频次：

- IP：192.0.2.10为3；192.0.2.20为3；198.51.100.30为1。
- 状态码：200为3；401为1；404为2；500为1。
- 路径：/login为3；/admin、/health、/missing、/search?q=python各1。
- 路径Top 5：/login、/admin、/health、/missing、/search?q=python。

每次核对：总行数等于有效加坏行加空白；三类频次各自的总和等于有效行数。不同IP数量不等于访问人数。

## 建议学习顺序

1. 在log_tool.py中用with open或Path.open逐行读取mixed.log，打印行号。
2. 实现parse_line，分别检查正常、空白、少字段和非法状态码。
3. 实现analyze_lines与top_items，对照上面的手工答案。
4. 加入JSON导出和命令行，完成文件缺失、编码和写出错误处理。
5. 在tests/test_log_tool.py中编写至少8条有意义的测试。
6. 在docs/记录字段说明、调试、集成检查和复现结果。

## 后续运行方式

在项目根目录创建自己的虚拟环境：

```text
python -m venv .venv
```

实现统计工具和命令行后运行：

```text
.venv\Scripts\python.exe log_tool.py samples/mixed.log --output report.json --top 5
.venv\Scripts\python.exe log_tool.py --help
```

编写实际测试方法后运行：

```text
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

当前练习模板没有统计实现和测试方法。完成后再以上述命令验收；核心项目只使用标准库，无需安装第三方依赖。

## Git与文件约定

源码、测试、README和samples中的.log文件保留在版本控制中。虚拟环境、缓存、report.json及tool_run.log由.gitignore忽略。输入输出不要指向同一个文件。
