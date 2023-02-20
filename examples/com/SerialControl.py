import serial
import time
import threading
import WriteLog

class SerialControl(object):
    def __init__(self,baudrate,portNum,fileSavePath):
       self.baudrate = baudrate
       self.portNum = "COM"+str(portNum)
       self.fileSavePath = fileSavePath
       self.writeLogHandle = WriteLog.WriteLog(self.fileSavePath)
       self.__connect()
       self.readFlag = False
    def serialWrite(self,writeData):
       writeData = writeData+"\r\n"
       self.serHandle.write(writeData.encode())
    def ReadData(self):
       self.readFlag = True
       thread1 = threading.Thread(target = self.__serialReadLine)
       thread1.setDaemon(False)
       thread1.start()
    def __connect(self):
       self.serHandle=serial.Serial(self.portNum)
       self.serHandle.baudrate=self.baudrate
       self.serHandle.timeout=5
    def __serialReadLine(self):
       self.writeLogHandle.getProcessHandle("SerialLog")
       while self.readFlag:
           self.receivedata=self.serHandle.readline()
           try:
              self.receivedata = bytes(self.receivedata).decode('ascii')
              print("receive = " + str(self.receivedata))
              self.writeLogHandle.writeProcessLog(self.receivedata)
           except:
              print("except")
              pass
       self.writeLogHandle.closeProcessLogHandle()
       print("closed")
    def stopConnect(self):
       self.serHandle.close()

if __name__ == "__main__":
    se = SerialControl(115200,4,r'D:\z')
    se.serialWrite('root')
    time.sleep(2)
    ss =se.ReadData()
    print(ss)
    time.sleep(5)
    se.readFlag = False
    time.sleep(3)

