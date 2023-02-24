# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/12/16 15:39
@File : 002_camera2mp4.py
@Desc : 验证ok
"""
import cv2
import os
import time

"打开摄像头，设置分辨率"
my_camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)
my_camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
my_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
time.sleep(5)

start_time = time.time()
video_time_length = 10  # 单位秒
print('Start to record video')
"循环录制视频文件，并给视频加上时间戳"
startFpsTime = time.time()
fpsCounter = 0
fps = 0
if my_camera.isOpened() is False:
    print("摄像头未打开！")
    os.system.exit(-1)
print("camera started")
while True:
    sucess, video_frame = my_camera.read()
    fpsCounter += 1
    if time.time() - startFpsTime >= 1:
        print(f"fps={fpsCounter}")
        fps = fpsCounter
        fpsCounter = 0
        startFpsTime = time.time()
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 显示时间和帧率
    cv2.putText(video_frame, f"{time_str} fps:{fps}", (1, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow('frame', video_frame)

    cur_time = time.time()  # 录制10秒后自动结束或者按ESC键退出
    if cur_time - start_time >= video_time_length:
        print('End the video with ' + str(video_time_length) + ' s')
        break
    if cv2.waitKey(1) & 0xff == 27:  # esc key
        break

"关闭录制"
my_camera.release()
cv2.destroyAllWindows()

"显示录制的视频文件大小"
# mp4_file_size = os.path.getsize('camera_video.mp4')
# print(int(mp4_file_size / 1024), 'KBytes')
