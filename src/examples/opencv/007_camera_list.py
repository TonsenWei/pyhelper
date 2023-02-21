# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/1/12 10:45
@File : 007_camera_list.py
@Desc : pip install pycameralist
not ok, 这个苦作者不维护了，尝试导入也不行，pip安装不成功，网上找whl的安装后也import不成功
"""
import PyCameraList
from PyCameraList import *

print(PyCameraList.__version__)
# print(dict(cameras))
# return: {0: 'Intel(R) RealSense(TM) 3D Camera (Front F200) RGB', 1: 'NewTek NDI Video', 2: 'Intel(R) RealSense(TM) 3D Camera Virtual Driver', 3: 'Intel(R) RealSense(TM) 3D Camera (Front F200) Depth', 4: 'OBS-Camera', 5: 'OBS-Camera2', 6: 'OBS-Camera3', 7: 'OBS-Camera4', 8: 'OBS Virtual Camera'}

# audios = list_audio_devices()
# print(dict(audios))
# return:  {0: '麦克风阵列 (Creative VF0800)', 1: 'OBS-Audio', 2: '线路 (NewTek NDI Audio)'}
