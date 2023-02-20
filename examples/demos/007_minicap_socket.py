import glob
import os
import socket
import sys
import time
import struct
from collections import OrderedDict
from datetime import datetime

# import cv2

IMAGE_FORMAT = ".png"

project_path = os.path.dirname(os.path.abspath(__file__))


class Banner:
    def __init__(self):
        self.__banner = OrderedDict(
            [('version', 0),
             ('length', 0),
             ('pid', 0),
             ('realWidth', 0),
             ('realHeight', 0),
             ('virtualWidth', 0),
             ('virtualHeight', 0),
             ('orientation', 0),
             ('quirks', 0)
             ])

    def __setitem__(self, key, value):
        self.__banner[key] = value

    def __getitem__(self, key):
        return self.__banner[key]

    def keys(self):
        return self.__banner.keys()

    def __str__(self):
        return str(self.__banner)


class Minicap:
    def __init__(self, host, port, banner):
        self.buffer_size = 4096
        self.host = host
        self.port = port
        self.banner = banner

    def connect(self):
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except (socket.error) as e:
            print(e)
            sys.exit(1)
        self.__socket.connect((self.host, self.port))

    def on_image_transfered(self, data):
        file_name = str(time.time()) + IMAGE_FORMAT
        file_path = project_path + "\\pics\\" + file_name
        # print(file_path)
        with open(file_path, 'wb') as f:
            for b in data:
                f.write(b.to_bytes(1, 'big'))

    def consume(self):
        readBannerBytes = 0
        bannerLength = 24
        readFrameBytes = 0
        frameBodyLength = 0
        frame_counter = 0
        data = []
        start_time = time.time()
        while True:
            try:
                chunk = self.__socket.recv(self.buffer_size)
            except (socket.error) as e:
                print(e)
                sys.exit(1)
            cursor = 0
            buf_len = len(chunk)
            while cursor < buf_len:
                if readBannerBytes < bannerLength:  # 24
                    map(lambda i, val: self.banner.__setitem__(self.banner.keys()[i], val),
                        [i for i in range(len(self.banner.keys()))], struct.unpack("<2b5ibB", chunk))
                    cursor = buf_len
                    readBannerBytes = bannerLength
                    print(self.banner)
                elif readFrameBytes < 4:
                    # print(struct.unpack('B', (chunk[cursor]).to_bytes(1, 'big')))
                    # frameBodyLength += (struct.unpack('B', chunk[cursor])[0] << (readFrameBytes * 8)) >> 0
                    frameBodyLength += (chunk[cursor] << (readFrameBytes * 8)) >> 0
                    cursor += 1
                    readFrameBytes += 1
                else:
                    # print("frame length:{0} buf_len:{1} cursor:{2}".format(frameBodyLength, buf_len, cursor))
                    # pic end
                    if buf_len - cursor >= frameBodyLength:
                        data.extend(chunk[cursor:cursor + frameBodyLength])
                        self.on_image_transfered(data)
                        cursor += frameBodyLength
                        frameBodyLength = readFrameBytes = 0
                        data = []
                        frame_counter += 1
                        # if frame_counter >= 60:
                        #     end_time = time.time() - start_time
                        #     print("cost time in 60 frame = " + str(end_time))
                        #     start_time = time.time()
                        #     frame_counter = 0
                    else:
                        data.extend(chunk[cursor:buf_len])
                        frameBodyLength -= buf_len - cursor
                        readFrameBytes += buf_len - cursor
                        cursor = buf_len

                frame_time = time.time() - start_time
                if frame_time >= 1:
                    print("frame rate = " + str(frame_counter))
                    frame_counter = 0
                    start_time = time.time()


if __name__ == '__main__':
    """minicap 使用socket截图
    调试步骤：
    1、获取版本信息
        cpu版本:adb shell getprop ro.product.cpu.abi   # DI5.0:arm64-v8a
        sdk版本：adb shell getprop ro.build.version.sdk  # DI5.0: 31
    2、在airtest上找到相应的minicap可执行文件和minicap.so文件。
        minicap在（AirtestIDE_2020-01-21_py3_win64\airtest\core\android\static\stf_libs\arm64-v8a）目录下，
        而minicap.so在（airtest\core\android\static\stf_libs\minicap-shared\aosp\libs\android-27\arm64-v8a）目录下。
        或者python库下的
        \Lib\site-packages\airtest\core\android\static\stf_libs\arm64-v8a\minicap
        \Lib\site-packages\airtest\core\android\static\stf_libs\minicap-shared\aosp\libs\android-31\arm64-v8a\minicap.so
    3、手机安装minicap的so库
        adb shell chmod 777 /data/local/tmp/minicap
        adb shell chmod 777 /data/local/tmp/minicap.so
    4、手机开启minicap服务：
       手机：adb shell LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P 1080x1920@1080x1920/0
       手机：adb shell LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P 1080x2340@1080x2340/0
       平板：adb shell LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P 1920x1080@1920x1080/0
    5、本机端口映射：
        adb forward tcp:1313 localabstract:minicap
    6、执行如下代码，即可在当前目录下生成手机截屏
    参考链接：https://blog.csdn.net/miaokaibo/article/details/103116411
    java版本：https://blog.csdn.net/itfootball/article/details/47658171
    """
    """
    1、调试在minicap实时截图时，uiautomator2是否可以同时操作: 实测可以（2022-07-08）
    2、uiautomator2截图帧率很低。
    """
    print("start ...")
    mc = Minicap('localhost', 1313, Banner())
    mc.connect()
    mc.consume()
    print("end ...")

""" 图像帧转换成视频"""


# import cv2
# import glob
# import os
# from datetime import datetime

def get_files_path_list(dir_path, suffix):
    """
    获取某个目录下所有后缀为 suffix 的文件的路径
    FileUtil.get_files_path_list(r"D:\Projects\gitee\pylearning\files\wav_report", ".wav")
    :param dir_path: 查找文件所在目录
    :param suffix: 后缀名，如 .wav
    :return: 路径列表
    """
    info_list = []
    for i, j, k in os.walk(dir_path):
        for file in k:
            if file.endswith(suffix):
                info_list.append(os.path.join(i, file))
    return info_list

#
# def frames_to_video(fps, save_path, frames_path, max_index):
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     videoWriter = cv2.VideoWriter(save_path, fourcc, fps, (960, 544))
#     imgs = glob.glob(frames_path + "\\*.png")
#     frames_num = len(imgs)
#     print("frames_num = " + str(frames_num))
#     pngs = get_files_path_list(frames_path, ".png")
#     counter = 0
#     for png_index in range(max_index):
#         counter += 1
#         if os.path.isfile(pngs[png_index]):
#             print(pngs[png_index])
#             frame = cv2.imread(pngs[png_index])
#             frame = cv2.resize(frame, (960, 544))  # 没有这行时，会提示视频损坏
#             videoWriter.write(frame)
#     videoWriter.release()
#     return
#
#
# if __name__ == '__main__':
#     """
#     Premature end of JPEG file
#     """
#     t1 = datetime.now()
#     # frames_to_video(22, "result.mp4", 'face_recog_frames', 1000)
#     frames_to_video(22, "result.mp4", project_path + "\\pics", 100)
#     t2 = datetime.now()
#     print("Time cost = ", (t2 - t1))
#     print("SUCCEED !!!")
