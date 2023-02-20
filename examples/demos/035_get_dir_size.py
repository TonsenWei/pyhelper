# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/1/17 15:45
@File : 035_get_dir_size.py
@Desc : 
"""
import os
import time
from os.path import join

print(os.path.getsize(r'E:\tmp'))  # 0, 不能获取文件夹

# path = r"E:\tmp"
path = r"E:\Tonsen"
size = 0  # Bytes
start_time = time.time()
for root, dirs, files in os.walk(path):
    for filename in files:
        # 获取文件大小用 os.path.getsize
        size += os.path.getsize(os.path.join(root, filename))
print(f"cost time = {time.time() - start_time}")  # 115.44G -> 6.18秒
print("{:.2f}M".format(size / (1024**2)))
print("{:.2f}G".format(size / (1024**3)))


def getDirSize(dir_path, unit="G"):
    """
    获取目录占用空间大小
    :param dir_path: 目录路径
    :param unit: 单位
    :return: 目录大小
    """
    dirSize = 0
    for root, dirs, files in os.walk(dir_path):
        for filename in files:
            # 获取文件大小用 os.path.getsize
            dirSize += os.path.getsize(os.path.join(root, filename))
    unit_lower = unit.lower()
    if unit_lower == "byte" or unit_lower == "b":
        return dirSize
    elif unit_lower == "k" or unit_lower == "kb":
        return round(dirSize / 1024, 3)
    elif unit_lower == "m" or unit_lower == "mb":
        return round(dirSize / (1024 ** 2), 3)
    elif unit_lower == "g" or unit_lower == "gb":
        return round(dirSize / (1024 ** 3), 3)
    elif unit_lower == "t" or unit_lower == "tb":
        return round(dirSize / (1024 ** 4), 3)
