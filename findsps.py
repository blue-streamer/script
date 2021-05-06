import numpy as np
import os
import sys
import struct

fileName = sys.argv[1]

bitstream = []
fileSize = os.path.getsize(fileName)

with open(fileName,'rb') as file:
        for i in range(fileSize):
            buffer = file.read(1)
            bitstream.append(buffer)

print(len(bitstream))
bitLen = len(bitstream)
startPos = []
for x in range(bitLen-5):
  if bitstream[x] == b'\x00' and bitstream[x+1] == b'\x00' and bitstream[x+2] == b'\x00' and bitstream[x+3] == b'\x01' and bitstream[x+4] == b'g' and bitstream[x+5] == b'B':
    startPos.append(x)

print(startPos)

for x in range(len(startPos)-1):
  bitstream_filename = str(x) + ".264"
  file = open(bitstream_filename, "wb")
  for i in range(startPos[x], startPos[x+1]):
    file.write(bitstream[i])
  file.close()
  
  

