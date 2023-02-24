import serial
import time
import threading
import sys
import os

sys.path.insert(0, '../')
from utils.log_util import LogUtil

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class SerialUtil:
    """
    串口工具类
    """
    message = ''
    keep_read = True

    def __init__(self, port, buand):
        super(SerialUtil, self).__init__()
        self.port = serial.Serial(port, buand)
        self.port.close()
        if not self.port.isOpen():
            self.port.open()

    def open(self):
        if not self.port.is_open():
            self.port.open()

    def close(self):
        self.port.close()

    def send(self, msg):
        self.port.write(msg.encode())

    def read(self):
        while self.keep_read:
            try:
                self.message = self.port.readline()
                LogUtil().LOGGER.info(self.message.decode("utf-8").replace("\n", "").replace("\t", ""))
            except:
                LogUtil().LOGGER.error("try exception....")
                pass

    def stop_read(self):
        self.keep_read = False


if __name__ == "__main__":
    # def serial_sync(port = "/dev/ttyUSB0", baudrate = 921600):
    mSerialSync = SerialUtil("COM29", 9600)
    tSync = threading.Thread(target=mSerialSync.read)
    tSync.daemon = True
    tSync.start()
    mSerialSync.send("root\r")
    time.sleep(1)
    mSerialSync.send("sv2655888\r")
    time.sleep(1)
    mSerialSync.send("rm -rf /var/share/itest.xml\n")
    time.sleep(1)
    mSerialSync.send("sync\n")
    time.sleep(3)
    mSerialSync.send("ls -l /var/share\n")
    time.sleep(3)
    mSerialSync.stop_read()
    mSerialSync.close()
