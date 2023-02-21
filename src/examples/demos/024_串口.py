# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/12/6 11:16
@File : 024_串口.py
@Desc : 
"""
import time

import serial


def write_ANSI_ASCII_test():
    """
    往串口写ANSI颜色字符和ASCII特殊字符测试
    :return:
    """
    com_serial = serial.Serial(port="COM2", baudrate=115200, bytesize=8, parity="N", stopbits=1)
    line0 = '# \r\r\n'
    line1 = '# \x00S - Secure Boot: Off\r\n'
    line = "    \x1b[1;30m[ \x1b[1;32mAna_Info\x1b[0m [Analyzer] starting on -ae tool_policy_manager \x1b[1;30m]\x1b[0m\r\n"
    line3 = "\x11[qcpe_qhee_vm_config.c:278]: [tid=1] qcpe_allow_map_phys_tz_bridges: Allow range IPA_GSI, pa_start=0x98710000, pa_end= 0x98716fff\r\n"
    com_serial.write(line0.encode(encoding="utf-8"))
    com_serial.write(line1.encode(encoding="utf-8"))
    com_serial.write(line.encode(encoding="utf-8"))
    com_serial.write(line3.encode(encoding="utf-8"))
    com_serial.close()

def writeFromFileTest():
    logPath = r"E:\Tonsen\Downloads\logs\zhanghuanxin\2023-02-08_09-17-33_555_COM27.txt"
    com_serial = serial.Serial(port="COM2", baudrate=921600, bytesize=8, parity="N", stopbits=1)
    # start_time = time.time()
    show_time = time.time()
    counter = 0
    while True:
        with open(logPath, encoding="utf-8", mode="r+") as logFile:
            line = logFile.readline()
            while line:
                # print(line.lstrip("b'").strip("\r\n").rstrip("'"))
                com_serial.write(f"{line}".encode(encoding="utf-8"))
                time.sleep(0.01)
                line = logFile.readline()
                if time.time() - show_time >= 5:
                    show_time = time.time()
                    counter += 1
                    print(f"running: {5*counter} s")


if __name__ == "__main__":
    # write_ANSI_ASCII_test()
    print("start ...")
    writeFromFileTest()
    print("end ...")
