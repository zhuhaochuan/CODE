import matplotlib.pyplot as plt

def count_kind_num(path,kind_choose):
	f = open(path)
	line = f.readline()

	kind = []
	date = []

	while line:
	    a = line.split()
	    temp = a[1].split('r')
	    kind.append(temp[1])
	    date.append(a[2])
	    line = f.readline()

	nums = []
	temp = date[0]
	i = 0
	nums.append(0)
	dates = []
	dates.append('01')
	j = 0

	for each in date :
	    if (each==temp) :
	        if(kind[j]==kind_choose) :
	            nums[i] = nums[i] + 1
	            j = j + 1
	        else :
	            j = j + 1
	    else :
	        nums.append(0)
	        d = each.split('-')
	        dates.append(d[2])
	        i = i + 1
	        if(kind[j]==kind_choose) :
	            nums[i] = nums[i] + 1
	            j = j + 1
	        else :
	            j = j + 1
	        temp = each
	f.close()
	return dates,nums,kind,date

def draw_pic(i,mean,kind):
	plt.figure()
	#plt.plot(i,mean)
	plt.grid(True) #增加格点
	plt.xlabel('month')
	plt.ylabel('mean')
	plt.title("mean of flavor" + kind)
	plt.plot(i,mean,'b',lw = 1.5) # 蓝色的线
	plt.plot(i,mean,'ro') #离散的点
	plt.show()

def mean_of_month(kind_choose,mean):
	for i in range(1,6):
		print(i)
		path = "数据/data" + str(i) + ".txt"
		[dates,nums,kind,date] = count_kind_num(path,kind_choose)
		mean.append(sum(nums)/len(dates))
	return mean

for i in range(1,16) :
	mean = []
	mean = mean_of_month(str(i),mean)
	print(mean)
	draw_pic([1,2,3,4,5],mean,str(i))









