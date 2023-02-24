"""
{sort()与sorted()的不同在于，sort是在原位重新排列列表，而sorted()是产生一个新的列表。
sorted(L)返回一个排序后的L，不改变原始的L；
L.sort()是对原始的L进行操作，调用后原始的L会改变，没有返回值。
【所以a = a.sort()是错的啦,a = sorted(a)才对.
sorted()适用于任何可迭代容器，list.sort()仅支持list（本身就是list的一个方法）
基于以上两点，sorted使用频率比list.sort()更高些，所以Python中更高级的排序技巧便通过sorted()来演示。}
"""

