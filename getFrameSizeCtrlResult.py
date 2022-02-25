import os
import sys
import csv
import np

if len(sys.argv) < 3:
    print("do not have enough params!")
    exit()

anchor = sys.argv[1]
test = sys.argv[2]
print("anchor:%s, test:%s"%(anchor, test))

if not os.path.exists(anchor):
    print("%s is not exist!"%(anchor))
    exit()

if not os.path.exists(test):
    print("%s is not exist!"%(test))
    exit()

anchorFile = open(anchor)
anchorReader = csv.reader(anchorFile, delimiter=',')
testFile = open(test)
testReader = csv.reader(testFile, delimiter=',')
resultFile = open("result.csv", "w")
resultWriter = csv.writer(resultFile)
resultSet = []


sequenceStart = "testSequence"
headerStart = "frameSizeLimit"
for anchorRow, testRow in zip(anchorReader, testReader):
    if anchorRow[0] == sequenceStart:
        resultWriter.writerow(anchorRow)
        continue

    if anchorRow[0] == headerStart:
        curRow = anchorRow[:]
        for times in range(2):
            curRow.append(" ")
            for item in anchorRow[2:]:
                curRow.append(item)
        resultWriter.writerow(anchorRow)
        continue

    curRow = anchorRow.copy()
    curRow.append(" ")
    curRow.append(testRow)
    curRow.append(" ")
    if len(resultSet) == 0:
        for data in anchorRow[2:]:
            resultSet.append([])

    for anchorData, testData, resultList in zip(anchorRow[2:], testRow[2:], resultSet):
        result = 0
        if int(anchorData) != 0:
            result = (float(testData) - float(anchorData)) / float(anchorData)
        
        resultList.append(result)
        curRow.append("%.3f"%(result))
    
    resultWriter.writerow(curRow)

finalRow = []
leadingBlank = 2 + len(resultSet) + 1 + len(resultSet)
for idx in range(leadingBlank):
    finalRow.append(" ")

for resultList in resultSet:
    resultArr = np.array(resultList)
    finalRow.append(resultArr.mean())

resultWriter.writerow(finalRow)
anchorFile.close()
testFile.close()
resultFile.close()










