"""
Author: Wei Dongcheng
Date: 2022/8/5 10:26
LastEditTime: 2022/8/5 10:26
LastEditors: Wei Dongcheng
File: 012_join.py.py
Description:
"""
args = ["adb", "shell", "ls", "-lh"]
print("args=" + str(" ".join(args)))
