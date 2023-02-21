import sys
import os


file_dir = os.path.dirname(os.path.abspath(__file__))
# print(os.path.abspath(os.path.join(file_dir, "../test1/")))
# sys.path.append(file_dir + "/test1/")
sys.path.append(os.path.abspath(os.path.join(file_dir, "../test1/")))

import test1_1 as output001


def output002():
    print("call ouput001 from output002")

if __name__ == "__main__":
    output001.output001()
