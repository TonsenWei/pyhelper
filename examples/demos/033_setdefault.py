# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/1/5 9:36
@File : 033_setdefault.py
@Desc : 
"""
d = {"x": "xValue", "y": "yVal"}

print(d.setdefault("a"))  # None
print("b = " + str(d.setdefault("b", "")))  # 9
