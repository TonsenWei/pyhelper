import serial
import time
import threading
import sys
import os


this_file_path = os.path.dirname(os.path.abspath(__file__))


class SerialUtil:
    '''
    串口工具类
    '''
    message = ''
    keep_read = True
    send_str = None
    ready = False
    def __init__(self, port, buand):
        super(SerialUtil, self).__init__()
        self.port = serial.Serial(port, buand)
        self.port.close()
        if not self.port.isOpen():
            self.port.open()
            
    def get_send_str(self):
        return self.send_str
    
    def is_ready(self):
        return self.ready

    def set_ready(self, value=False):
        self.ready = value
        
    def open(self):
        if not self.port.is_open():
            self.port.open()
    
    def close(self):
        self.port.close()

    def send_ctrl_c(self):
        print("send ctrl c")
        self.port.write("\n^c\n".encode("utf-8"))
        time.sleep(0.2)

    def send(self, msg):
        print("send msg:" + str(msg))
        self.port.write(msg.encode("utf-8"))
        # time.sleep(0.2)
    
    def read(self):
        """读串口数据，根据读回来的串口输入写入对应的值
        """
        while self.keep_read:
            try:
                read_msg = self.port.readline()
                print(read_msg.decode("utf-8").replace("\n","").replace("\t",""))
                self.message = read_msg.decode("utf-8").replace("\n","").replace("\t","")
                if self.message.__contains__("range"):
                    to_write = get_value(self.message, 1)  # range: 0~10
                    if to_write is not None:
                        if to_write.strip() == "":
                            # print("-------------strip write: " + to_write)
                            # # value = float(to_write) - 1
                            # self.send("1\n")
                            self.send_str = "1\n"
                            self.ready = True
                        else:
                            # print("-------------write: " + to_write)
                            # self.send(to_write + "\n")
                            self.send_str = to_write + "\n"
                            self.ready = True
                    # print(line.replace('\r', '').replace('\n', ''))
                elif self.message.__contains__("0 or 1"):
                    # print(line.replace('\r', '').replace('\n', ''))
                    # print("-------------write: 1")
                    # self.send("1\n")
                    self.send_str = "1\n"
                    self.ready = True
                elif self.message.__contains__("max size is"):
                    # print(line.replace('\r', '').replace('\n', ''))
                    # print("-------------write: 1")
                    # self.send("1\n")
                    self.send_str = "1\n"
                    self.ready = True
                elif self.message.__contains__("max") and self.message.__contains__("string format"):
                    # print(line.replace('\r', '').replace('\n', ''))
                    # print("write: 1")
                    # self.send("1\n")
                    self.send_str = "1\n"
                    self.ready = True
                elif self.message.__contains__("value:"):
                    # 0xa0
                    # print(line.replace('\r', '').replace('\n', ''))
                    # print("-------------write 0xa0")
                    # self.send("0xa0\n")
                    self.send_str = "0xa0\n"
                    self.ready = True
                elif self.message.__contains__("0 0r 1"):
                    # print(line.replace('\r', '').replace('\n', ''))
                    # print("-------------write: 1")
                    # self.send("1\n")
                    self.send_str = "1\n"
                    self.ready = True
            except:
                print("try exception....")
                pass
    
    def stop_read(self):
        self.keep_read = False


def get_value(line="", target=1):
    """获取range后面的数字，line为某行的字符串，target表示获取最大值还是最小值

    Args:
        line (str, optional): [串口接收到的字符串]. Defaults to "".
        target (int, optional): [获取最大值还是最小值]. Defaults to 1.

    Returns:
        [type]: [返回需要的值，None为获取不到任何值]
    """
    range_list = line.split("range:")
    range_list_len = len(range_list)
    # print("range_list = " + str(range_list_len))
    result = None
    if range_list_len == 2:
        right_str = range_list[1]
        # print(right_str)
        if right_str.__contains__(","):
            comma_list = right_str.split(",")
            if len(comma_list) == 2:
                value_list = comma_list[0].replace(")", "").split("~")
                # print(comma_list[0].replace(")", ""))
                print("-------------value = " + value_list[0] + ", " + value_list[1])
                if target == 1:
                    return value_list[0]
                else:
                    return value_list[1]
        elif right_str.__contains__(")"):
            brackets_list = right_str.split(")")
            value_list = brackets_list[0].split("~")
            # print(brackets_list[0])
            print("-------------value = " + value_list[0] + ", " + value_list[1])
            if target == 1:
                return value_list[0]
            else:
                return value_list[1]
        # range_list[1]


def test_file():
    test_from_file_path = this_file_path + "\\sample.txt"
    with open(test_from_file_path, 'r', encoding='utf-8') as from_file:
        line = from_file.readline()
        counter = 0;
        while line:
            # print("line = " + line.replace('\r', '').replace('\n', ''))
            if line.__contains__("range"):
                counter += 1
                value_target = get_value(line, 1)
                if value_target is not None:
                    print("-------------write value_target = " + value_target)
                # print(line.replace('\r', '').replace('\n', ''))
            elif line.__contains__("0 or 1"):
                counter += 1
                # print(line.replace('\r', '').replace('\n', ''))
                # print("write: 1")
            elif line.__contains__("max size is"):
                counter += 1
                # print(line.replace('\r', '').replace('\n', ''))
                # print("write: 1")
            elif line.__contains__("max") and line.__contains__("string format"):
                counter += 1
                # print(line.replace('\r', '').replace('\n', ''))
                # print("write: 1")
            elif line.__contains__("value:"):
                # 0xa0
                counter += 1
                # print(line.replace('\r', '').replace('\n', ''))
                # print("write 0xa0")
            elif line.__contains__("0 0r 1"):
                counter += 1
                # print(line.replace('\r', '').replace('\n', ''))
                # print("write: 1")
            line = from_file.readline()
        print("-------------counter = " + str(counter))


if __name__ == "__main__":
    print("start...")
    # test_file()
    mSerialSync = SerialUtil("COM21", 115200)
    tSync = threading.Thread(target=mSerialSync.read)
    tSync.daemon = True
    tSync.start()
    time.sleep(5)
    mSerialSync.send_ctrl_c()
    # mSerialSync.send("^c\n")
    # time.sleep(1)
    mSerialSync.send("cd /app/bin\n")
    time.sleep(1)
    mSerialSync.send("./tx_sample 2\n")
    time.sleep(1)
    mSerialSync.send("c\n")
    time.sleep(3)
    mSerialSync.send("e\n")
    time.sleep(2)
    mSerialSync.send("d\n")
    time.sleep(1)
    # tSync.start()

    while True:
        if mSerialSync.is_ready():
            mSerialSync.send(mSerialSync.get_send_str())
            mSerialSync.set_ready(False)
            time.sleep(0.5)
        else:
            time.sleep(0.3)

