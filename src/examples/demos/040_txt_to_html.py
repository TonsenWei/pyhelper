# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/2/13 11:12
@File : 040_txt_to_html.py
@Desc : 
"""
TEST_INOF = "TestInformation"
ATTACHMENT = "Attachment"
RUN_TYPE = "RunType"
ONE_CASE = "OneCase"
ONE_SUIT = "OneSuit"
RUN_SUITS = "RunSuits"
TASK_NAME = "TaskName"
CASE_NAME = "CaseName"
EXP_TIMES = "expectTimes"
LOOP_COUNTER = "LoopCounter"
STATUS = "Status"
ATTA_TYPE = "type"

def txtToHtml(txtPath):
    with open(txtPath, "r+", encoding="utf8") as reportTxt:
        # html_report = ReportAs()
        reportType = None
        currentType = None
        expectTimes = None
        line = reportTxt.readline()
        while line:
            try:
                lineDict = eval(line)
                currentType = lineDict.setdefault(RUN_TYPE, "")
                if currentType == ONE_CASE:
                    reportType = ONE_CASE
                elif currentType == ONE_SUIT:
                    reportType = ONE_SUIT
                elif currentType == RUN_SUITS:
                    reportType = RUN_SUITS
                if reportType == ONE_CASE:
                    if currentType == TEST_INOF:
                        taskName = lineDict.setdefault(TASK_NAME, "未知")
                        caseName = lineDict.setdefault(CASE_NAME, "未知")
                        status = lineDict.setdefault(STATUS, "")
                        print(f"taskName={taskName}, caseName={caseName}, status={status}")
                    elif currentType == ATTACHMENT:
                        attaType = lineDict.setdefault(ATTA_TYPE, "")
                        print(f"attaType={attaType}")
            except Exception as e:
                print(e)
            line = reportTxt.readline()


if __name__ == "__main__":
    txtToHtml(r"D:\projects\python\pyside2_prjs\std_autotest\output\report\2023-02-13_11-37-49\report.txt")