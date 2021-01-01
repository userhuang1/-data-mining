import xlrd
import xlwt
import os
import math


#list1表示xlrd中的数据，list2表示的是TXT文件中的数据
list1 = []
file1_addr = "C:/Users/win10/Desktop/数据挖掘/实验一/数据源1.xlsx"  #获取地址
if os.path.exists(file1_addr): #判断文件是否存在
    xlrd_file = xlrd.open_workbook(file1_addr)
    xlrd_sheet = xlrd_file.sheets()[0]  #打开文件
    nrows = int(xlrd_sheet.nrows)  #获取行数和页数
    ncols = int(xlrd_sheet.ncols)
    for row in range(1, nrows):  #遍历数据（从第一行开始）
        list1.append(xlrd_sheet.row_values(row))
    #     最开始的list1（读入数据）
    # for i in list1:
    #     print(i)


list2 = []
file2_addr = "C:/Users/win10/Desktop/数据挖掘/实验一/数据源2.txt" #测试是否成功的
with open(file2_addr,'r+',encoding='utf-8') as f:  #这里相当于将文件打开并赋给f
    for index,line in enumerate(f.readlines()):   #每行读入数据
        if index>0:  #确保第一行的表头不会被读入数据列表中
            list2.append(line.strip().split(',')) #清楚前后空格，并且按照，分割开
    # 最开始的list2（读入TXT数据）
    # for i in list2:
    #     print(i)

# print("####################################")
# for i in list2:
#     if i not in list1:
#         list1.append(i)
#
# print(list1)


#去重操作，根据名字去重
list1_rem_dict = {}  #存放的是出现过得name值
for cnt,i in enumerate(list1):
    if i[1] in list1_rem_dict:  #查看名字是否出现过，如果出现过就将后出现的这个人的信息删除
        list1.pop(cnt)
    else:
        list1_rem_dict[i[1]] = 1  #将未出现过得name当做key加入字典中

# for i in list1:
#     print(i)

#原版有bug存在，名字不应该是连续的，可能是不连续的。
#对于list2数据（从TXT文件中获得的数据）
#去重操作，根据名字去重
#操作与上面相同
list2_rem_dict = {}  #存放的是出现过得name值
for cnt,i in enumerate(list2):
    if i[1] in list2_rem_dict:
        list2.pop(cnt)
    else:
        list2_rem_dict[i[1]] = 1  #将未出现过得name当做key加入字典中

# for i in list2:
#     print(i)


# print("***************************************************************************")
#处理不同名字的序号问题：
for i in range(len(list2)):
    if (i<len(list2)-1):
        if(list2[i][0] == list2[i+1][0]):  #判断序号是否相同
            if(int(list2[i+1][0])+1<int(list2[i+2][0])): #如果可以将学号直接加一
                list2[i+1][0] = str(int(list2[i+1][0])+1)
            else:
                list2[i+1][0] = str(int(list2[len(list2)-1][0])+1)#将学号转化为最后的学号的后一位
                # list2.pop(i)
                list2.append(list2.pop(i+1))  #其实是两个函数，先删除前一个信息，然后将信息放到最后面

# for i in list2:
#     print(i)

# #合并两个表放入list_all列表之中
# list_all = []
# list_all = list1 + list2
#
# for i in list:
#     print(i)

all_key = {}
print("最后的结果显示如下：")
print()
#合并数据
#以第一个作为基准值，将第二个的数据存放入第一个中
for i in range(len(list1)):
    cur_name = list1[i][1]    #记录下当前的name
    all_key[cur_name] = 1
    for j in range(len((list2))):
        if(cur_name == list2[j][1]): #在list2中查找与当前name相同的name
            for k in range(len(list1[0])):
                if(list1[i][k]==''):  #对于list1中缺少的数据，将list2的值传给他
                    list1[i][k] = list2[j][k]

cur_index = list1[-1][0] #记录的是现在的最后一位的序号
# print(cur_index)
for j in list2:
    if (j[1] not in all_key): #将不再list1中出现过的姓名（即在一中缺失的信息放入其中）
        j[0] = cur_index+1  #先将加入的每一个人都给重新排列学号
        cur_index += 1  #更新现在的最大学号
        list1.append(j)

# for i in list1:
#     print(i)
# print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
# print()

#数据规整化：
#1、没有值的写NULL
#2、Gender：以male/female表示
#3、Height：单位为m
#4、课程1-10成绩：不为NULL的均以int类型表示
#5、把处理后的data列表导出到【xxe3.xls】中，以便直接查看结果，以验证上面操作的正确性。

for i in list1:  #将值不存在的数归为NULl
    for j in range(len(i)):
        if(i[j]==""):
            i[j] = "NULL"  #这个值可以随意改动，只要自己知道不同既可（但不能是列表中的任意一个出现过的字符串）

for i in range(len(list1)):
    if(list1[i][3] == 'female'): #统一性别的称呼，方便后面的计算
        list1[i][3] = 'girl'
    elif(list1[i][3] == 'male'):  #female->girl, male->boy
        list1[i][3] = 'boy'

for i in range(len(list1)):
    if(float(list1[i][4])>3):  #正常来说，不可能有人超过三米高，所以这里取值为三，大于三证明是使用cm为单位
    # if(list1[i][4]>'100'):
        list1[i][4] = ("%.2f"%float(list1[i][4]/100))  #将单位转化为统一，并且都是转为float类型数据
    #一个小细节需要注意，我在最外面多加了一个float，但是默认是一位小数，咖喱很久没有解决，最后自己尝试发现错误
    else:
        list1[i][4] = ( "%.2f" % float(list1[i][4])) #将数据转为float类型并且是两位小数

#测试用例，发现float默认一个小数
# w = 1.6
# w = float("%.2f" % (w))
# print(w)

#由于成绩的分布在列表之中是5到15，所以
#转化为int类型的数据，相当于去掉了后面的小数点。向下取整
for i in  list1:
    for cnt in range(5,15):
        if(i[cnt] != "NULL"):
            i[cnt] = int(i[cnt])

# i = 1.6
# print(int(i))



#将结果放入硬盘中

result = open("经过整理的数据.xls",'w',encoding='utf-8') #创建一个新的xls文件，存放经过清理整合好的数据
for i in range(len(list1)):
    for j in range(len(list1[i])):
        result.write(str(list1[i][j])) #一个个读入
        result.write('\t')
    result.write('\n')  #读完一行换一行
result.close()  #关闭文件（这个一定要做） 养成好习惯
print('经过清理的文件已放入“经过整理的数据.xls"中')
print()
# result.write()


#1. 学生中家乡在Beijing的所有课程的平均成绩。
#对于每一个成绩都需要进行计算
count = 0  #计算家乡在北京的总人数
score = [0,0,0,0,0,0,0,0,0,0]
for i in range(len(list1)):
    if(list1[i][2] == "Beijing"):
        count += 1
        for cnt in range(5,15):
            if(list1[i][cnt] != "NULL" ): #空值相当于直接加了一个0 ，
                score[cnt-5] += int(list1[i][cnt])

#将总分转化为平均分
for i in range(len(score)):
    score[i] ="%.5f" % float(score[i]/count)


# for i in list1:
#     print(i)


print("各科的平均成绩")
for i in range(len(score)):
    print("C",i+1,"科目的平均成绩是: ",score[i],"分",sep='') #sep表示省略空格
print()
#2. 学生中家乡在广州，课程1在80分以上，且课程9在9分以上的男同学的数量。(备注：该处做了修正，课程10数据为空，更改为课程9)
count = 0  #符合条件的人数
heshi = []# 用来存放符合条件的人的姓名
for i in range(len(list1)):
    if(list1[i][2] == "Guangzhou" and list1[i][3] == "boy" and list1[i][5]>80 and list1[i][13]>9):
        heshi.append(list1[i][1])
        count += 1


print("学生中家乡在广州，课程1在80分以上，且课程9在9分以上的男同学的数量为",count,"人")
print("分别是：")
for i in range(count):
    print('\t',heshi[i],',')
print("         等人")
print()


#3. 比较广州和上海两地女生的平均体能测试成绩，哪个地区的更强些？
#自定义：excellent=90，good=80,general=70,bad=60，空的就不计算进去人数了
#定义广州人数和上海人数变量 guang_num,shang_nam;
guang_girl_num = 0 #广州有体育成绩的女生人数
shang_girl_num = 0 #上海有体育成绩的女生人数
score_guang = 0 #广州女生体育成绩总分
score_shang = 0 #上海女生体育成绩总分
score_guang_average = 0 #广州女生体育成绩平均分
score_shang_average = 0 #上海女生体育成绩平均分
for i in range(len(list1)):
    if(list1[i][2] == "Guangzhou" and list1[i][3] == "girl"):
        if(list1[i][15]!="NULL"): #符合条件的广州有体育成绩的女生
            guang_girl_num += 1
            if(list1[i][15]=="excellent"):
                score_guang += 90
            elif(list1[i][15]=="good"):
                score_guang += 80
            elif(list1[i][15]=="general"):
                score_guang += 70
            elif(list1[i][15]=="bad"):
                score_guang += 60
    elif(list1[i][2] == "Shanghai" and list1[i][3] == "girl"):
        if (list1[i][15] != "NULL"): #符合条件的上海有体育成绩的女生
            shang_girl_num += 1
            if (list1[i][15] == "excellent"):
                score_shang += 90
            elif (list1[i][15] == "good"):
                score_shang += 80
            elif (list1[i][15] == "general"):
                score_shang += 70
            elif (list1[i][15] == "bad"):
                score_shang += 60

score_guang_average = "%.2f" % float(score_guang/guang_girl_num) #计算平均分
score_shang_average = "%.2f" % float(score_shang/shang_girl_num)

print("广州的女生的平均体育成绩为",score_guang_average)
print("上海的女生的平均体育成绩为",score_shang_average)
if(score_guang_average > score_shang_average):
    print("从上面可以知道，广州女生的平均体育成绩更高一些！")
elif(score_guang_average == score_shang_average):
    print("从上面可以知道，广州与上海女生的平均体育成绩一样！")
else:
    print("从上面可以知道，上海女生的平均体育成绩更高一些！")
print()


# 4. 学习成绩和体能测试成绩，两者的相关性是多少？（九门课的成绩分别与体能成绩计算相关性）
sum = [0,0,0,0,0,0,0,0,0,0]  #用来存放各科成绩的总和，包括课程c1到c9，以及体育成绩
sum_average = [0,0,0,0,0,0,0,0,0,0] #各科的平均成绩
double_sum = [0,0,0,0,0,0,0,0,0,0] #平方和
standard = [0,0,0,0,0,0,0,0,0,0]  #标准差
p=[0,0,0,0,0,0,0,0,0]  #相关系数
X_EX=[0,0,0,0,0,0,0,0,0]

#计算各科的总分 C1到C9，C10的都是null，不计算
for i in range(len(list1)):
    for j in range(5,14):
        if(list1[i][j]!="NULL"):
            sum[j-5] += float(list1[i][j])  #减5的原因是与列表对应上

for i in range(len(list1)):
    if(list1[i][15] != "NULL"):
        if(list1[i][15] == "excellent"):
            sum[-1] += 90
        elif(list1[i][15] == "good"):
            sum[-1] += 80
        elif(list1[i][15] == "general"):
            sum[-1] += 70
        elif(list1[i][15] == "bad"):
            sum[-1] += 60



#平均成绩
for i in range(10):
    sum_average[i] = "%.5f" % float(sum[i]/len(list1))  #平均成绩
    if(i == 9):
        print("体育成绩的平均分为：",sum_average[9])
    else:
        print("C",i,"科目的平均成绩为 ",sum_average[i],"分",sep = "")
print()

#9门成绩成绩的平方和
for i in range(len(list1)):
    for j in range(5,14):
        if(list1[i][j] != "NULL"):
            double_sum[j-5] += ((float(list1[i][j]) - float(sum_average[j-5]))**2)
        else:
            double_sum[j-5] += (float(sum_average[j-5])**2)

#体能测试成绩平方和
for i in range(len(list1)):
    if(list1[i][15] == "excellent"):
        double_sum[-1] += (90-float(sum_average[-1]))**2
    elif(list1[i][15] == "good"):
        double_sum[-1] += (80-float(sum_average[-1]))**2
    elif (list1[i][15] == "general"):
        double_sum[-1] += (70-float(sum_average[-1]))**2
    elif(list1[i][15] == "bad"):
        double_sum[-1] += (60-float(sum_average[-1]))**2
    else:
        double_sum[-1] += (float(sum_average[-1]))**2


#9门课程学习成绩及体能测试成绩的标准差
for i in range(len(double_sum)):
    standard[i]='%.4f' % (math.sqrt(double_sum[i]/(len(list1)-1)))  #在指导书上的公式
    # if(i==0):
    #     print('9门课程成绩的标准差:',standard[i])
    # elif(i==9):
    #     print('体能测试成绩的标准差：',standard[i],'\n')
    # else:print('                ',standard[i])
    if(i==9):
        print("体能成绩的标准差为： ",standard[i])
    else:
        print("C",i+1,"课程成绩的标准差为： ",standard[i],sep='')
print()

#(x-E(x))*(y-E(y))的和
for i in range(len(list1)):
    for y in range(5,14):
        if(list1[i][y]!='NULL'):
            c=float(list1[i][y])-float(sum_average[y-5]) #公式的运用
        else:
            c=0-float(sum_average[y-5])
        if(list1[i][15]=='excellent'):
            g=90-float(sum_average[9])
        elif(list1[i][15]=='good'):
            g=80-float(sum_average[9])
        elif(list1[i][15]=='general'):
            g=70-float(sum_average[9])
        elif(list1[i][15]=='bad'):
            g=60-float(sum_average[9])
        else:
            g=0-float(sum_average[9])
        X_EX[y-5]+=c*g

#计算9对数据的相关系数
for i in range(len(X_EX)):
    p[i]='%.6f' % (X_EX[i]/((len(list1)-1)*float(standard[i])*float(standard[9]))) #套公式
    print("C",i,"课程学习成绩跟体能成绩的相关系数：  ",p[i],sep="")
    if(i==8):
        print()
print('综上，学习成绩与体能测试成绩相关性如下：')
for i in range(len(p)):
    if(float(p[i])>0):
        if(float(p[i])<0.3):
            print('C',i+1,'的学习成绩跟体能测试成绩无直线相关！')
        elif(0.3<=float(p[i])<0.5):
            print('C',i+1,'的学习成绩跟体能测试成绩低度相关！')
        elif(0.5<float(p[i])<0.8):
            print('C',i+1,'的学习成绩跟体能测试成绩中度相关！')
        else:
            print('C',i+1,'的学习成绩跟体能测试成绩高度相关！')
    else:
        if(-float(p[i])<0.3):
            print('C',i+1,'的学习成绩跟体能测试成绩无直线相关！')
        elif(0.3<=-float(p[i])<0.5):
            print('C',i+1,'的学习成绩跟体能测试成绩低度相关！')
        elif(0.5<-float(p[i])<0.8):
            print('C',i+1,'的学习成绩跟体能测试成绩中度相关！')
        else:
            print('C',i+1,'的学习成绩跟体能测试成绩高度相关！')