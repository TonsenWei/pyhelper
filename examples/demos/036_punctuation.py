# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/1/29 10:27
@File : 036_punctuation.py
@Desc : 字符串标点符号
"""
import re
import string

line = "!#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~,.，。hhhhh哈哈哈shi djaljgllb  slg555667&*……&*%……&￥……%￥&*……！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛“”„‟…‧﹏."

# c = line
# for j in line:
#     if j in string.punctuation:
#         c = c.replace(j, '')
# print(c)


def remove_punctuation(line):
  rule = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]")
  line = rule.sub('',line)
  return line

print(remove_punctuation(line))