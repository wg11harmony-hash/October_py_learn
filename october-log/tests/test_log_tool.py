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
from log_tool import parse_line, analyze_lines, top_items
from pathlib import Path

# 从这里开始编写测试类与具体断言。
class TestParseLine(unittest.TestCase):

    def test_parse_normal_line(self):
        # 准备输入
        line = "2026-10-22T10:00:00 192.0.2.10 GET /login 200"

        # 根据输入，手工写出预期结果
        expected = {
            "time": "2026-10-22T10:00:00",
            "ip": "192.0.2.10",
            "method": "GET",
            "path": "/login",
            "status": 200,
        }
        # 调用待测函数，得到实际结果
        actual = parse_line(line)
        # 比较实际与预期
        self.assertEqual(actual, expected)
        # 确认状态码已经转换成整数
        self.assertIsInstance(actual["status"], int)

    def test_parse_blank_line(self):
        line = "  \t\n"
        # 调用解析函数
        actual = parse_line(line)
        # 检查返回值是否为None
        self.assertIsNone(actual)

        fields = line.strip().split()
        if not fields:
            return None
        self.assertIsNone(actual)

    def test_parse_missing_fields(self):
        # 只有4个字段，缺少状态码
        line = "2026-10-22T10:00:00 192.0.2.10 GET /login"

        # 预期解析函数抛出ValueError
        with self.assertRaises(ValueError):
            parse_line(line)

    def test_parse_nonnumeric_status(self):
        # 五个字段齐全，但状态码不是数字
        line = "2026-10-22T10:00:00 192.0.2.10 GET /login abc"

        with self.assertRaises(ValueError):
            parse_line(line)

    def test_parse_out_of_range_status(self):
        # 五个字段齐全，状态码为三位数字，但超出范围
        line = "2026-10-22T10:00:00 192.0.2.10 GET /login 700"

        with self.assertRaises(ValueError):
            parse_line(line)

class TestAnalyzeLines(unittest.TestCase):

    def test_analyze_empty_input(self):
        # 没有任何日志行
        lines = []

        # 手工写出预期报告
        expected = {
            "total_lines": 0,
            "valid_lines": 0,
            "bad_lines": 0,
            "blank_lines": 0,
            "unique_ips": 0,
            "ip_counts": {},
            "path_counts": {},
            "status_counts": {},
            "top_ips": [],
            "top_paths": [],
            "errors": [],
        }

        # 获取实际统计结果
        actual = analyze_lines(lines)

        # 检查完整报告
        self.assertEqual(actual, expected)

    def test_analyze_mixed_log(self):
        # 从tests目录向上一级，找到项目根目录
        project_dir = Path(__file__).resolve().parent.parent
        sample_path = project_dir / "samples" / "mixed.log"

        # 读取真实样例，保留所有行，包括空白行
        with open(sample_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        actual = analyze_lines(lines)

        # 检查行数和不同IP数
        self.assertEqual(actual["total_lines"], 13)
        self.assertEqual(actual["valid_lines"], 7)
        self.assertEqual(actual["bad_lines"], 4)
        self.assertEqual(actual["blank_lines"], 2)
        self.assertEqual(actual["unique_ips"], 3)

        # 检查每个IP的具体次数
        self.assertEqual(
            actual["ip_counts"],
            {
                "192.0.2.10": 3,
                "192.0.2.20": 3,
                "198.51.100.30": 1,
            },
        )

        # 检查每个路径的具体次数
        self.assertEqual(
            actual["path_counts"],
            {
                "/login": 3,
                "/admin": 1,
                "/health": 1,
                "/missing": 1,
                "/search?q=python": 1,
            },
        )

        # 状态码频次的键应为字符串
        self.assertEqual(
            actual["status_counts"],
            {
                "200": 3,
                "401": 1,
                "404": 2,
                "500": 1,
            },
        )

        # 检查坏行的行号
        error_lines = [
            error["line_number"]
            for error in actual["errors"]
        ]
        self.assertEqual(error_lines, [9, 10, 11, 12])

class TestTopItems(unittest.TestCase):

    def test_top_items_order_and_limit(self):
        # 故意把低频项放前面，并把两个并列项反着排列
        counts = {
            "198.51.100.30": 1,
            "192.0.2.20": 3,
            "192.0.2.10": 3,
        }

        actual = top_items(counts, 2)

        expected = [
            {"item": "192.0.2.10", "count": 3},
            {"item": "192.0.2.20", "count": 3},
        ]

        self.assertEqual(actual, expected)