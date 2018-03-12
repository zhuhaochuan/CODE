 # coding=<encoding name> 例如，可添加# coding=utf-8
from __future__ import print_function
import pandas as pd
import numpy as np
from scipy import  stats
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt

def nums_of_month(path):
    f = open(path)

    line = f.readline()

    kind = []
    date = []
    mymap = {}

    while line:
        a = line.split()
        temp = a[1].split('r')
        kind.append(temp[1])
        date.append(a[2])
        line = f.readline()


    dic = {}
    for i in range(1,16):
        a = str(i)
        dic[a] = 0

    nums = []
    temp = date[0]
    i = 0
    nums.append(0)
    dates = []
    dates.append('01')
    for each in date:
        if (each==temp) :
            nums[i] = nums[i] + 1
        else :
            d = each.split('-')
            dates.append(d[1]+d[2])
            nums.append(1)
            temp = each
            i = i+1
    f.close()
    return nums
def draw_pic(nums):
    plt.figure()
    plt.plot(nums)
    #plt.grid(True) #增加格点
    plt.xlabel('dates')
    plt.ylabel('nums')
    #plt.title(month + '-flavor' + kind_choose)
    plt.plot(nums,'b',lw = 1.5) # 蓝色的线
    plt.plot(nums,'ro') #离散的点
    plt.show()
    #plt.savefig('pic/' + month + '/' + month + '-flavor' + kind_choose + ".jpg")

path = "数据/data1.txt"
nums = nums_of_month(path)

#draw_pic(nums)
#print(nums)

#得到一个月的每日虚拟机个数图像
dta=pd.Series(nums)
print(dta)
dta.index = pd.Index(sm.tsa.datetools.dates_from_range('2001','2024'))

print(dta)
#print(dta)
dta.plot()
#draw_pic(dta)

#一阶差分 后一天的数量减去前一天的数量
plot_acf(dta)
plot_pacf(dta)
dta=np.array(dta,dtype=np.float)
arma_mod30 = sm.tsa.ARMA(dta, (3,0)).fit(disp=False)

sm.stats.durbin_watson(arma_mod30.resid)
#print(arma_mod30.aic,arma_mod30.bic,arma_mod30.hqic)

resid = arma_mod30.resid#残差
stats.normaltest(resid)
plot_acf(resid.squeeze())
plot_pacf(resid)


#print(sm.stats.durbin_watson(arma_mod30.resid))

fig = plt.figure()
ax = fig.add_subplot(111)
fig = qqplot(resid, line='q', ax=ax, fit=True)

r,q,p = sm.tsa.acf(resid.squeeze(), qstat=True)
data = np.c_[range(1,24), r[1:], q, p]
table = pd.DataFrame(data, columns=['lag', "AC", "Q", "Prob(>Q)"])
#print(table.set_index('lag'))
#模型预测
predict_sunspots = arma_mod30.predict('2015', '2020', dynamic=True)



plt.show()
