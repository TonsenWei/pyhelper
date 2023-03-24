# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/3/21 14:27
@File : relay_demo.py
@Desc : 
"""
import os
from ctypes import *

# DLL_PATH = os.path.abspath(os.path.dirname(__file__))
# os.add_dll_directory(DLL_PATH)
dll = WinDLL("./usb_relay_device.dll")

res = dll.usb_relay_init()
print(f"init res = {res}")
res = dll.usb_relay_exit()
print(f"exit res = {res}")