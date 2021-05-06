import cv2
import numpy as np
import os
import sys
import struct

dump_dir = "/Users/bytedance/yuv_dump"
portrait = False


file_list = os.listdir(dump_dir)
file_list = [file_name for file_name in file_list if file_name.split('.')[1]=="yuv"]
file_list.sort(key=lambda x:int(x.split('_')[0]))
for x in file_list :
    print(x)

if (len(file_list)<=0):
    exit()

start_idx = sys.argv[1]
print(int(start_idx))
idx = int(start_idx)
width = 180
height = 320

# prev_w,prev_h=0,0
# for idx in range(len(file_list)):
while(True):
    file_name = file_list[idx]
    file_path = os.path.join(dump_dir,file_name)
    file_size = os.path.getsize(file_path)
    if not portrait:
        if (file_size == 1280*720*1.5):
            width,height = 1280,720
        elif (file_size == 640*360*1.5):
            width,height = 640,360
        elif (file_size == 320*180*1.5):
            width,height = 320,180
        else:
            print("no resolution matched, file_size: ",file_size)
            continue
    else:
        if (file_size == 1080*768*1.5):
            width,height = 768,1080
        elif (file_size == 640*384*1.5):
            width,height = 384,640
        elif (file_size == 320*192*1.5):
            width,height = 192,320
        elif (file_size == 320 * 256 * 1.5):
            width, height = 256, 320
        else:
            print("no resolution matched, file_size: ",file_size)
            continue

    # frame_num = int(file_name.split('_')[0])
    # if (prev_w != width):
    #     print(frame_num)
    # prev_w,prev_h = width,height

    uv_stride = width//2
    uv_height = height//2

    raw_datas = []
    with open(file_path,'rb') as file:
        for i in range(int(width*height*1.5)):
            buffer = file.read(1)
            data = struct.unpack('B',buffer)[0]
            data = min(max(0.0,data),255.0)
            raw_datas.append(data)

    print(len(raw_datas))

    y_data = raw_datas[:width*height]
    u_data = raw_datas[width*height:width*height+uv_stride*uv_height]
    v_data = raw_datas[width*height+uv_stride*uv_height:]

    y_mat = np.array(y_data).reshape([height,width]).astype(np.uint8)
    u_mat = np.array(u_data).reshape([uv_height,uv_stride]).astype(np.uint8)
    v_mat = np.array(v_data).reshape([uv_height,uv_stride]).astype(np.uint8)

    yuv_mat = np.array(raw_datas).reshape([height*3//2,width]).astype(np.uint8)
    rgb = cv2.cvtColor(yuv_mat,cv2.COLOR_YUV2BGR_I420)

    cv2.imshow("_y_data",y_mat)
    cv2.imshow("_u_data",u_mat)
    cv2.imshow("_v_data",v_mat)
    cv2.imshow("yuv_data",rgb)

    print(file_name)


    key = cv2.waitKey(0)
    # cv2.destroyAllWindows()
    if (key==ord(',')):
        idx = max(0,idx-1)
        continue
    elif (key == ord('.')):
        idx = min(idx+1,len(file_list)-1)
        continue
    elif (key==ord('q')):
        exit()
