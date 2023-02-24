"""
sub是substitute的所写，表示替换；
re.sub是个正则表达式方面的函数，用来实现通过正则表达式，实现比普通字符串的replace更加强大的替换功能；
"""
# a="张明 98分"，用re.sub，将98替换为100
import re

a = "张明 98分"
ret = re.sub(r"\d+", "100", a)  # “+” 匹配前面的子表达式一次或多次。要匹配 + 字符，请使用 \+。
print(ret)  # 张明 100分

inputStr = "hello 111 world 222"
ret1 = re.sub(r"\d+", "", inputStr)
print(ret1)  #  hello  world    :会有两个空格
