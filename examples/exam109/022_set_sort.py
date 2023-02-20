s = "ajldjlajfdljfddd"
s1 = set(s)
print("set = " + str(s1))
s2 = list(s1)
# sort()与sorted()的不同在于，sort是在原位重新排列列表，而sorted()是产生一个新的列表
# sort()不会返回任何值，而sorted返回一个列表
s2.sort()  
print("".join(s2))