import re
import matplotlib.pyplot as plt


testFile=open("test1.txt")
cpuStr = testFile.read()

testList=re.split(r'Processes:', cpuStr)
print "The number of cpu info is "+str(len(testList))
cpuNumList=[]
xIndex=[]

for item in testList:
    numberList=re.split(r'FeishuRooms-stag', item)
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

plt.plot(xIndex, cpuNumList)
plt.show()


