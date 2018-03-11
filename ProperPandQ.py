import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf


f = open("E:\HUAWEICodeCraft\Data\data_2015_1.txt")

line = f.readline()

#print(type(line))
kind = []
date = []
mymap = {}

while line:
    a = line.split()
    temp = a[1].split('r')
    #print(a[2].split('-'))
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

dta = pd.Series(nums)
dta.index = pd.Index(sm.tsa.datetools.dates_from_range('2001', '2024'))
#print(dta)
#print(dates)

'''
fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(dta, lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(dta, lags=40, ax=ax2)

plot_acf(dta)
plt.show()

plot_pacf(dta)
plt.show()
'''

dta = np.array(dta, dtype=np.float)
arma_mod20 = sm.tsa.ARMA(dta, (1, 2)).fit()
print(arma_mod20.aic, arma_mod20.bic, arma_mod20.hqic)
