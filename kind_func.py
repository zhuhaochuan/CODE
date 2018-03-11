import matplotlib.pyplot as plt

def count_kind_num(path,month,kind_choose):
	f = open(path)
	line = f.readline()

	kind = []
	date = []
	#month = '2015-01'
	#kind_choose = '2'

	while line:
	    a = line.split()
	    temp = a[1].split('r')
	    #print(a[2].split('-'))
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
	return dates,nums
def draw_pic(dates,nums,month,kind_choose):
	plt.figure()
	plt.plot(dates,nums)
	plt.grid(True) #增加格点
	plt.xlabel('dates')
	plt.ylabel('nums')
	plt.title(month + '-flavor' + kind_choose)
	plt.show()

path = "数据/data2.txt"
month = '2015-01'
#kind_choose = '2'

#[dates,nums] = count_kind_num(path,month,kind_choose)
#draw_pic(dates,nums,month,kind_choose)

for i in range(1,16):
	[dates,nums] = count_kind_num(path,month,kind_choose = str(i))
	#draw_pic(dates,nums,month,kind_choose = str(i))
	print(sum(nums))
	#print(len(dates))
	print(sum(nums)/len(dates))