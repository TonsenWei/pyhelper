# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/12/9 15:54
@File : 026_List差集并集.py
@Desc : 
"""
import operator

listA = [1, 2, 3, 4]
listB = [2, 3, 4, 5]

print(list(set(listA).difference(set(listB))))  # [1]  差集，包含在集合A中，不包含在集合B中


listD1 = ['237b6307']
listD2 = ['237b6307']
print(operator.eq(listD1, listD2))  # True



