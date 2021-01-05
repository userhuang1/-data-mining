import matplotlib.pyplot as plt
import numpy as np

# 防止乱码
plt.rcParams['font.sans-serif']=['SimHei']

# 为保证各类颜色相同，定义一个颜色数组
color = ['green', 'yellow', 'red', 'black', 'blue', 'orange']  #定义几种不同的颜色用于显示区别（结果）

flie1 = open("test_3.txt") #打开文件

line = "1"
list1 = []

# 读取文件内容到data[]数组中
while line:
    line = flie1.readline()  #读取每一行
    if line:
        int_data = [float(i) for i in (line.replace("\n","").split(' ', 6))]   #删除掉换行符\n，并且根据" "(空格）进行6次切割
        list1.append(int_data)   #存入数据到列表中

Data = np.array(list1)  #转为矩阵

maxClass = np.max(Data[:,2])           # 类数目k

indexClass = Data[:,2]      # 类索引

x = [0,0,0,0,0,0]   # 类质心x
y = [0,0,0,0,0,0]   # 类质心y
for i in range(len(list1)):
    cur = int(list1[i][2])
    x[cur] = float(list1[i][4])   #输入数据到x列表中
    y[cur] = float(list1[i][5])   #输入数据到y列表中


Radius = [0.0,0.0,0.0,0.0,0.0]       # 定义半径
# 找该类的半径
for i in range(len(list1)):
    cur = int(list1[i][2])
    distance = float(list1[i][3])
    if distance>Radius[cur]:   #判断当前值与距离的大小
        Radius[cur] = distance    #查找最大的半径


# 画图
def plot(maxClass,x_centerClass,y_centerClass):
    # 初始坐标列表
    x = []
    y = []
    for i in range(int(maxClass)+1):
        x.append([])
        y.append([])

    # 填充坐标 并绘制散点图
    for j in range(int(maxClass)+1):
        for i in range(len(indexClass)):
            if int(indexClass[i])== j:
                x[j].append(list1[i][0])
                y[j].append(list1[i][1])

        '''
            其中scatter的参数的意思，c代表的是显示出来的颜色，因为这一题需要从图中明显的看出聚类的结果，所以这里采用的是一个颜色数组，
            包含不同的颜色，用于区分不同的聚类半径。
            marker是显示的图标形状，o是默认值。
        '''
        plt.scatter(x[j], y[j], c=color[j],marker='o',label=("类别%d" % (j + 1)))

        if(j==(maxClass - 1)):
            plt.scatter(x_centerClass[j], y_centerClass[j], c='red', marker='*', label="中心点")  # 画聚类中心
        else:
            plt.scatter(x_centerClass[j], y_centerClass[j], c='red', marker='*')  # 画聚类中心
    # 画出类半径
    for i in range(int(maxClass)+1):
        # 定义圆心和半径
        x = x_centerClass[i]
        y = y_centerClass[i]
        r = Radius[i]
        # 点的横坐标为a
        a = np.arange(x - r, x + r, 0.0001)
        # 点的纵坐标减掉质心的y为b
        b = np.sqrt(abs(pow(r, 2) - pow((a - x), 2)))
        # 绘制上半部分
        plt.plot(a, y + b, color=color[i], linestyle='-')
        # 绘制下半部分
        plt.plot(a, y - b, color=color[i], linestyle='-')
    plt.scatter(2, 6, c='violet', marker='x', label="(2,6)")  # 画（2，6）
    # 设置标题
    plt.title('K-means聚类图')
    # 给图加上图例
    plt.legend()
    # 设置X轴标签
    plt.xlabel('X')
    # 设置Y轴标签
    plt.ylabel('Y')

    # 将生成的聚类表示图存入内存中
    plt.savefig("K-means聚类图")

    # 显示散点图
    plt.show()

plot(maxClass,x,y)  #调用自定义的函数

flie1.close()  #关闭文件