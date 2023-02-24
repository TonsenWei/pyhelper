# 13、列表[1,2,3,4,5],请使用map()函数输出[1,4,9,16,25]，
# 并使用列表推导式（[表达式 for 变量 in 列表]    或者  [表达式 for 变量 in 列表 if 条件]）提取出大于10的数，最终输出[16,25]


def squar(x):
    return x**2

# 第一个参数接受一个函数名，后面的参数接受一个或多个可迭代的序列，返回的是一个集合。
# 把函数依次作用在list中的每一个元素上，得到一个新的list并返回。注意，map不改变原list，而是返回一个新list。
res = map(squar, [1,2,3,4,5])
res = [i for i in res if i > 10]
print(res)  # [16, 25]

print([i*i for i in range(0, 6)])  
# 输出 [0, 1, 4, 9, 16, 25]
print([i*i for i in range(0, 6) if i*i > 10])  
# 输出 [16, 25]


# 通过使用lambda匿名函数的方法使用map()函数：
res1 = map(lambda x, y: x+y,[1,3,5,7,9],[2,4,6,8,10])
print([i for i in res1])
print(", ".join(res1))
# 结果如下：[3,7,11,15,19]