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
path = "数据/TrainData_2015.1.1_2015.2.19.txt"

nums = nums_of_month(path)
#得到数据的长度
l = len(nums)
print(l)
#将nums转换为dta的数据类型
dta = sm.datasets.sunspots.load_pandas().data
dta = dta[1:l+1]
dta.index = pd.Index(sm.tsa.datetools.dates_from_range('2001', '20'+str(l)))
i = 0
for each in nums:
    dta.values[i][1] = each
    i = i + 1
del dta["YEAR"]
print(dta)
#得到原始数据图像
#dta.plot();

#得到自相关图和偏自相关图
#plot_acf(dta)
#plot_pacf(dta)

'''
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
'''
score = []
#for i in range(0,3):

#采用模型 设计参数
arma_mod10 = sm.tsa.ARMA(dta, (7,3)).fit(disp=False)
#print(arma_mod10.aic, arma_mod10.bic, arma_mod10.hqic)
#残差
#print(sm.stats.durbin_watson(arma_mod10.resid))

#残差图像
#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax = arma_mod10.resid.plot(ax=ax);

resid = arma_mod10.resid
#print(stats.normaltest(resid))

#判断是否是正态分布
#fig = plt.figure()
#ax = fig.add_subplot(111)
#fig = qqplot(resid, line='q', ax=ax, fit=True)

#残差的相关图
#plot_acf(resid.values.squeeze())
#plot_pacf(resid)


#r,q,p = sm.tsa.acf(resid.squeeze(), qstat=True)
#data = np.c_[range(1,126), r[1:], q, p]
#table = pd.DataFrame(data, columns=['lag', "AC", "Q", "Prob(>Q)"])
#print(table.set_index('lag'))

#预测结果
predict_sunspots = arma_mod10.predict('2042', '20'+str(l), dynamic=True)
#predict_sunspots = arma_mod10.predict('20'+str(l), '2049', dynamic=True)
print(predict_sunspots)

fig, ax = plt.subplots(figsize=(12, 8))
ax = dta.ix['2001':].plot(ax=ax)
fig = arma_mod10.plot_predict('2042', '20'+str(l), dynamic=True, ax=ax, plot_insample=False)
#fig = arma_mod10.plot_predict('20'+str(l), '2049', dynamic=True, ax=ax, plot_insample=False)



#计算误差的均值和方差
def mean_forecast_err(y, yhat):
    return y.sub(yhat).mean()

def var_forecast_err(y, yhat):
    return y.sub(yhat).var()

#print(mean_forecast_err(dta.SUNACTIVITY, predict_sunspots))
#print(var_forecast_err(dta.SUNACTIVITY, predict_sunspots))
#print(dta.SUNACTIVITY.sub(predict_sunspots)[17:25])

def score_of_pre(y, yhat):
    return 1-y.sub(yhat).std()/(y.std()+yhat.std())

score.append(score_of_pre(dta.SUNACTIVITY, predict_sunspots))
#print(score_of_pre(dta.SUNACTIVITY, predict_sunspots))

print(score)

plt.figure()
plt.plot(score)
#plt.grid(True) #增加格点
plt.xlabel('p')
plt.ylabel('score')
#plt.title(month + '-flavor' + kind_choose)
plt.plot(score,'b',lw = 1.5) # 蓝色的线
plt.plot(score,'ro') #离散的点
plt.show()










'''
from statsmodels.tsa.arima_process import arma_generate_sample, ArmaProcess
np.random.seed(1234)
# include zero-th lag
arparams = np.array([1, .75, -.65, -.55, .9])
maparams = np.array([1, .65])
arma_t = ArmaProcess(arparams, maparams)
print(arma_t.isinvertible)
print(arma_t.isstationary)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(arma_t.generate_sample(nsample=50));


arparams = np.array([1, .35, -.15, .55, .1])
maparams = np.array([1, .65])
arma_t = ArmaProcess(arparams, maparams)
print(arma_t.isstationary)

arma_rvs = arma_t.generate_sample(nsample=500, burnin=250, scale=2.5)
plot_acf(arma_rvs)
plot_pacf(arma_rvs)


arma11 = sm.tsa.ARMA(arma_rvs, (1,1)).fit(disp=False)
resid = arma11.resid
r,q,p = sm.tsa.acf(resid, qstat=True)
data = np.c_[range(1,25), r[1:], q, p]
table = pd.DataFrame(data, columns=['lag', "AC", "Q", "Prob(>Q)"])
print(table.set_index('lag'))

arma41 = sm.tsa.ARMA(arma_rvs, (4,1)).fit(disp=False)
resid = arma41.resid
r,q,p = sm.tsa.acf(resid, qstat=True)
data = np.c_[range(1,25), r[1:], q, p]
table = pd.DataFrame(data, columns=['lag', "AC", "Q", "Prob(>Q)"])
print(table.set_index('lag'))

macrodta = sm.datasets.macrodata.load_pandas().data
macrodta.index = pd.Index(sm.tsa.datetools.dates_from_range('1959Q1', '2009Q3'))
cpi = macrodta["cpi"]

fig = plt.figure()
ax = fig.add_subplot(111)
ax = cpi.plot(ax=ax);
ax.legend();

print(sm.tsa.adfuller(cpi)[1])
'''
#plt.show()
