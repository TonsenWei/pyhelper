# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/2/28 17:03
@File : 042_txt_to_allure_json.py
@Desc : 
"""
import json
import os
import random
import socket
import string

import uuid

TEST_INOF = "TestInformation"
ATTACHMENT = "Attachment"
RUN_TYPE = "RunType"
ONE_CASE = "OneCase"
ONE_SUIT = "OneSuit"
SUMMARY = "Summary"
RUN_SUITS = "RunSuits"
TASK_NAME = "TaskName"
CASE_NAME = "CaseName"
EXP_TIMES = "expectTimes"
LOOP_COUNTER = "LoopCounter"
STATUS = "Status"
TIMESTAMP = "timestamp"
TOTAL = "total_cases"
FAILED_CASES = "fail_cases"
PASSED_COUNT = "pass_counter"
PASSED_RATE = "pass_rate"
COST_TIME = "cost_time"
START_TIME = "start"
STOP_TIME = "stop"

ATTA_TYPE = "type"
ATTA_VALUE = "value"
ATTA_STATE = "status"
TYPE_STR = "str"  # {"type": "str", "value": "str_value", "status": "error"}
TYPE_PNG = "png"  # {"type": "png", "value": ["png_path1", "png_path2"], "status": "passed"}


class TxtToAllureJson:

    @staticmethod
    def getStatusDetails(message, trace, stripedLine):
        """
        解析行
        :param trace:
        :param message:
        :param stripedLine:
        :return:
        """
        # message, trace = "", ""
        splitStr = "{\"RunType\":\"Attachment\", \"type\":\"str\", \"value\":\""
        res = stripedLine.split(splitStr)[1]
        attaValue = res.split("\", \"Status\":")[0]
        attaStatus = res.split("\", \"Status\":")[1].replace("\"", "").replace("}", "")
        if attaStatus == "fail" or attaStatus == "failed" or attaStatus == "error":
            valueLines = attaValue.split("\r\n")
            failInfo = attaValue
            if len(valueLines) > 0:
                failInfo = valueLines[-1]
            if message != "":
                message = f"{message}\r\n{failInfo}"
            else:
                message = failInfo
        if trace != "":
            trace = f"{trace}\r\n{attaValue}"
        else:
            trace = attaValue
        return message, trace

    @staticmethod
    def getImgsNames(lineDict):
        attachments = []
        if lineDict is None:
            return attachments
        attaValue = lineDict.setdefault(ATTA_VALUE, "")
        imgs = eval(attaValue.replace("\\", "\\\\"))
        for pngIndex, img in enumerate(imgs):
            fpath, fname = os.path.split(img)
            attachments.append(fname)
        return attachments

    @staticmethod
    def genCaseJson(taskName, caseName, status, message, trace, startInt, stopInt, attachments, dirPath):
        """
        生成用例结果json信息
        :param taskName:
        :param caseName:
        :param status:
        :param message:
        :param trace:
        :param startInt:
        :param stopInt:
        :param attachments:
        :param dirPath:
        :return:
        """
        if taskName is not None and caseName is not None:  # 不为空，则说明检索完一条用例
            resultJson = {}
            resultJson.setdefault("name", caseName)
            resultJson.setdefault("status", status)
            statusDetails = {}
            if status == "passed" or status == "pass":
                message = "passed, clicked to show more"
            statusDetails.setdefault("message", message)
            statusDetails.setdefault("trace", trace)
            resultJson.setdefault("statusDetails", statusDetails)
            if len(attachments) > 0:
                attachs = []
                for aIndex, atta in enumerate(attachments):
                    imgAtt = {}
                    imgAtt.setdefault("name", f"{aIndex + 1}_图片")
                    imgAtt.setdefault("source", f"{atta}")
                    imgAtt.setdefault("type", f"image/png")
                    attachs.append(imgAtt)
                resultJson.setdefault("attachments", attachs)
            resultJson.setdefault("statusDetails", statusDetails)
            resultJson.setdefault("start", startInt)
            resultJson.setdefault("stop", stopInt)
            resultJson.setdefault("uuid", str(uuid.uuid5(uuid.NAMESPACE_X500, caseName)))
            id32 = ''.join(random.sample(string.ascii_letters + string.digits, 32))
            resultJson.setdefault("historyId", id32.lower())
            caseId32 = ''.join(random.sample(string.ascii_letters + string.digits, 32))
            resultJson.setdefault("testCaseId", caseId32.lower())
            resultJson.setdefault("fullName", f"{taskName}#{caseName}")
            labels = []
            # parentSuite = {}
            # parentSuite.setdefault("name", "parentSuite")
            # parentSuite.setdefault("value", "tests")
            # labels.append(parentSuite)
            suite = {}
            suite.setdefault("name", "suite")
            suite.setdefault("value", taskName)
            labels.append(suite)
            # subSuite = {}
            # subSuite.setdefault("name", "subSuite")
            # subSuite.setdefault("value", taskName)
            # labels.append(subSuite)
            package = {}
            package.setdefault("name", "package")
            package.setdefault("value", taskName)
            # package.setdefault("value", "parentSuite.suite.tests")
            labels.append(package)
            hostname = socket.gethostname()
            host = {}
            host.setdefault("name", "host")
            host.setdefault("value", hostname)
            labels.append(host)
            framework = {}
            framework.setdefault("name", "framework")
            framework.setdefault("value", "Std_AutoTest")
            labels.append(framework)
            language = {}
            language.setdefault("name", "language")
            language.setdefault("value", "python3")
            labels.append(language)
            thread = {}
            thread.setdefault("name", "thread")
            thread.setdefault("value", "3856-MainThread")
            labels.append(thread)
            resultJson.setdefault("labels", labels)
            fileName = f"{str(uuid.uuid1())}-result.json"
            # dirPath = r"D:\projects\python\pylearning\examples\demos\allure_data"
            fullPath = f"{dirPath}\\{fileName}"
            with open(fullPath, "w", encoding="utf-8") as json_append:
                json.dump(resultJson, json_append, ensure_ascii=False, indent=4,
                          separators=(',', ': '))

    @staticmethod
    def genAllureData(txtPath, dirPath):
        with open(txtPath, "r+", encoding="utf8") as reportTxt:
            reportType = ""
            expectTimes = None
            loopCounter = None

            line = reportTxt.readline()

            totalCostTime = 0
            taskNameList = []
            multiSuits = False
            counter = 0
            lastLoopTimeStamp = None
            currentSuitTimeStamp = None
            taskBeforeCostTime = 0
            attachType = TYPE_PNG
            taskName = None
            caseName = None
            status = "failed"
            message = ""
            trace = ""
            startInt = 0
            stopInt = 0
            attachments = []
            lineDict = None
            while line:
                stripedLine = line.strip()
                if stripedLine != "":
                    if stripedLine.startswith("{\"RunType\":\"Attachment\", \"type\":\"str\", \"value\":\""):
                        currentType = ATTACHMENT
                        attachType = TYPE_STR
                    elif stripedLine.startswith("{\"RunType\":\"Attachment\", \"type\":\"png\", \"value\":\""):
                        currentType = ATTACHMENT
                        attachType = TYPE_PNG
                        lineDict = eval(line)
                    else:
                        lineDict = eval(line)
                        currentType = lineDict.setdefault(RUN_TYPE, "")
                    if currentType == ONE_CASE:
                        reportType = ONE_CASE
                        # startCaseTime = float(lineDict.setdefault(TIMESTAMP, "0"))
                    elif currentType == ONE_SUIT:
                        reportType = ONE_SUIT
                        # startCaseTime = float(lineDict.setdefault(TIMESTAMP, "0"))
                    elif currentType == RUN_SUITS:
                        reportType = RUN_SUITS
                        try:
                            expectTimes = int(lineDict[EXP_TIMES])  # 转换成功
                        except Exception as e:
                            pass
                        try:
                            loopCounter = int(lineDict[LOOP_COUNTER])
                            if lastLoopTimeStamp is None:
                                lastLoopTimeStamp = float(lineDict[TIMESTAMP])
                                currentSuitTimeStamp = lastLoopTimeStamp
                            else:
                                lastLoopTimeStamp = currentSuitTimeStamp
                                currentSuitTimeStamp = float(lineDict[TIMESTAMP])
                        except Exception as e:
                            pass
                    if reportType == ONE_CASE or reportType == ONE_SUIT:
                        # 第一次检测到时，taskName caseName为空，第二次检测到时是第二条，则之前收集的信息都是第一条的
                        if currentType == TEST_INOF:
                            TxtToAllureJson.genCaseJson(taskName, caseName, status, message, trace,
                                                        startInt, stopInt, attachments, dirPath)
                            attachments.clear()
                            taskName = lineDict.setdefault(TASK_NAME, "未知")
                            caseName = lineDict.setdefault(CASE_NAME, "未知")
                            status = lineDict.setdefault(STATUS, "")
                            if status.lower() == "fail" or status.lower() == "failed":
                                status = "failed"
                            elif status.lower() == "pass" or status.lower() == "passed":
                                status = "passed"
                            if taskName not in taskNameList:
                                taskNameList.append(taskName)
                            caseCostTime = float(lineDict.setdefault(COST_TIME, "0"))
                            startTimeF = float(lineDict.setdefault(START_TIME, "0"))
                            startInt = int(startTimeF*1000)
                            stopInt = int((startTimeF + caseCostTime)*1000)
                            totalCostTime += caseCostTime
                        elif currentType == ATTACHMENT:
                            if attachType == TYPE_STR:
                                # 获取trace，解析msg
                                message, trace = TxtToAllureJson.getStatusDetails(message, trace, stripedLine)
                            elif attachType == TYPE_PNG:
                                attachment = TxtToAllureJson.getImgsNames(lineDict)
                                attachments.extend(attachment)
                        elif currentType == SUMMARY:
                            TxtToAllureJson.genCaseJson(taskName, caseName, status, message, trace,
                                                        startInt, stopInt, attachments, dirPath)
                            attachments.clear()
                    elif reportType == RUN_SUITS:
                        if expectTimes is not None and expectTimes != "":
                            if expectTimes > 1:
                                multiSuits = True
                            else:
                                multiSuits = False
                        if loopCounter is not None and loopCounter != "":
                            counter = loopCounter
                        if currentType == TEST_INOF:
                            TxtToAllureJson.genCaseJson(taskName, caseName, status, message, trace,
                                                        startInt, stopInt, attachments, dirPath)
                            attachments.clear()
                            taskName = lineDict.setdefault(TASK_NAME, "未知")
                            if multiSuits is True:
                                taskName = f"{taskName}[{counter}]"
                            caseName = lineDict.setdefault(CASE_NAME, "未知")
                            status = lineDict.setdefault(STATUS, "")
                            if status.lower() == "fail" or status.lower() == "failed":
                                status = "failed"
                            elif status.lower() == "pass" or status.lower() == "passed":
                                status = "passed"
                            if taskName not in taskNameList:
                                taskNameList.append(taskName)
                                if len(taskNameList) > 0 and currentSuitTimeStamp is not None and lastLoopTimeStamp is not None:
                                    taskBeforeCostTime += (currentSuitTimeStamp - lastLoopTimeStamp)
                                    # html_report.modify_suit_time(
                                    #     TimeUtil.time_simple(currentSuitTimeStamp - lastLoopTimeStamp))
                            caseCostTime = float(lineDict.setdefault(COST_TIME, "0"))
                            startTimeF = float(lineDict.setdefault(START_TIME, "0"))
                            startInt = int(startTimeF * 1000)  # 报告时间以毫秒为单位
                            stopInt = int((startTimeF + caseCostTime) * 1000)
                            totalCostTime += caseCostTime
                        elif currentType == ATTACHMENT:
                            if attachType == TYPE_STR:  # 字符串
                                # 获取trace，解析msg
                                message, trace = TxtToAllureJson.getStatusDetails(message, trace, stripedLine)
                            elif attachType == TYPE_PNG:  # 图片，解析为附件
                                attachment = TxtToAllureJson.getImgsNames(lineDict)
                                attachments.extend(attachment)
                        elif currentType == SUMMARY:
                            TxtToAllureJson.genCaseJson(taskName, caseName, status, message, trace,
                                                        startInt, stopInt, attachments, dirPath)
                            attachments.clear()
                    line = reportTxt.readline()


if __name__ == "__main__":
    TxtToAllureJson.genAllureData(r"D:\projects\python\pyside2_prjs\std_autotest\output\report\2023-03-01_14-11-04\report.txt",
                                  "./allure_data/")
