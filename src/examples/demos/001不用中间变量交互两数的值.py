a = 1
b = 2

print("before:a=" + str(a) + ", b=" + str(b))
a,b = b,a
print("after:a=" + str(a) + ", b=" + str(b))
