'''
计算输入的多个字符串最后一个字符串的长度，多个字符串空格隔开
如： abc gaggag gagsg
'''
a = input()
b = a.split()[-1]
c = len(b)
print(c)

# 一行代码
print(len(input().split()[-1]))