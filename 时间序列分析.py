from __future__ import print_function
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt

import statsmodels.api as sm

from statsmodels.graphics.api import qqplot
#print(sm.datasets.sunspots.NOTE)

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
dta=pd.Series(nums)
#dta = sm.datasets.sunspots.load_pandas().data

dta.index = pd.Index(sm.tsa.datetools.dates_from_range('1701', '1724'))
#del dta["YEAR"]

dta.plot();

print(dta.values)
print(type(dta.values))

temp = dta.values.reshape(24,1)

fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(temp.squeeze(), lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(dta, lags=40, ax=ax2)
arma_mod20 = sm.tsa.ARMA(dta, (2,0)).fit(disp=False)
print(arma_mod20.params)
arma_mod30 = sm.tsa.ARMA(dta, (3,0)).fit(disp=False)

plt.show()
