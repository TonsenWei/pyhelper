# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/2/3 15:32
@File : 037_replace_string.py
@Desc : 
"""
content = "test0123456"
newContent = content.replace("test", "xyz")
print(content)
print(newContent)

textStr = ["1", "2", "3"]
print(textStr)
textStr[1] = "19"
print(textStr)

dic = {"root":
    [
        {"item1": "test1"},
        {"item2": "test2"},
    ]}
print(dic)
dic["root"][0]["item1"] = "ttttt"
print(dic)