import random
import numpy as np

# 包含两头的数
print("随机整数：", random.randint(10, 20))

# n个随机小数，可有正负
res = np.random.randn(5)
print("n个随机小数", res)

# 输出0-10间的随机偶数
res0_1 = random.randrange(0, 10, 2)
print("randrange:", res0_1)

# 0-1随机小数
print("随机小数：", random.random())