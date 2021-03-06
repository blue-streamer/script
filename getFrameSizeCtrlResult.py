import os
import sys
import csv
import numpy as np

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
header = []
for anchorRow, testRow in zip(anchorReader, testReader):
    if anchorRow[0] == sequenceStart:
        resultWriter.writerow(anchorRow)
        continue

    if anchorRow[0] == headerStart:
        curRow = anchorRow[:]
        header = anchorRow[2:]
        for times in range(2):
            curRow.append(" ")
            curRow.extend(header[:])
        resultWriter.writerow(curRow)
        continue
    
    curRow = anchorRow.copy()
    curRow.append(" ")
    curRow.extend(testRow[2:])
    curRow.append(" ")
    if len(resultSet) == 0:
        for data in anchorRow[2:]:
            resultSet.append([])

    for anchorData, testData, resultList in zip(anchorRow[2:], testRow[2:], resultSet):
        result = 0
        if float(anchorData) > 0.001:
            result = (float(testData) - float(anchorData)) / float(anchorData)
        
        resultList.append(result)
        curRow.append("%.3f"%(result))
    
    resultWriter.writerow(curRow)
   

leadingBlank = 2 + len(resultSet) + 1 + len(resultSet) + 1
finalRowHeader = [" "] * leadingBlank
finalRowHeader.extend(header)
resultWriter.writerow(finalRowHeader)

finalRow = [" "] * leadingBlank
for resultList in resultSet:
    resultArr = np.array(resultList)
    finalRow.append("%.3f%%"%(resultArr.mean()*100))
resultWriter.writerow(finalRow)

anchorFile.close()
testFile.close()
resultFile.close()










