#coding=UTF-8
import re
import sys
import matplotlib.pyplot as plt
import numpy as np

'''
记录一段时间的top输出，命名为top_record.txt
输入参数 pid1 process_name1 pid2 process_name2 ...
example: python prase_top 27041 Feishu\\sHelper 35603 zoom.us ......
功能 把传入的所有process 消耗的cpu相加，计算均值，画图
'''

param_len = len(sys.argv)
if param_len <= 2:
  print "error param, please input targe pid and process name"
  sys.exit()
match_str_list=[]
for index in range(param_len/2) :
  itr = index*2+1
  print "target pid:"+str(sys.argv[itr])
  print "target process:"+str(sys.argv[itr+1])
  match_str = str(sys.argv[itr])+"\s*"+str(sys.argv[itr+1])+"\s*(\d*\.*\d*)"
  match_str_list.append(match_str)
  print "target match str:"+match_str

testFile=open("top_record.txt")
cpuStr = testFile.read()

list_of_result_list = []
min_length = 0xffffffff
for match_str in match_str_list:
  obj = re.compile(match_str, re.M)
  result = obj.findall(cpuStr)
  print "the list length of result:", len(result)
  print result
  min_length = min(min_length, len(result))
  list_of_result_list.append(result)

print "min length of list:", min_length

final_result = []
index_list = []
for index in range(min_length):
  cur = 0
  index_list.append(index)
  for cur_list in list_of_result_list:
    cur += float(cur_list[index])
  final_result.append(cur)

print final_result

mean_value = np.mean(final_result)
mean_list = []
print "average cpu usage:" + str(mean_value)
for item in final_result :
  mean_list.append(mean_value)

plt.plot(index_list, final_result, "blue")
plt.plot(index_list, mean_list, "red")
plt.show()


