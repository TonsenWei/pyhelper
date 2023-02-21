# python脚本传递参数

import sys

print(sys.argv[0])          #sys.argv[0] 类似于shell中的$0,但不是脚本名称，而是脚本的路径   
print(sys.argv[1])          #sys.argv[1] 表示传入的第一个参数，既 hello

# (py3env) PS D:\Projects\VSCodeProject\Python\pylearning\examples\demos> python 003_sys_argv.py test
# 输出：
# 003_sys_argv.py
# test