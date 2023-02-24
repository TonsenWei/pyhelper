# -*- coding: utf-8 -*-
input_str = input()
if input_str is not None and len(input_str) < 5000:
    print(str(len(input_str.split()[-1])))