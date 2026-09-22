"""
平台学习：学习变量、赋值、input、print、int和float；
本地实践：编写 ，尝试整数、小数和负数输入。
当天验收：解释 input 返回字符串；转换结果正确，输出格式符合题意。
"""
# input 获取结果一律返回字符串类型 str

# eval 去掉字符串形式，执行内语句
# 双重引号报错 外双内单 / 外单内双 / 转义符\"
eval("print('hello world')")

# 货币转换
# try 异常捕获 防止报错
# try - except 捕获异常 - else 不报错则执行 - finally 最终一定执行
# 多重选择 ((A,B)) 借助元组
# and 与 &
# if 条件语句不使用 & ；& 优先级高，容易逻辑上出错
# num >= 0 & c.startswith("RMB") ；优先执行 0 & c.startswith()
# [start:end:step] 切片 前闭后开
try:
    c=input()
    if c.startswith(("RMB","rmb")) and float(c[3:])>=0:
        print(f"USD{float(c[3:])/6.78:.2f}")
    elif c.startswith(("USD","usd")) and float(c[3:])>=0:
        print(f"RMB{float(c[3:])*6.78:.2f}")
    else:
        print("error")
except ValueError:  # 具体异常种类 不填则为所有异常
    print("error")