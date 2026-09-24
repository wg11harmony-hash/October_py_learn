# 程序分支 循环 random库

# 单分支 if :
# 二分支 if :  else :
# 紧凑形式 <表达式1>if<条件>else<表达式2>
# 多分支 if :  elif :  elif :

# 遍历循环
# for <循环变量> in <遍历结构> :
# 计数循环
# for i in range(start,end,step):
# 字符串循环
# for c in s:
# 列表循环
# for item in ls:
# 文件循环
# for line in fi:

# 无限循环 while  ctrl+c强制退出
# continue 结束单次循环
# break 结束后续循环

# 循环与else
# 若不被break 则else 不被continue影响

# random库
# 给定seed，所出现随机数则一致，便于程序复现
# 若不给seed，则以第一次调用random系统时间作为seed，精确至微秒，不可复现
import random
random.seed(10)
print(random.random())
print(random.random())
# 扩展随机数
# 导入random随机数库
import random

# seed(n)：固定随机种子，相同种子会产生完全一样的随机序列，方便复现结果
# 注释：如果不写seed，默认使用系统时间作为种子，每次运行随机数不同
random.seed(10)
# random.random() 生成 [0.0, 1.0) 之间的随机浮点数（包含0.0，不包含1.0）
r1 = random.random()
print(f"random() 0~1随机小数：{r1}")

# randint(a,b) 生成 [a, b] 的随机整数，左右边界都包含
r2 = random.randint(1, 10)
print(f"randint(1,10) 1到10随机整数：{r2}")

# randrange(m,n,k)：从m开始，到n之前，以k为步长随机选整数，区间[m,n)，取不到n
# 示例：只能在1,3,5,7,9里面随机挑选
r3 = random.randrange(1, 10, 2)
print(f"randrange(1,10,2) 步长2随机整数：{r3}")

# getrandbits(k)：生成k个二进制位长度的随机整数
r4 = random.getrandbits(8)
print(f"getrandbits(8) 8比特随机整数：{r4}")

# uniform(a,b)生成[a,b]之间随机浮点数，和random()区别：可以自定义区间，不限于0-1
r5 = random.uniform(2, 8)
print(f"uniform(2,8) 2到8随机小数：{r5}")

# seq可以是列表、字符串等序列类型
lst = ["苹果","香蕉","橙子"]
r6 = random.choice(lst)
print(f"choice随机选取元素：{r6}")

# shuffle直接修改原列表！无返回值，不能写 new_lst = random.shuffle(lst)
lst2 = [1,2,3,4,5]
random.shuffle(lst2)
print(f"shuffle打乱后的列表：{lst2}")

# 计算圆周率
# 直接导入random 不用再写random.random
from random import random
pi=0
N=10000
for i in range(N):
    x,y=random(),random()
    if x**2+y**2<1:
        pi+=1
print(4*pi/N)

# 水仙数
a=""
for i in range(100,1000):
    s=str(i)
    if int(s[0])**3+int(s[1])**3+int(s[2])**3==i:
        a+=f"{s},"
print(f"{a}".strip(","))

print(",".join(str(i) for i in range(100,1000) if sum(int(c)**3 for c in str(i)) == i))

b0=""
for i in range(100,1000):
    bai = i // 100
    shi = (i//10) % 10
    ge = i % 10
    if bai**3 + shi**3 + ge**3 == i:
        b0+=f"{i},"
print(f"{b0}".strip(","))




