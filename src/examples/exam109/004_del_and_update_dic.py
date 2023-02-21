# 字典如何删除键和合并两个字典
dic = {'name':'alex', 'age':18, 'sex':'female'}
del dic['sex']
print(dic)

dic1={'sex':'female'}
dic.update(dic1)
print(dic)

dic.pop("name")
print(dic)