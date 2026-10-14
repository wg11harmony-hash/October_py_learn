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

PROJECT_DIR = Path(__file__).resolve().parent
SAMPLES_DIR = PROJECT_DIR / "samples"
file_path = SAMPLES_DIR / "mixed.log"
# 从这里开始编写自己的实现。
def read_lines ():
    lines=[]
    with open(file_path,"r",encoding="utf_8") as f:
        for number,line in enumerate (f,start=1):
            print(f"{number:02d}    {line.strip()}")
            lines.append(line)
    return lines

def parse_lines(lines):
    count={}
    normal_line=[]
    for line in lines:
        fields=line.strip().split()
        if not fields:
            count["white_line"]=count.get("white_line",0)+1
            continue
        if  (len(fields)!=5
        or (len(fields[-1])!=3
        or not fields[4].isascii()    # 判断ASCII
        or not fields[4].isdecimal()  # 判断数字
        or not 599>=int(fields[4])>=100)):
            count["error_line"]=count.get("error_line",0)+1
            continue
        else:
            normal_line.append(line)
            count["normal_line"]=count.get("normal_line",0)+1
    return count

def judge_lines(lines):
    normal_line=[]
    for line in lines:
        fields=line.strip().split()
        if not fields:
            continue
        if (len(fields)!=5
        or (len(fields[-1])!=3
        or not fields[4].isascii()    # 判断ASCII
        or not fields[4].isdecimal()  # 判断数字
        or not 599>=int(fields[4])>=100)):
            continue
        else:
            normal_line.append(line)
    return normal_line

def analyze_lines(lines):
    count_ip={}
    count_path={}
    count_status={}
    normal_line=judge_lines(lines)
    for line in normal_line:
        fields=line.strip().split()
        count_ip[fields[1]]=count_ip.get(fields[1],0)+1
        count_path[fields[3]]=count_path.get(fields[3],0)+1
        count_status[fields[4]]=count_status.get(fields[4],0)+1
    return count_ip,count_path,count_status

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
    # 取前 n 个
    return sorted_items[:n]

def save_json(result, output_file):
    data = {
        "ip": result[0],
        "path": result[1],
        "status": result[2]
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,  # 关闭ASCII转换
            indent=4             # 缩进格式
        )
def main():
    lines = read_lines()
    result = analyze_lines(lines)
    print(result)

if __name__ == "__main__":
        main()