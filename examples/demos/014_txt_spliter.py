"""
Author: Wei Dongcheng
Date: 2022/8/10 18:50
LastEditTime: 2022/8/10 18:50
LastEditors: Wei Dongcheng
File: 014_txt_spliter.py
Description:
"""
from src.myutils.file_util import FileUtil


file_size = FileUtil.get_file_size(r'D:\software\YY\20220810_01语义测试\20220628008\logcat.txt')
file_size_kb = FileUtil.get_file_size(r'D:\software\YY\20220810_01语义测试\20220628008\logcat.txt', "k")
file_size_mb = FileUtil.get_file_size(r'D:\software\YY\20220810_01语义测试\20220628008\logcat.txt', "m")
file_size_gb = FileUtil.get_file_size(r'D:\software\YY\20220810_01语义测试\20220628008\logcat.txt', "g")
file_size_tb = FileUtil.get_file_size(r'D:\software\YY\20220810_01语义测试\20220628008\logcat.txt', "t")
print(file_size)
print(file_size_kb)
print(file_size_mb)
print(file_size_gb)
print(file_size_tb)
