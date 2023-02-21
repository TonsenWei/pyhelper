import sys
import os

# import test1.test1_1

file_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(file_dir + "/test1/")
import test1_1  # 这个导入，需要在sys.path.append之后，否则在外层文件夹执行出错


def testtwofun():
    print("testtwofun()")
