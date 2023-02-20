# 写一段自定义异常
def fn():
    try:
        for i in range(5):
            if i>2:
                raise Exception("数字大于2了")
    except Exception as ret:
        print(ret)  # 输出：数字大于2了

if __name__ == "__main__":
    fn()