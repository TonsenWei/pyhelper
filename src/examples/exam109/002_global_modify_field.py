# 在一个函数内部修改全局变量
a = 1  # 全局变量
def modify_field():
    global a  # 表明使用全局变量
    a = 2
    print(a)
    return

print("before modify:" + str(a))  # before modify:1
modify_field()
print("after modify:" + str(a))  # after modify:2