import re
import matplotlib.pyplot as plt
import numpy as np


testFile=open("top_record.txt")
cpuStr = testFile.read()

testList=re.split(r'Processes:', cpuStr)
print "The number of cpu info is "+str(len(testList))
cpuNumList=[]
xIndex=[]

for item in testList:
    numberList=re.split(r'Feishu-prereleas', item)
    #print len(numberList)
    currentCpu=0
    for i in range(len(numberList)):
        if i==0:
            continue
        #print numberList[i]
        #print "==========="
        numberMatch=re.match(r'\s*(\d*\.*\d*)', numberList[i])
        if numberMatch:
            currentCpu += float(numberMatch.group(1))

    xIndex.append(len(cpuNumList))
    cpuNumList.append(currentCpu)


print "cpuNumList len "+str(len(cpuNumList))
print "xIndex len "+str(len(xIndex))
print "average cpu:"+str(np.mean(cpuNumList))

mean_value = np.mean(cpuNumList)
mean_list = []
for item in xIndex :
    mean_list.append(mean_value)

plt.plot(xIndex, cpuNumList, "blue")
plt.plot(xIndex, mean_list, "red")
plt.show()


