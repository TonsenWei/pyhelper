# 1）利用推导式运行过程：for i in a ,每个i是【1,2】，【3,4】，【5,6】，for j in i，每个j就是1,2,3,4,5,6,合并后就是结果
 
a=[[1,2],[3,4],[5,6]]
x=[j for i in a for j in i]  # 这个的解析过程是 从a中取出每一个值付给i，然后从i中取出每一个 值复制给j 然后输出j的结果
print(x)    # ==>[1, 2, 3, 4, 5, 6]

# 2）将列表转成numpy矩阵，通过numpy的flatten（）方法
import numpy as np
b=np.array(a).flatten().tolist()
print(b)
# 3）# j for i in a for j in i等于：
list=[]
for i in a:
    for j in i:
        list.append(j)
print(list)