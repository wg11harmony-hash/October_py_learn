# Python离线日志统计工具

使用Python标准库实现的命令行学习项目：读取约定格式的离线日志，统计行数、IP、路径和状态码频次，生成Top列表，并导出完整JSON报告。

当前为学习开发版。功能和测试状态以实际运行结果为准，完整v0.1验收还包括新目录复现和独立讲解。

## 1. 环境与依赖

- 已验证环境：Windows、PowerShell、Python 3.14.7。
- 仅使用Python标准库，无需安装第三方依赖。
- 输入日志使用UTF-8编码，JSON报告使用UTF-8编码。
- 以下快速运行命令以本机项目目录 `E:\octoeber_learn\october-log` 为例；复制到其他目录后替换对应路径。

## 2. 项目目录

```text
october-log/
├── log_tool.py                 # 正式工具源码
├── samples/
│   ├── valid.log               # 7条有效记录
│   ├── mixed.log               # 有效、坏行和空白混合，共13行
│   └── empty.log               # 零字节空文件
├── tests/
│   └── test_log_tool.py        # 8条核心自动测试
├── docs/                      # 学习、验收与复现记录
├── README.md                  # 本说明
└── .gitignore
```

运行后可能出现 `.venv`、`__pycache__` 和 `report_*.json` 等本地文件。`samples/invalid_utf8_test.log` 是解码失败实验的辅助文件，不属于三份基准日志。

## 3. 快速运行

先进入项目目录：

```powershell
cd E:\octoeber_learn\october-log
```

如果没有虚拟环境，先创建一次；已有 `.venv` 时无需重复创建：

```powershell
python -m venv .venv
```

直接使用虚拟环境解释器，不要求先激活环境：

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe log_tool.py --help
.\.venv\Scripts\python.exe log_tool.py samples/mixed.log --output report_mixed.json --top 3
```

预期控制台显示的四类行数：

```text
总行数： 13
有效行： 7
坏行： 4
空白行： 2
```

同时显示Top IP和Top路径。报告写入当前工作目录中的 `report_mixed.json`。在以上示例中，完整位置为 `E:\octoeber_learn\october-log\report_mixed.json`。

如果终端已经激活本项目的虚拟环境，可以简写为：

```powershell
python log_tool.py samples/mixed.log --output report_mixed.json --top 3
```

现有输出文件会被写入模式覆盖，运行前请确认输出文件名。

## 4. 输入格式与解析规则

每条有效日志包含5个按空白分隔的字段：

```text
时间 IP 方法 路径 状态码
2026-10-13T10:00:00 192.0.2.10 GET /login 200
```

解析与统计约定：

- 使用 `strip().split()` 拆分字段，连续空格或制表符可以作为分隔。
- 去除首尾空白后没有字段的行，计入空白行。
- 非空行必须恰好包含5个字段，否则计入坏行。
- 状态码必须是三位ASCII十进制数字，数值范围为100至599。
- 路径必须以 `/` 开头，查询字符串保留在路径中。
- 时间、IP和方法只保留文本，目前不做语义校验。
- 有效行才参与IP、路径和状态码频次统计。
- 坏行记录从1开始的原始行号及原因，并继续处理后续行。
- 总行数包含有效行、坏行和空白行；文件末尾的结束换行本身不额外算一行。
- 解析记录中的状态码为整数；报告的状态码频次字典使用字符串键。
- 不同IP数按IP文本去重，不等同于访问人数。

## 5. 命令行参数

```text
python log_tool.py input_path [--output OUTPUT] [--top TOP]
```

| 参数 | 用途 | 规则与默认值 |
| --- | --- | --- |
| `input_path` | 输入日志路径 | 位置参数，必须提供 |
| `--output` | JSON报告路径 | 默认 `report.json` |
| `--top` | IP与路径排行榜数量 | 正整数，默认5 |
| `-h`、`--help` | 显示帮助并结束 | 不要求输入文件 |

参数先解析和检查，再打开日志文件。无效整数、0和负数被拒绝；输入与输出规范化为绝对路径后相同，也会被拒绝，包括 `./` 等价写法。

Top先按次数降序排列，次数相同按名称字符串升序排列。`--top` 同时控制 `top_ips` 和 `top_paths`，完整频次字典不会被截断。实际条目不足N项时返回已有条目。

最简命令使用默认输出位置和Top数量：

```powershell
.\.venv\Scripts\python.exe log_tool.py samples/valid.log
```

所有相对输入、输出路径均相对于当前工作目录，不是自动相对于脚本目录。路径包含空格时使用英文双引号：

```powershell
.\.venv\Scripts\python.exe log_tool.py samples/mixed.log --output "report with spaces.json" --top 3
```

## 6. 三份样例与预期结果

```powershell
.\.venv\Scripts\python.exe log_tool.py samples/mixed.log --output report_mixed.json --top 3
.\.venv\Scripts\python.exe log_tool.py samples/valid.log --output report_valid.json
.\.venv\Scripts\python.exe log_tool.py samples/empty.log --output report_empty.json
```

| 样例 | 总行数 | 有效行 | 坏行 | 空白行 | 不同IP |
| --- | ---: | ---: | ---: | ---: | ---: |
| `mixed.log` | 13 | 7 | 4 | 2 | 3 |
| `valid.log` | 7 | 7 | 0 | 0 | 3 |
| `empty.log` | 0 | 0 | 0 | 0 | 0 |

`valid.log` 与 `mixed.log` 的有效记录相同，因此三类完整频次相同：

- IP：`192.0.2.10` 为3，`192.0.2.20` 为3，`198.51.100.30` 为1。
- 状态码：`200` 为3，`401` 为1，`404` 为2，`500` 为1。
- 路径：`/login` 为3；`/admin`、`/health`、`/missing`、`/search?q=python` 各为1。
- Top 3 IP：`192.0.2.10`、`192.0.2.20`、`198.51.100.30`。
- Top 3路径：`/login`、`/admin`、`/health`。

混合样例第8行为空，第13行仅含空格；第9行少字段，第10行状态码为abc，第11行状态码为700，第12行多字段。错误行号应为 `[9, 10, 11, 12]`。

空文件的频次字典均为 `{}`，Top和错误列表均为 `[]`。

## 7. JSON报告与核对规则

报告保留中文，每层缩进2个空格。字段说明：

| 字段 | 含义 |
| --- | --- |
| `total_lines` | 总行数 |
| `valid_lines` | 有效行数 |
| `bad_lines` | 坏行数 |
| `blank_lines` | 空白行数 |
| `unique_ips` | 不同IP数 |
| `ip_counts` | IP及其出现次数 |
| `path_counts` | 路径及其出现次数 |
| `status_counts` | 状态码字符串及其出现次数 |
| `top_ips` | IP排行榜，条目包含 `item`、`count` |
| `top_paths` | 路径排行榜，条目包含 `item`、`count` |
| `errors` | 坏行记录，条目包含 `line_number`、`reason` |

例如，Top列表条目和错误条目的结构分别为：

```json
{"item": "192.0.2.10", "count": 3}
```

```json
{"line_number": 9, "reason": "字段数量必须为5"}
```

当前开发流程会在写入后重新读取JSON，并通过断言核对：

```text
读回的报告 == 导出前的报告
总行数 == 有效行数 + 坏行数 + 空白行数
IP频次之和 == 有效行数
路径频次之和 == 有效行数
状态码频次之和 == 有效行数
```

具体频次还应与样例的手工预期比较。普通 `assert` 可以被Python的 `-O` 选项关闭，验收时不要使用该选项。报告读回或断言失败属于开发检查问题，当前没有统一包装为友好的CLI提示。

## 8. 错误提示与退出码

| 场景 | 当前行为 | 退出码 |
| --- | --- | ---: |
| 成功统计并导出 | 显示统计摘要 | 0 |
| 查看帮助 | 显示帮助，不读取日志 | 0 |
| 缺少输入参数、Top无效、输入输出同路径 | 显示参数错误 | 2 |
| 输入缺失、UTF-8解码失败、其他输入文件操作错误 | 提示原因并结束 | 1 |
| 输出目录不存在、无写入权限等写入错误 | 提示原因并结束 | 1 |

混合样例中的坏行属于可记录的行级错误，仍能生成报告并正常结束。文件级失败则停止本次处理。错误提示写入标准错误，正常摘要写入标准输出。

错误参数验收命令：

```powershell
.\.venv\Scripts\python.exe log_tool.py samples/mixed.log --top 0
.\.venv\Scripts\python.exe log_tool.py samples/mixed.log --top abc
.\.venv\Scripts\python.exe log_tool.py samples/mixed.log --output ./samples/mixed.log
```

文件错误验收命令，运行前确认以下输入和输出目录确实不存在：

```powershell
.\.venv\Scripts\python.exe log_tool.py samples/no_such.log --output report_missing.json
.\.venv\Scripts\python.exe log_tool.py samples/mixed.log --output no_such_dir/report.json
```

当前程序不会自动创建输出目录。若要生成解码失败样例，可使用单独的辅助文件，不修改三份基准日志：

```powershell
.\.venv\Scripts\python.exe -c "from pathlib import Path; Path('samples/invalid_utf8_test.log').write_bytes(b'\xff')"
.\.venv\Scripts\python.exe log_tool.py samples/invalid_utf8_test.log --output report_invalid.json
```

每次运行后，立即查看该次退出码：

```powershell
$LASTEXITCODE
```

程序不会自动生成 `tool_run.log`。需要保存输出时，可显式重定向：

```powershell
.\.venv\Scripts\python.exe log_tool.py samples/mixed.log --output report_mixed.json 1> run_stdout.txt 2> run_stderr.txt
```

以上两个文本文件保存控制台信息，JSON仍单独写入 `--output` 指定的文件。

## 9. 自动测试

在项目根目录运行：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

当前8条核心测试覆盖：

1. 正常行返回正确字典，状态码为整数。
2. 空白行返回 `None`。
3. 少字段抛出 `ValueError`。
4. 状态码abc抛出 `ValueError`。
5. 状态码700抛出 `ValueError`。
6. 空输入返回全零计数及空映射、空列表。
7. 混合日志的行数、具体频次与错误行号符合预期。
8. Top次数降序、平局名称升序，以及数量截取正确。

预期结尾：

```text
Ran 8 tests in ...

OK
```

显示 `Ran 0 tests` 不算通过。测试文件从正式工具导入函数；正式工具使用主入口判断，被导入时不自动读取日志或打印统计。

确认导入没有触发运行：

```powershell
.\.venv\Scripts\python.exe -c "import log_tool"
```

预期无统计输出，退出码0。上述8条测试主要覆盖函数行为，命令行及文件异常需要结合本说明中的集成命令验收。

## 10. 在PyCharm中运行

将Python运行配置指向本项目的 `log_tool.py`，解释器选择项目的 `.venv\Scripts\python.exe`，工作目录设为项目根目录。

脚本参数栏只填写：

```text
samples/mixed.log --output report_mixed.json --top 3
```

参数栏不填写 `python log_tool.py`，也不放进解释器选项。查看帮助时，将脚本参数改为 `--help`。如果提示缺少 `input_path`，检查脚本参数是否填写、是否选择了对应运行配置。

## 11. 新目录复现

将 `log_tool.py`、`samples`、`tests`、`README.md`、`.gitignore` 及需要的文档复制到新的目录。重新创建虚拟环境，不复制原来的 `.venv` 和缓存。

在新项目根目录，按照第3节创建环境，再按第6节生成三份报告，按第9节运行测试。将新目录、Python版本、实际命令、结果和修复记录到 `docs`。原有JSON报告不是复现运行的必需输入。

## 12. 当前范围与文件管理

- 当前只支持约定的五字段文本日志，不直接兼容Nginx、Apache或 `http.server` 的原始日志格式。
- 不校验时间、IP和方法的语义；不把不同IP数解释为真实人数。
- JSON保存完整报告。CSV独立练习用于记录读写及IP频次表导出，正式CLI当前没有CSV输入或导出选项。
- 当前先将全部日志读入内存，适合学习样例，未针对超大日志优化。
- 输出目录需提前存在；同名输出会覆盖。输入输出路径保护基于 `Path.resolve()` 比较，不承诺识别不同路径指向同一文件的所有情况，例如硬链接。
- 版本控制保留源码、测试、README和三份基准日志。运行报告可作为本地验收证据保存。
- 当前 `.gitignore` 忽略虚拟环境、Python缓存以及根目录的 `report.json`、`tool_run.log`；不会自动忽略所有 `report_*.json` 或重定向文件，提交前应查看差异并明确选择文件。

2026-10-24本机验证：8条核心测试通过；三份样例统计与JSON读回通过；帮助、Top无效值、同路径保护、缺失输入、解码失败、输出目录缺失及带空格路径均通过。尚不能仅凭这些结果将新目录复现与全部v0.1学习验收记为完成。
