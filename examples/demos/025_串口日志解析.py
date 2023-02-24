# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/12/8 19:15
@File : 025_串口日志解析.py
@Desc : 
"""

def readLog():
    logPath = r"D:\projects\python\pylearning\files\A02开机日志OK.txt"
    with open(logPath, encoding="utf-8", mode="r+") as logFile:
        line = logFile.readline()
        while line:
            print(line.lstrip("b'").strip("\r\n").rstrip("'"))
            line = logFile.readline()


if __name__ == "__main__":
    readLog()
