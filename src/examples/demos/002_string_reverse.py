str_tobe_rev = "123456789"
print("------字符串：" + str_tobe_rev)
print("\r\n------使用切片反转字符串：")
print(str_tobe_rev[::-1])
print("\r\n------使用Reversed反转字符串：")
print("\r\n------使用 reversed() 函数进行逆序操作，并不会修改原来序列中元素的顺序")
print(''.join(reversed(str_tobe_rev)))
print("\r\n------使用for循环反转字符串：")
for i in range(len(str_tobe_rev)):
    print(str_tobe_rev[len(str_tobe_rev) - 1 - i], end='')