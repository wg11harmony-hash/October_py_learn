"""日志工具自动测试练习模板。

实现核心函数后，在这里编写unittest.TestCase及测试方法。
建议至少覆盖以下8种行为：
1. 正常五字段行返回记录字典，status为整数200。
2. 仅含空白的行返回None。
3. 少字段抛ValueError。
4. 状态码abc抛ValueError。
5. 状态码700抛ValueError。
6. 空输入的四类行数与唯一IP数均为0。
7. mixed.log得到13总行、7有效、4坏、2空白及正确频次。
8. 两个IP各3次时192.0.2.10排在192.0.2.20之前。

本文件尚未包含测试方法；不要把发现0条测试记为测试通过。
测试运行方式见README.md。
"""

import unittest

# 核心函数完成后再导入，例如：
# from log_tool import parse_line, analyze_lines, top_items

# 从这里开始编写测试类与具体断言。
