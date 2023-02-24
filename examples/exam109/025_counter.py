# 利用collections库的Counter方法统计字符串每个单词出现的次数

from collections import Counter

a = "kjalfj;ldsjafl;hdsllfdhg;lahfbl;hl;ahlf;h"

res = Counter(a)
# 返回的是counter对象
print(res)  # Counter({'l': 9, ';': 6, 'h': 6, 'f': 5, 'a': 4, 'j': 3, 'd': 3, 's': 2, 'k': 1, 'g': 1, 'b': 1})
# 列出所有元素
# ['k', 'j', 'j', 'j', 'a', 'a', 'a', 'a', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'f', 'f', 'f', 'f', 'f', ';', ';', ';', ';', ';', ';', 'd', 'd', 'd', 's', 's', 'h', 'h', 'h', 'h', 'h', 'h', 'g', 'b']
print(list(res.elements()))
# 取l的计数结果
print(res["l"])  # 9
# 计数最多的两个
print(res.most_common(2))  # [('l', 9), (';', 6)]

# 统计字符或字符串出现的次数
print(a.count("l"))
str="张三 哈哈 张三 呵呵 张三"
res=str.count("张三")
print(res)  # ==》3
