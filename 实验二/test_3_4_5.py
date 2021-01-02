import matplotlib.pyplot as plt
import os
import xlrd
import math, functools
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False

# # 读入数据
# student_data = []
# with open('data.csv') as f:
#     file_csv = csv.reader(f)
#     student_data = [list(map(float, v)) for v in file_csv]
list1 = []
file1_addr = "C:/Users/win10/Desktop/数据挖掘/实验二/hxb_test2.xlsx"
if os.path.exists(file1_addr):
    print("********************")
    xlrd_file = xlrd.open_workbook(file1_addr)
    xlrd_sheet = xlrd_file.sheets()[0]
    nrow = xlrd_sheet.nrows
    ncol = xlrd_sheet.ncols
    for i in range(nrow):
        list1.append(xlrd_sheet.row_values(i))


# for i in list1:
#     print(i)

student_data = [] #将c1到c9的成绩以及体育成绩都放入这个列表中
cur = []  #用来存放每一行的数据，方便最后的读入
for i in range(len(list1)):
    for j in range(5,14):
        if(list1[i][j] != "NULL"):
            cur.append(int(list1[i][j]))
        else:
            cur.append(0)
    if(list1[i][-1] == "excellent"):
        cur.append(90)
    elif (list1[i][-1] == "good"):
        cur.append(80)
    elif (list1[i][-1] == "general"):
        cur.append(70)
    elif (list1[i][-1] == "bad"):
        cur.append(60)
    else:
        cur.append(0)
    # print(cur)
    student_data.append(cur)  #将本轮获得的数据放入student_data中
    cur = []  #将数据插入student_data后就删除掉，
    # print(i,student_data)
    # if(i!=len(list1)-1):
    #     cur.clear()


# print(len(student_data))
# for i in student_data:   #查看筛选出来的成绩的结果
#     print(i)

# 平均数
def avg(x):
    return sum(x) / len(x)

# 协方差
def cov(x):
    sum_ = sum(x)
    n = len(x)
    return (sum([i * i for i in x]) - sum_ * sum_ / n) / (n - 1)  #公式，
# 其中i * i for i in x代表的是从将x这种的数据逐个抽取出来并且做平方运算得出结果（返回值）
# 计算标准差
def std(x):
    return math.sqrt(cov(x))  #嵌套公式使用

# 计算相关性
def correlation(A, B):
    def sol(l):
        avg_ = avg(l)
        std_ = std(l)
        return [(x - avg_) / std_ for x in l]
    return sum([x * y for x, y in zip(sol(A), sol(B))])

def zscore(A):
    m, s = avg(A), std(A)
    if s == 0:
        # 如果标准差为0，所有元素相等
        return [0 for _ in A]
    return [(x - m) / s for x in A]

# 矩阵转置
def rev(A):
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]

# 计算zscore归一化的数据矩阵
zscore_mat = rev([zscore(l) for l in rev(student_data)])
#由于矩阵过宽，所以我将他放在一个TXT文件中查看
# for i in zscore_mat:
#     print(i)

#可以再归一矩阵.xls中查看结果
'''
file1 = open("归一矩阵.xls",'w',encoding='utf-8')
for i in zscore_mat:
    for j in i:
        file1.write(str(j))
        file1.write('\t')
    file1.write('\n')
file1.close()
'''



# 计算相关矩阵
correlation_mat = [[correlation(student_data[i], student_data[j]) for j in range(len(student_data))]  #换行
for i in range(len(student_data))]

# 可视化混淆矩阵
plt.matshow(correlation_mat, cmap=plt.cm.BuGn) #可以设置颜色，颜色的选择可以自选，按Ctrl+左键可以查找到颜色
plt.colorbar()  #颜色条
plt.title("混淆矩阵",fontsize = 15,y = 1.1)  #其中的y是让标题设置高一点
plt.show() #显示

# 根据相关矩阵，找到距离每个样本最近的三个样本，得到100x3的矩阵（每一行为对应三个样本的ID）输出到txt文件中，以\t,\n间隔
# 相关性越大，距离越近

# 通过自定义排序找到最大值的下标
index = [i for i in range(len(correlation_mat))]
with open('相关矩阵.txt', 'w') as f:
    # f.write("相关性：\n")
    for l in correlation_mat:
        index.sort(key=functools.cmp_to_key(lambda x, y: l[y] - l[x]))
        for cnt in range(3):
            f.write(str(index[cnt]))
            f.write('\t')  #排版好看一些
        f.write('\n')
