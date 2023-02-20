# 一、倒序列表输出
test = [1,2,3,4,5]
# 解法一
print(test[::-1])
# 解法二
count = len(test)
new_list = []
while(count):
    count -= 1
    new_list.append(test[count])
print(new_list)
# 解法三
new_list_2 = []
for i in range(len(test)-1, -1, -1):
    new_list_2.append(test[i])
print(new_list_2)

# 二、计算 0 + 1 + 2 + 3 + ... + 100
# 解法一
counter = 100
total = 0
while(counter):
    total += counter
    counter -= 1
print(total)
# 解法2
total_sum = 0
for i in range(0, 101):
    total_sum += i
print(total_sum)

print("sum(range(101)) = " + str(sum(range(101))))

# 三、计算列表中各自数字的平方生成新列表
print("\n\n计算列表中各自数字的平方生成新列表")
list_num = [1, 2, 3, 4, 5]
print([i*i for i in list_num])
def sqr(x):
    return x**2
res = map(sqr, list_num)
print("list(res) = " + str(list(res)))

# 四、列表操作
print("\n\n列表操作")
a=[1,2,3,4,5]
print("原列表 = " + str(a))
# print("a(0) = " + str(a(0))) # TypeError: 'list' object is not callable,列表访问使用[]而不是括号()
print("a[-1] = " + str(a[-1])) ### 取最后一个元素
# [5]

print("a[:-1] = " + str(a[:-1])) ### 除了最后一个取全部,顾头不顾尾，-1是最后一个数
# [ 1 2 3 4 ]

print("a[::-1] = " + str(a[::-1])) ### 取从后向前（相反）的元素
# [ 5 4 3 2 1 ]

print("a[2::-1] = " + str(a[2::-1])) ### 取从下标为3的元素翻转读取
# [3 2 1 ]


