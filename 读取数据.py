import matplotlib.pyplot as plt
f = open("数据/data_all.txt")

line = f.readline()

kind = []
date = []
mymap = {}

while line:
    a = line.split()
    temp = a[1].split('r')
    kind.append(temp[1])
    print(len(kind))
    #date.append(a[2])
    line = f.readline()


f.close()

plt.figure()
plt.plot(nums)
plt.show()