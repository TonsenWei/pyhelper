# a="hello"和b="你好"编码成bytes类型
a = b"hello"  # 直接指定这个hello是bytes类型

b="你好".encode()
print(a,b)  # b'hello' b'\xe4\xbd\xa0\xe5\xa5\xbd'

# （对于bytes，我们只要知道在Python3中某些场合下强制使用，以及它和字符串类型之间的互相转换，其它的基本照抄字符串。
# 简单的省事模式：
string = b'xxxxxx'.decode()  # 直接以默认的utf-8编码解码bytes成string
b = string.encode()  # 直接以默认的utf-8编码string为bytes