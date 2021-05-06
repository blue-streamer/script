import sys
import os
os.system("grep -R "+sys.argv[1]+" api audio base call common_audio common_video logging media modules p2p pc rtc_base video sdk")
print "finish almost dir"
os.system("grep -R "+sys.argv[1]+" third_party")
