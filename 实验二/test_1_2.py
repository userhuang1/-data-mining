'''
由于每一小问的代码量不多，所以将前三个小问放入一个py文件中（注释里面）
'''
import matplotlib.pyplot as plt
import os
import xlrd
import xlwt
import numpy as np
import math
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False

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

#课程1的位置是下标五
#体能成绩是最后一位
#将excellent = 90，good = 80,general = 70,bad =60
x = []
y = []
for i in range(len(list1)):
    x.append(int(list1[i][5]))
    if(list1[i][-1] == "excellent"):
        y.append(90)
    elif(list1[i][-1] == "good"):
        y.append(80)
    elif(list1[i][-1] == "general"):
        y.append(70)
    elif(list1[i][-1] == "bad"):
        y.append(60)
    else:
        y.append(0)



'''
1. 请以课程1成绩为x轴，体能成绩为y轴，画出散点图。
#第一小问的代码
'''
# for i in range(len(list1)):
#     print(x[i],y[i])
#
# plt.title('散点图',fontsize=18,color='red') #为图表明题目
# plt.xlabel('课程1成绩',fontsize=12,color='yellowgreen') #表示x代表的含义以及颜色
# plt.ylabel('体能成绩',fontsize=12,color='yellowgreen') #表示y代表的含义以及颜色
#
# #为纵坐标设置一个宽度，不设置的话会根据数据自动调整
# my_y=np.arange(0,100,10)
# plt.yticks(my_y)
#
# #绘图
# plt.scatter(x,y )  #散点图的横纵坐标
# plt.show()   #将画出的散点图显示出来



'''
2. 以5分为间隔，画出课程1的成绩直方图。
第二小问的代码
'''
#从第一个小问可以得到课程1的数据就在x中存放，可以直接使用
plt.title('直方图',fontsize=18,color='red')
plt.xlabel('课程1成绩',fontsize=12,color='green')
plt.ylabel('在该成绩区间的人数',fontsize=12,color='green')
my_x = np.arange(0,100,5)  #返回的是一个元组
plt.xticks(my_x)  #设置5的刻度

bins = np.linspace(min(x),max(x))

# 这个是调用画直方图的函数，意思是把数据按照从bins的分割来画
plt.hist(x,bins)
plt.show()


