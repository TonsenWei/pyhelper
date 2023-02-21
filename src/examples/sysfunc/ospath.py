# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/11/9 9:08
@File : ospath.py
@Desc : 
"""
import os

path = os.path.relpath(r"D:\projects\python\ocr\PaddleOCR-json-main", r"D:\projectts\pythontt")
print(path)  # ..\python\ocr\PaddleOCR-json-main
abs_path = os.path.abspath(r"D:/projects/python/ocr/PaddleOCR-json-main")  # D:\projects\python\ocr\PaddleOCR-json-main
print(abs_path)