import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm

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

#for each in kind:
#    print(each)

#for each in date:
#    print(each)


#print(nums)
#print(dates)

#f.close()
#plt.figure()
#plt.plot(dates,nums)
#plt.show()

dta = pd.Series(nums)
#print(dta)
#dta.index-pd.Index(sm.tsa.datetools.dates_from_range('01','24'))
#plt.figure()
#plt.plot(dta)
#plt.show()

#fig = plt.figure(figsize=(12, 8))
#ax1 = fig.add_subplot(111)

#the following code is for draw diff graph

diff1 = dta.diff(1)
plt.figure()
plt.plot(diff1)
plt.show()

diff2 = dta.diff(2)
plt.figure()
plt.plot(diff2)
plt.show()

diff3 = dta.diff(3)
plt.figure()
plt.plot(diff3)
plt.show()

f.close()
