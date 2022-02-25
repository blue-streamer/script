import os
import sys
import re
import subprocess

hlsList = [
    "http://pull-hls-l11-admin.douyincdn.com/stage/stream-397398652089794705/timeshift.m3u8?starttime_epoch=1626743979&endtime_epoch=1626753219&session_id=202107221505430102112211410466BA9A",
    "http://pull-hls-l1-admin.douyincdn.com/stage-stream-109170437111676958.m3u8?wsStart=1626772421&wsEnd=1626776353&session_id=202107221506400102112211410466D23B",
    "http://pull-hls-f5.douyincdn.com/stage/stream-685631253976449125/index.m3u8?start=1626768298&end=1626770448&session_id=202107221507380102112211410466E9A4",
    "http://pull-hls-l11-admin.douyincdn.com/stage/stream-397397068120064145/timeshift.m3u8?starttime_epoch=1626712400&endtime_epoch=1626713325&session_id=202107221508250102112211410466FFBD", 
    "http://pull-hls-f5.douyincdn.com/stage/stream-109165388713164901/index.m3u8?start=1626714064&end=1626714884&session_id=20210722150929010211221141046717D2",
    "http://pull-hls-f5.douyincdn.com/stage/stream-109170255515615333/index.m3u8?start=1626765813&end=1626766559&session_id=20210722151003010211221141046721C5",
    "http://pull-hls-f5.douyincdn.com/stage/stream-685632220345139301/index.m3u8?start=1626787371&end=1626788002&session_id=20210722151204010211221141046752DE",
    "http://pull-hls-f5.douyincdn.com/stage/stream-397400816086155365/index.m3u8?start=1626768006&end=1626768580&session_id=202107221512380102112211410467614E",
    "http://pull-hls-f5.douyincdn.com/stage/stream-685629872942874725/index.m3u8?start=1626751549&end=1626752112&session_id=2021072215132101021122114104677083",
    "http://pull-hls-l11-admin.douyincdn.com/stage/stream-109171835660927121/timeshift.m3u8?starttime_epoch=1626790666&endtime_epoch=1626791163&session_id=2021072215134801021122114104677B44",
]

hlsList0 = [
    #"http://pull-hls-l11-admin.douyincdn.com/stage/stream-397398652089794705/timeshift.m3u8?starttime_epoch=1626743979&endtime_epoch=1626753219&session_id=202107221505430102112211410466BA9A",
    r'http://pull-hls-l11-admin.douyincdn.com/stage/stream-397398652089794705/timeshift.m3u8?starttime_epoch=1626743979&endtime_epoch=1626753219&session_id=202107221505430102112211410466BA9A',
]



#use ffmpeg download and save as hevc
for idx in range(len(hlsList)):
    print("process:", idx)
    hls = hlsList[idx]
    prefix = "hls" + str(idx)
    hevcFile = prefix + ".265"
    yuvFile = prefix + ".yuv"
    paramFile = "params.txt"
    yuvDir = "./decodeYuv/"
    cmd = ["ffmpeg", "-i", hls, "-t", "00:03:00", "-c", "copy", hevcFile]
    print("ffmpeg cmd:", cmd)
    ps = subprocess.Popen(cmd)
    ps.wait()
    if os.path.exists(hevcFile):
        cmd = "./ByteVC1_dec -i " + hevcFile + " -o " + yuvFile
        print("decode cmd:", cmd)
        subprocess.call(cmd, shell=True)
        if os.path.exists(yuvFile) and os.path.exists(paramFile):
            fileParam = open(paramFile, "r")
            lines = fileParam.readlines()
            if len(lines) == 0:
                print("param file is empty!")
                continue
            firstLine = lines[0]
            for line in lines[1:]:
                if line != firstLine:
                    print("resolution changed!")
                    continue
            matchObj = re.match(r'(\d+)x(\d+)', firstLine)
            width = 0
            height = 0
            if matchObj:
                width = int(matchObj.group(1))
                height = int(matchObj.group(2))
                print("Get size from param, width:%d, height:%d"%(width, height))
            else:
                print("can not get size from param!")
                continue
                
            cmd = "mv " + yuvFile + " " + yuvDir + prefix + "_" + str(width) + "x" + str(height) + "_15.yuv"
            print(cmd)
            subprocess.call(cmd, shell=True)
            cmd = "rm -rf " + paramFile + " " + hevcFile
            print(cmd)
            subprocess.call(cmd, shell=True)

        

