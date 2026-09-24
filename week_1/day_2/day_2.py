# 数据类型 符号运算 函数运算 类型转换 字符串操作

# int 整数 0b-2 0o-8 0x-16
# float 浮点数 由于二进制与十进制的互化，会出现不确定尾数
# 复数 j
# round( , 保留位数 ) 四舍五入 排除浮点数不确定尾数影响
# eg
# print(0.1+0.2) #0.30000000000000004
# print(0.1+0.2==0.3)  #False
# print(round(0.1+0.2,1)==0.3) #True

# // 整数除 10//3=3
# 二元运算符 += /= 等
# a**=3 -> a=a**3

# abs 取绝对值
# divmod 商余 divmod(10,3) -> (3,1)
# pow(x,y,z) 乘方 z为取模运算
# max min

# float()
# int()
# complex()

def dayUp (df):
    dayup=1
    for i in range(365):
        if i%7 in [0,6]:
            dayup=dayup*0.99
        else :
            dayup=dayup*(1+df)
    return dayup
dayfactor=0.01
a=round(1.01**365,2)
while dayUp(dayfactor)<a:
    dayfactor+=0.001
print(f"工作日的努力参数是: {dayfactor:.3f}")

# str.split 分割
# str.count 计数，统计出现次数
# str.strip 去除左右两侧出现的特定元素
# str.center ( width , fillchar ) 居中
# str.join 用str来填充进后面
# print(",".join("12345"))  #1,2,3,4,5
# chr 编码 -> 字符
# ord 字符 -> 编码

# 凯撒密码
s = input()
t = ""
for c in s:
    if 'a' <= c <= 'z':
        t += chr( ord('a') + ((ord(c)-ord('a')) + 3 )%26 )
    elif 'A' <= c <= 'Z':
        t += chr( ord('A') + ((ord(c)-ord('A')) + 3 )%26 )
    else:
        t += c
print(t)

# 输出填空
# print(f"{变量}")
# print("123{2}456{1}789{0}".format("0","00","000"))  可编序

# 冒号 → 填充 → 对齐 → 宽度 → 千分逗号 → . 精度 → 类型
# 对齐 < 左 > 右 ^ 居中
# eg
# print("{:=^20}".format("python")) # =======python=======
