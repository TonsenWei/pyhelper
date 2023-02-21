# 浮点字符串直接强转为int会报错
# print(int("1.4"))  # ValueError: invalid literal for int() with base 10: '1.4'
print(int(float("1.4")))  # 先转为float再转int即可
print(int(1.4))

print(str("abc".split()))  # ['abc']
print(list("abcd"))
