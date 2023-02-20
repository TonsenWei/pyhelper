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
my_camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))  # 该格式才支持高帧率

"设置视频格式"
write_ok = False
frame_size = (int(my_camera.get(cv2.CAP_PROP_FRAME_WIDTH)), int(my_camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
frame_fps = 30
video_format = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

"设置录制的视频文件名"
video_file_fp = cv2.VideoWriter()
video_file_fp.open('camera_video.mp4', video_format, frame_fps, frame_size, True)

start_time = time.time()
video_time_length = 10
print('Start to record video')

"循环录制视频文件，并给视频加上时间戳"
startFpsTime = time.time()
fpsCounter = 0
fps = 0
while (True):
    sucess, video_frame = my_camera.read()
    fpsCounter += 1
    if time.time() - startFpsTime >= 1:
        print(f"fps={fpsCounter}")
        fps = fpsCounter
        fpsCounter = 0
        startFpsTime = time.time()
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # cv2.putText(video_frame, time_str, (5, 340), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    # 显示时间和帧率
    cv2.putText(video_frame, f"{time_str} fps:{fps}", (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    video_file_fp.write(video_frame)
    cv2.imshow('frame', video_frame)

    cur_time = time.time()  # 录制10秒后自动结束或者按ESC键退出
    if cur_time - start_time >= video_time_length:
        print('End the video with ' + str(video_time_length) + ' s')
        break
    if cv2.waitKey(1) & 0xff == 27:  # esc key
        break

"关闭录制"
video_file_fp.release()
my_camera.release()
cv2.destroyAllWindows()

"显示录制的视频文件大小"
mp4_file_size = os.path.getsize('camera_video.mp4')
print(int(mp4_file_size / 1024), 'KBytes')
