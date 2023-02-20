import test
import test.test1
import test.testtwo as testtwo
import test.test2.test2_2 as output002

if __name__ == "__main__":
    print("this is main.py")
    testtwo.testtwofun()
    output002.output002()
    # test2_2中导入了test1_1并as为output001，所以引用output1方式如下：
    output002.output001.output001()