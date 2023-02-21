#  递归求和
def get_sum(num):
    if num>=1:
        res = num + get_sum(num-1)
    else:
        res = 0
    return res

if __name__ == "__main__":
    print(get_sum(10))