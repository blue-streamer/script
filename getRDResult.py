#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import numpy as np
import xlwings as xw
import math

def getResult0(anchor, test, wb):
    print ("anchor:", anchor)
    print ("test:", test)
    anchorFile=open(anchor,"r")
    testFile=open(test,"r")
    ancLines=anchorFile.readlines()
    testLines=testFile.readlines()
    dataLen = len(ancLines)

    startRow = 3
    currentRow=startRow
    sheet = wb.sheets[0]
    for i in range(0, dataLen):
        oneList_anchor=ancLines[i].split(",")
        oneList_test=testLines[i].split(",")
        #copy name
        name = oneList_anchor[0]
        pos="B"+str(currentRow)
        sheet.range(pos).value = name
        #copy data
        newList_anchor=oneList_anchor[1:len(oneList_anchor)-1]
        newList_test=oneList_test[1:len(oneList_test)-1]
        newList_anchor.append(" ")
        newList_anchor.extend(newList_test)
        #print (newList_anchor)
        pos="D"+str(currentRow)
        sheet.range(pos).value = newList_anchor

        currentRow = currentRow + 1 

    anchorFile.close()
    testFile.close()



def getResult(anchor, test, wb, sheetDataLength):
    print ("anchor:", anchor)
    print ("test:", test)
    anchorFile=open(anchor,"r")
    testFile=open(test,"r")
    ancLines=anchorFile.readlines()
    testLines=testFile.readlines()
    dataLen = len(ancLines)

    startRow=4
    currentRow=startRow
    sheetIdx=0
    sheet = wb.sheets[sheetIdx]
    for i in range(0, dataLen):
        if currentRow - startRow >= sheetDataLength * 4:
            sheetIdx += 1
            sheet = wb.sheets[sheetIdx]
            currentRow = startRow
            print("change to sheet ", str(sheetIdx))
        oneList_anchor=ancLines[i].split(",")
        oneList_test=testLines[i].split(",")
        #copy name
        name = oneList_anchor[0]
        pos="C"+str(currentRow)
        sheet.range(pos).value = name
        #copy data
        newList_anchor=oneList_anchor[1:len(oneList_anchor)-1]
        newList_test=oneList_test[1:len(oneList_test)-1]
        newList_anchor.append(" ")
        newList_anchor.extend(newList_test)
        print (newList_anchor)
        pos="E"+str(currentRow)
        sheet.range(pos).value = newList_anchor
        currentRow=currentRow+1
        

    anchorFile.close()
    testFile.close()

def createOriginBookAndGetResult(anchor, test, template):
    app = xw.App(visible=False)
    wb = app.books.open(template)
    #open anchor and test File
    dataLen=137
    sheetDataLength=16
    
    sheetNamePrefix='sheet'
    sheetNum = len(wb.sheets)
    if sheetNum == 0:
        print("empty template!")
        return
    while sheetNum < math.ceil(dataLen * 1.0 / sheetDataLength):
        wb.sheets[0].copy(after=wb.sheets[-1], name=sheetNamePrefix+str(sheetNum))
        sheetNum += 1
    
    getResult(anchor, test, wb)
    wb.api.save(timeout=3000)
    app.kill()

#def copyBookAndGetResult(anchor, test, templ):
#def copyBookAndGetResult(anchor, test, template, newResult):
def copyBookAndGetResult(anchor, test, template):
    newResult = anchor.split(".")[0] + "VS" + test.split(".")[0]
    print("resultFile:", newResult)
    os.system("cp " + template + " " + newResult + ".xlsm")
    app = xw.App(visible=False)
    #app = xw.App(visible=True)
    curBook = app.books.open(newResult + ".xlsm")

    #getResult(anchor, test, curBook, 16)
    getResult0(anchor, test, curBook)
    curBook.api.save(timeout=3000)
    print("finish!")
    #app.kill()

if __name__ == '__main__':
    #argv: anchor test template resultName
    #createOriginBookAndGetResult(sys.argv[1], sys.argv[2], sys.argv[3])
    #copyBookAndGetResult(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    copyBookAndGetResult(sys.argv[1], sys.argv[2], sys.argv[3])
