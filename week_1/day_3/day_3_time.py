# time库的使用

import time

# 获取时间戳  1790232239.4002867
print(time.time())
# 获取系统时间  Thu Sep 24 14:43:59 2026
print(time.ctime())
# 获取系统时间 time.struct_time(tm_year=2026, tm_mon=9, tm_mday=24, tm_hour=6, tm_min=45, tm_sec=51, tm_wday=3, tm_yday=267, tm_isdst=0)
# 计算机可以处理的时间格式
print(time.gmtime())

# time.strftime 将struct_time转换为字符串
print(time.strftime("%Y-%m-%d %a %H:%M:%S %I %p", time.localtime()))
# time.strptime 将字符串转换为struct_time
timeStr = '2018-01-26 12:55:20'
res = time.strptime(timeStr, "%Y-%m-%d %H:%M:%S")
print(res)

# 程序计时
# time.perf_counter() 需连续调用  含休眠
# time.process_counter() 不含休眠
# time.sleep(seconds) 休眠
start = time.perf_counter()  # 计时开始
# -------- 测试代码 --------
time.sleep(1)
s = 0
for i in range(1000000):
    s += i
# ----------------------------------
end = time.perf_counter()    # 计时结束
print(f"运行耗时：{end - start:.6f} 秒")

# TextProBarV1.py
for i in range(101):
    print("\r{:3}%".format(i), end="")
    time.sleep(0.1)

#########
print()
#########

# \r 回到行首
# end= 去除 print 自动换行特性
# TextProBarV3.py
scale = 50
print("执行开始".center(scale//2, "-"))
start = time.perf_counter()
for i in range(scale+1):
    a = '*' * i
    b = '.' * (scale - i)
    c = (i/scale)*100
    dur = time.perf_counter() - start
    print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c,a,b,dur),end='')
    time.sleep(0.1)
print("\n"+"执行结束".center(scale//2, "-"))


