import datetime

todaytime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + " 星期：" + str(datetime.datetime.now().isoweekday())
print(todaytime)  # 2021-12-17_14-43-24 星期：5