"""
mode:文件打开模式
r:只读模式，文件不存在泽报错，默认模式(文件指针位于文件末尾)
r+:只读模式，文件不存在泽报错(文件指针位于文件开头)
w:写入模式，文件不存在则自动报错，每次打开会覆盖原文件内容,文件不关闭则可以进行多次写入（只会在打开文件时清空文件内容）
w+:写入模式，文件不存在则自动报错，每次打开会覆盖原文件内容，文件不关闭则可以进行多次写入（只会在打开文件时清空文件内容，指针位置在文件内容末尾）
a:追加模式，文件不存在则会自动创建，从末尾追加，不可读。
a+:追加且可读模式，刚打开时文件指针就在文件末尾。
"""
import os
import sys

this_file_path = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    '''
    打开文件在进行读写的时候可能会出现一些异常状况，如果按照常规的f.open写法，
    我们需要try,except,finally，做异常判断，并且文件最终不管遇到什么情况，
    都要执行finally f.close()关闭文件，with方法帮我们实现了finally中f.close
    '''
    print("this_file_path = " + this_file_path)
    test_from_file_path = this_file_path + "\\012_test_from.txt"
    os.remove(test_from_file_path)
    with open(test_from_file_path, "w+", encoding='gbk') as from_file:
        from_file.write("test\ntest1\ntest2\ntest3\ntest4\ntest5")

    test_to_file_path = this_file_path + "\\012_test_to.txt"
    with open(test_from_file_path, 'r', encoding='gbk') as from_file, open(test_to_file_path, 'w+', encoding='gbk') as to_file:
        line = from_file.readline()
        while line:
            to_file.write(line)
            print("line = " + line.replace('\r', '').replace('\n', ''))
            line = from_file.readline()
