import os
import time


class WriteLog(object):
       def __init__(self,filepath):
              self.writeLogPath = filepath
              self.creatFold()
       def creatFold(self):
              if not os.path.exists(self.writeLogPath):
                     os.makedirs(self.writeLogPath)
       def getProcessHandle(self,testName):
              timename = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
              file_path_str = self.writeLogPath+"\\"+testName+timename+".txt"
              print("file_path_str = " + file_path_str)
              self.writeProcessDataHandle = open(file_path_str,"a+")
       def writeProcessLog(self,processData):
              processData = processData.replace("\n","")
              self.writeProcessDataHandle.write(processData+"\n")
       def closeProcessLogHandle(self):
               self.writeProcessDataHandle.close()
if __name__ == "__main__":
       writeLog = WriteLog()
       writeLog.writeResultLog("CSD","PASS")
