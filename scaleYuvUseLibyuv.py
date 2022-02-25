import os
import sys

org720pDir = "./douyin_linkmic_effect_yuv/720x1280/"
yuvconvertCmd = "./libyuv/cmake_build/linux/yuvconvert"
dir720p = "./douyin_linkmic_effect_yuv/selected_douyin_yuv/720x1280/"
dir360p = "./douyin_linkmic_effect_yuv/selected_douyin_yuv/360x640/"

fileList = os.listdir(org720pDir)
selectedFileCount = 10
fileCount = 0

for file in fileList:
    fileSplit = file.split(".")
    if len(fileSplit) != 2:
        print("abnormal file name", file)
        break   

    filePrefix = fileSplit[0]
    filePrefixLibyuv = filePrefix + "_P420"
    cmd = "cp " + org720pDir + file + " " + dir720p + filePrefixLibyuv + ".yuv"
    result = os.system(cmd)
    if result != 0:
        print("cp failed", cmd)
    
    fileCount += 1
    print("copy file", fileCount)
    if fileCount >= selectedFileCount:
        break

fileList720p = os.listdir(dir720p)

for file in fileList720p:
    fileSplit = file.split(".")
    if len(fileSplit) != 2:
        print("abnormal file name", file)
        break

    filePrefixSplit = fileSplit[0].split("_")
    if len(filePrefixSplit) < 4:
        print("abnormal file prefix", fileSplit[0])
        break

    cmd = yuvconvertCmd + " -s 720 1280 -d 360 640 -f 3 " + dir720p + file + " " + dir360p + "tmp_P420.yuv"
    result = os.system(cmd)
    if result != 0:
        print("convert failed", cmd)
        break

    filePrefix = ""
    for item in filePrefixSplit[:-3]:
        filePrefix += item + "_"
    
    filePrefix += "360x640_"
    filePrefix += filePrefixSplit[-2]
    
    cmd = "mv " + dir360p + "tmp_P420.yuv " + dir360p + filePrefix + ".yuv"
    result = os.system(cmd)
    if result != 0:
        print("360p mv failed", cmd)
        break

for file in fileList720p:
    fileSplit = file.split(".")
    if len(fileSplit) != 2:
        print("abnormal file name", file)
        break

    filePrefixSplit = fileSplit[0].split("_")
    if len(filePrefixSplit) < 4:
        print("abnormal file prefix", fileSplit[0])
        break

    filePrefix = ""
    for item in filePrefixSplit[:-2]:
        filePrefix += item + "_"
    filePrefix += filePrefixSplit[-2] 
    
    cmd = "mv " + dir720p + file + " " + dir720p + filePrefix + ".yuv"
    result = os.system(cmd)
    if result != 0:
        print("720p mv failed", cmd)
        break

