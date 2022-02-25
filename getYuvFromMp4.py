#coding=utf-8
import os
import sys
import subprocess
import re


def subprocessPopen(statement):
    p = subprocess.Popen(statement, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # 执行shell语句并定义输出格式
    while p.poll() is None:  # 判断进程是否结束（Popen.poll()用于检查子进程（命令）是否已经执行结束，没结束返回None，结束后返回状态码）
        if p.wait() != 0:  # 判断是否执行成功（Popen.wait()等待子进程结束，并返回状态码；如果设置并且在timeout指定的秒数之后进程还没有结束，将会抛出一个TimeoutExpired异常。）
            print("command is failed", statement)
            return False, []
        else:
            re = p.stderr.readlines()  # 获取原始执行结果
            result = []
            for i in range(len(re)):  # 由于原始结果需要转换编码，所以循环转为utf8编码并且去除\n换行
                res = re[i].decode('utf-8').strip('\r\n')
                result.append(res)
            return True, result

fileDir = "./douyin_linkmic_effect/"
yuvFileDir = "./douyin_linkmic_effect_yuv/"
files = os.listdir(fileDir)
fileCount = 0
for file in files:
    fileSplit = file.split(".")
    if len(fileSplit) <= 0:
        print("file name is abnormal", file)
        break
    filePrefix = fileSplit[0]
    cmd = "ffprobe " + fileDir+file
    success, result = subprocessPopen(cmd)
    if success:
        pattern = r'Stream.*: Video: '
        resolution = ""
        frameRate = ""
        for line in result: 
            searchObjLine = re.search(pattern, line)
            if searchObjLine:
                resolutionPattern = r'(\d+x\d+),'
                frameRatePattern =r'(\d+)(\.*\d*) fps,'
                resolutionResult = re.search(resolutionPattern, line)
                if resolutionResult:
                    resolution = resolutionResult.group(1)
                else:
                    print("can not get resolution, searchLine:", line)
                
                frameRateResult = re.search(frameRatePattern, line)
                if frameRateResult:
                    frameRate = frameRateResult.group(1)
                else:
                    print("can not get frameRate, searchLine:", line)
                
                break
        
        if resolution == "" or frameRate == "":
            print("do not get yuv info", file)
            break

        if not os.path.exists(yuvFileDir + resolution):
            os.makedirs(yuvFileDir + resolution)

        currentYuvFileDir = yuvFileDir + resolution + "/"
        subfix = resolution + "_" + frameRate

        filePrefixSplit = filePrefix.split("_")
        yuvFile = ""
        if len(filePrefixSplit) >=2 :
            for item in filePrefixSplit[:-1]:
                yuvFile += item + "_"
            
            yuvFile += subfix + ".yuv"
        else:
            print("current file prefix is abnormal:", filePrefix)
            break
    else:
        print("probe info failed!")
        break
        
    cmd = "ffmpeg -i " + fileDir + file + " -vcodec rawvideo -an " + currentYuvFileDir + yuvFile
    success, result = subprocessPopen(cmd)
    fileCount += 1
    print ("finish file:", fileCount)
    if success == False:
        print("decode fail")
        print(result)
        break