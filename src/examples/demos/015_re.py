# -*- coding: utf-8 -*-
"""
Author: Wei Dongcheng
Date: 2022/8/22 13:46
LastEditTime: 2022/8/22 13:46
LastEditors: Wei Dongcheng
File: 015_re.py
Description:
"""
import re


def find_cases(file_path):
    with open(file_path, 'r', encoding='utf-8') as from_file:
        line = from_file.readline()
        script_file_str = ""
        case_counter = 0
        while line:
            line_str = line.replace("\r", "").replace("\n", "").replace("\t", "").strip()
            data = re.match(".*tests/.*.py::.*test_.*setup.*", line_str)
            if data:
                case_counter += 1
                found = re.findall("tests/test_.*.py", line_str)
                if found:
                    # print(found[0].split("::")[0])
                    script_file_str = found[0].split("::")[0].replace("tests/", "")
                    # print("script_file_str = " + script_file_str)
            if line_str.__contains__("PASSED " + script_file_str) and script_file_str != "":
                print("case " + str(case_counter) + " PASSED")
                script_file_str = ""
            if line_str.__contains__("FAILED " + script_file_str) and script_file_str != "":
                print("case " + str(case_counter) + " FAILED")
                script_file_str = ""
            if line_str.__contains__("XFAIL " + script_file_str) and script_file_str != "":
                print("case " + str(case_counter) + " XFAIL")
                script_file_str = ""
            if line_str.__contains__("________ ERROR at") and script_file_str != "":
                print("case " + str(case_counter) + " ERROR")
                script_file_str = ""
            line = from_file.readline()


def find_suits(file_path):
    with open(file_path, 'r', encoding='utf-8') as from_file:
        line = from_file.readline()
        script_file_str = ""
        case_counter = 0
        keep_counter = True
        while line:
            line_str = line.replace("\r", "").replace("\n", "").replace("\t", "").strip()
            data = re.match(".*tests/.*.py::.*test_.*", line_str)
            if data and line_str.__contains__("pytest_main.py") is False:  # 排除pytest_main打印的
                if keep_counter:
                    case_counter += 1
                    found = re.findall("tests/test_.*.py", line_str)
                    if found:
                        print(line_str)
                        suit_info = line_str.split()[0]
                        # print("suit_info = " + suit_info)
                        sp_list = suit_info.split("::")
                        print("task_name = " + "::".join(sp_list[:-1]))
                        print("case_name = " + sp_list[-1])
                        # print(found[0].split("::")[0])
                        script_file_str = found[0].split("::")[0].replace("tests/", "")
                        # print("script_file_str = " + script_file_str)
                    if line_str.endswith("ERROR") and script_file_str != "":  # 有些失败用例直接在后面添加ERROR 信息
                        print("case " + str(case_counter) + " ERROR")
                        script_file_str = ""
            if line_str.__contains__("PASSED " + script_file_str) and script_file_str != "":
                print("case " + str(case_counter) + " PASSED")
                script_file_str = ""
            elif line_str.__contains__("FAILED " + script_file_str) and script_file_str != "":
                print("case " + str(case_counter) + " FAILED")
                script_file_str = ""
            elif line_str.__contains__("XFAIL " + script_file_str) and script_file_str != "":
                print("case " + str(case_counter) + " XFAIL")
                script_file_str = ""
            elif line_str.__contains__("________ ERROR at") and script_file_str != "":
                print("case " + str(case_counter) + " ERROR")
                script_file_str = ""
            elif line_str == "PASSED" and script_file_str != "":
                print("case " + str(case_counter) + " PASSED")
                script_file_str = ""
            elif line_str == "ERROR" and script_file_str != "":
                print("case " + str(case_counter) + " ERROR")
                script_file_str = ""
            elif line_str == "FAILED" and script_file_str != "":
                print("case " + str(case_counter) + " FAILED")
                script_file_str = ""
            elif line_str.__contains__("short test summary info"):
                keep_counter = False
            line = from_file.readline()
        print("total cases = " + str(case_counter))


if __name__ == "__main__":
    case_info = "[2022-08-19  08:02:45.005] runner.py -> run line:987 [INFO] : tests/test_volume_control.py::TestVolumeControl::test_001_音量小于等于22[声音大点] setup class：type"
    # case_info = "tests/test_volume_control.py::TestVolumeControl::test_001_音量小于等于22[声音大点] setup class：type"
    passed_info = "[2022-08-19  08:03:12.515] runner.py -> run line:987 [INFO] : PASSED test_volume_control.py -> teardown_method line:95 [INFO] : teardown():every method"
    failed_info = "[2022-08-19  08:05:40.423] runner.py -> run line:987 [INFO] : FAILED test_volume_control.py -> teardown_method line:95 [INFO] : teardown():every method"
    xfailed_info = "[2022-08-19  08:22:45.002] runner.py -> run line:987 [INFO] : XFAIL test_volume_control.py -> teardown_method line:95 [INFO] : teardown():every method"
    error_info = "________ ERROR at setup of TestVolumeControl.test_073_媒体音量查询[媒体音量是多少呢] ________"
    short_info = "=========================== short test summary info ==========================="
    print("start")
    # print(re.findall("tests/.*.py::.*test_", case_info))

    # find_cases(r"D:\projects\python\pyside6\backup\BYDauto\backup\20220819\output.txt")
    find_suits(r"D:\projects\python\pyside6\backup\logs\all_pytest.txt")
    # case_list_str = ["case1", "case2", "case5", "case3", "case4", "case5"]
    # print(case_list_str.index("case5"))
    # if "case3" in case_list_str:
    #     print("in")
    # else:
    #     print("not in")
    print("end")
