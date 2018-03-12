from __future__ import print_function
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot


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

#读取数据的路径
path = "数据/data1.txt"

nums = nums_of_month(path)
#得到数据的长度
l = len(nums)

#将nums转换为dta的数据类型
dta = sm.datasets.sunspots.load_pandas().data
dta = dta[1:l+1]
dta.index = pd.Index(sm.tsa.datetools.dates_from_range('2001', '2024'))
i = 0
for each in nums:
    dta.values[i][1] = each
    i = i + 1

del dta["YEAR"]

#得到原始数据图像
#dta.plot();

#得到自相关图和偏自相关图
#plot_acf(dta)
#plot_pacf(dta)

arma_mod10 = sm.tsa.ARMA(dta, (1,0)).fit(disp=False)
arma_mod20 = sm.tsa.ARMA(dta, (2,0)).fit(disp=False)
arma_mod30 = sm.tsa.ARMA(dta, (3,0)).fit(disp=False)
arma_mod40 = sm.tsa.ARMA(dta, (4,0)).fit(disp=False)
arma_mod50 = sm.tsa.ARMA(dta, (5,0)).fit(disp=False)
arma_mod60 = sm.tsa.ARMA(dta, (6,0)).fit(disp=False)
arma_mod70 = sm.tsa.ARMA(dta, (7,0)).fit(disp=False)

con = []
con.append(arma_mod10)
con.append(arma_mod20)
con.append(arma_mod30)
con.append(arma_mod40)
con.append(arma_mod50)
con.append(arma_mod60)
con.append(arma_mod70)


for each in con:
    print(each.aic, each.bic, each.hqic)

for each in con:
    print(sm.stats.durbin_watson(each.resid))



#arma_mod10 = sm.tsa.ARMA(dta, (7,0)).fit(disp=False)
#print(arma_mod10.aic, arma_mod10.bic, arma_mod10.hqic)
#print(sm.stats.durbin_watson(arma_mod10.resid))



resid = arma_mod10.resid
r,q,p = sm.tsa.acf(resid.squeeze(), qstat=True)
data = np.c_[range(1,24), r[1:], q, p]
table = pd.DataFrame(data, columns=['lag', "AC", "Q", "Prob(>Q)"])
#print(table.set_index('lag'))

#plot_acf(resid.squeeze())
#plot_pacf(resid)

#print(arma_mod30)
predict_sunspots = arma_mod10.predict('2014', '2024', dynamic=True)
print(predict_sunspots)


fig, ax = plt.subplots()
ax = dta.ix['2001':].plot(ax=ax)
predict_sunspots.plot(ax=ax)


plt.show()
