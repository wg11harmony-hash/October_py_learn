"""Python离线日志统计工具练习模板。

按十月剩余计划逐步完成：
1. 读取samples/mixed.log，观察每行和行号。
2. 编写parse_line(line)，区分有效行、空白行和坏行。
3. 编写analyze_lines(lines)，统计行数和IP、路径、状态码频次。
4. 编写top_items(counts, n)，次数降序，平局按名称升序。
5. 加入JSON导出、命令行参数和文件级错误提示。
6. 编写main()，使用主入口判断，保证导入模块不自动处理文件。

本文件为待填写模板；当前尚未实现统计功能。
样例格式及预期结果见README.md。
"""
from itertools import count
from pathlib import Path
import json
import argparse
import sys

PROJECT_DIR = Path(__file__).resolve().parent
SAMPLES_DIR = PROJECT_DIR / "samples"
# 从这里开始编写自己的实现。
def read_lines (int_path):
    lines=[]
    with open(int_path,"r",encoding="utf_8") as f:
        for line in f:
            lines.append(line)
    return lines

def parse_line(line):
    fields = line.strip().split()
    if not fields:
        return None
    if len(fields) != 5:
        raise ValueError("字段数量必须为5")
    time, ip, method, path, status_text = fields
    if (
                len(status_text) != 3
                or not status_text.isascii()
                or not status_text.isdecimal()
     ):
        raise ValueError("状态码必须为三位ASCII数字")
    status = int(status_text)
    if not 100 <= status <= 599:
        raise ValueError("状态码必须在100至599之间")
    if not path.startswith("/"):
        raise ValueError("路径必须以/开头")
    return {
         "time": time,
         "ip": ip,
         "method": method,
         "path": path,
         "status": status,
        }

def judge_lines(lines):
    normal_lines = []
    for line in lines:
        try:
            record = parse_line(line)
        except ValueError:
            continue
        if record is not None:
            normal_lines.append(line)
    return normal_lines

def analyze_lines(lines,top_n=5):
    count_ip = {}
    count_path = {}
    count_status = {}

    total_lines = 0
    valid_lines = 0
    bad_lines = 0
    blank_lines = 0
    errors = []
    for line_number, line in enumerate(lines, start=1):
        total_lines += 1
        try:
            record = parse_line(line)
        except  ValueError as error:
            bad_lines += 1
            errors.append({
                "line_number": line_number,
                "reason": str(error),
            })
            continue
        if record is None:
            blank_lines += 1
            continue

        valid_lines += 1
# 从解析后的字典取值，无需再次split
        ip = record["ip"]
        path = record["path"]
        status = str(record["status"])
        count_ip[ip] = count_ip.get(ip, 0) + 1
        count_path[path] = count_path.get(path, 0) + 1
        count_status[status] = count_status.get(status, 0) + 1

    return {
    "total_lines": total_lines,
    "valid_lines": valid_lines,
    "bad_lines": bad_lines,
    "blank_lines": blank_lines,
    "unique_ips": len(count_ip),
    "ip_counts": count_ip,
    "path_counts": count_path,
    "status_counts": count_status,
    "top_ips": top_items(count_ip, top_n),
    "top_paths": top_items(count_path, top_n),
    "errors": errors,
        }

def top_items(counts, n):
    # 将字典转换为(key, value)形式
    items = counts.items()
    # 排序：
    # -item[1]：次数降序
    # item[0]：名称升序
    sorted_items = sorted(
        items,
        key=lambda item: (-item[1], item[0])
    )
    result = []
    for item, count in sorted_items[:n]:
        result.append({
            "item": item,
            "count": count,
        })
    # 取前 n 个
    return result

def save_json(report, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            report,
            f,
            ensure_ascii=False,
            indent=2,
        )

def read_report(input_path):
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_args():
    parser = argparse.ArgumentParser(
        description="统计日志并导出JSON报告"
    )
    parser.add_argument(
        "input_path",
        help="输入日志文件路径",
    )
    parser.add_argument(
        "--output",
        default="report.json",
        help="JSON输出路径，默认report.json",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="Top数量，必须为正整数，默认5",
    )
    args = parser.parse_args()
    if args.top <= 0:
        parser.error("--top必须是正整数")

    input_path = Path(args.input_path).resolve()
    output_path = Path(args.output).resolve()

    if input_path == output_path:
        parser.error("输入和输出不能是同一个文件")

    return args

def main():

    args = get_args()

    try:
        lines = read_lines(args.input_path)

    except FileNotFoundError:
        print(
            f"错误：输入文件不存在：{args.input_path}",
            file=sys.stderr,
        )
        return 1

    except UnicodeDecodeError:
        print(
            f"错误：输入文件无法按UTF-8解码：{args.input_path}",
            file=sys.stderr,
        )
        return 1

    except OSError as error:
        print(
            f"错误：无法读取输入文件：{error}",
            file=sys.stderr,
        )
        return 1
    report = analyze_lines(lines, top_n=args.top)

    output_path = Path(args.output)
    try:
        save_json(report, output_path)
    except OSError as error:
        print(
            f"错误：无法写入JSON报告：{output_path}；原因：{error}",
            file=sys.stderr,
        )
        return 1
    restored = read_report(output_path)

        # 这里继续保留原来的assert和print
    assert restored == report, "JSON读回结果不一致"

    # 检查四个计数等式
    assert restored["total_lines"] == (
        restored["valid_lines"]
        + restored["bad_lines"]
        + restored["blank_lines"]
    ), "总行数不一致"

    for field in ("ip_counts", "path_counts", "status_counts"):
        assert (
            sum(restored[field].values()) == restored["valid_lines"]
        ), f"{field}频次之和不一致"
    print("总行数：", report["total_lines"])
    print("有效行：", report["valid_lines"])
    print("坏行：", report["bad_lines"])
    print("空白行：", report["blank_lines"])
    print("Top IP：", report["top_ips"])
    print("Top路径：", report["top_paths"])
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
