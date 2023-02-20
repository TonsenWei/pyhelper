# python2和python3区别？列举5个
# 1、Python3 使用 print 必须要以小括号包裹打印内容，比如 print('hi')
# Python2 既可以使用带小括号的方式，也可以使用一个空格来分隔打印内容，比如 print 'hi'

# 2、python2 range(1,10)返回列表，python3中返回迭代器，节约内存

# 3、python2中使用ascii编码，python3中使用utf-8编码

# 4、python2中unicode表示字符串序列，str表示字节序列
# python3中str表示字符串序列，byte表示字节序列

# 5、python2中为正常显示中文，引入coding声明，python3中不需要

# 6、python2中是raw_input()函数，python3中是input()函数
# 7、
# True和False
# True 和 False 在 Python2 中是两个全局变量（名字），在数值上分别对应 1 和 0，既然是变量，那么他们就可以指向其它对象，例如：

# # py2
# >>> True = False
# >>> True
# False
# >>> True is False
# True
# >>> False = "x"
# >>> False
# 'x'
# >>> if False:
# ...     print("?")
# ... 
# ?
# 显然，上面的代码违背了 Python 的设计哲学 Explicit is better than implicit.。而 Python3 修正了这个缺陷，True 和 False 变为两个关键字，永远指向两个固定的对象，不允许再被重新赋值。

# py3
# >>> True = 1
#   File "<stdin>", line 1
# SyntaxError: can't assign to keyword

# 8、我们都知道在Python2中可以在函数里面可以用关键字 global 声明某个变量为全局变量，
# 但是在嵌套函数中，想要给一个变量声明为非局部变量是没法实现的，
# 在Pyhon3，新增了关键字 nonlcoal，使得非局部变量成为可能。

def func():
    c = 1
    def foo():
        c = 12
    foo()
    print(c)
func()    #1
# 可以对比上面两段代码的输出结果

def func():
    c = 1
    def foo():
        nonlocal c
        c = 12
    foo()
    print(c)
func()   # 12
