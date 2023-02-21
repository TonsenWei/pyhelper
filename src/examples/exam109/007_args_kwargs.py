'''
*args和**kwargs主要用于函数定义。你可以将不定数量的参数传递给一个函数。
这里的不定的意思是:预先并不知道,函数使用者会传递多少个参数给你所以在这个场景下使用这两个关键字。

*args是用来发送一个非键值对的可变数量的参数列表给一个函数
        用来将参数打包成tuple(元组)给函数体调用

**kwargs允许你将不定长度的键值对，作为参数传递给一个函数。
        打包关键字参数成dict(字典)给函数体调用
'''

def function(x, y, *args):
    print(x, y, args)  # 1 2 (3, 4, 5)
    print("args[0] = " + str(args[0]))  # args[0] = 3

function(1, 2, 3, 4, 5)

def function(**kwargs):
    print( kwargs, type(kwargs))

function(a=2)  # {'a': 2} <class 'dict'>

def function(**kwargs):
    print(kwargs)

function(a=1, b=2, c=3)  # {'a': 1, 'b': 2, 'c': 3}