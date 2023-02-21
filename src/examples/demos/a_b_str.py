
print("Plz input to str split with space:")
# str_in = input()
str_in = "inpaut a  to a split with space"
print(str_in)
strs = str_in.split()
print(strs)
a = strs[0]
b = strs[1]
print(a.index(b))  # b在a中的索引
print(a.find(b))  # b在a中的索引