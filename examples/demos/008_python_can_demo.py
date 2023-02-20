"""
利用虚拟总线可以在没有硬件的情况下实现跟底层无关的代码，不需要使用任何驱动和dll，只需要使用python-can就可以完成。

需要注意的是在总线上有收发节点，不同的节点要连接在相同的虚拟总线上，这些节点必须在同一个python应用里边实现，
也就是说如果，你写了两个py脚本，一个发送，一个接收，这两个脚本分别运行，他们之间的虚拟总线是没有连接的，所以是不能互相通讯的。

在我们的virtual_bus.py代码中

我们创建了一个发送(bus_tx)，一个接收(bus_rx)两个节点，并都连接到virtual_ch上
我们创建了一个名为logger的日志记录器，该日志记录器会将受到的信息写入到logfile.asc文件，
记录器会根据文件的后缀来决定写入的格式，因此，它将会生成一个asc格式的日志，如果这里后缀为csv，
blf或者其它，则会生成相应格式的文件。
日志记录器logger被放置到了一个listeners的列表中，里边还包含一个print_message的回调函数，
这个是我们自己实现的函数，只是简单的将输入参数msg打印出来。
listeners列表通过Notifier绑定到接收节点（bus_rx），这样只要有新的消息在接收节点上收到，
这两个listener就会被执行，print_message会将消息打印到终端，而logger会将消息写入到logfile.asc文件。

为了实现周期发送消息，我们自己定义了一个线程，在线程中，会每隔0.5s发送CANID为0x7E0，数据为随机的CAN消息到总线上 。
使用can.Message来构建CAN消息对象，而使用bus.send就可以将消息发送出去。
脚本会监控键盘按键，一旦有任何按键被按下，脚本则会进入退出程序，在退出部分一定要调用notifier.stop()来停止 notifier ，
只有这样才能确保logger能够完整正确的写入日志，如果不显示的调用这个函数来停止，则日志内容无法成功写入。
"""

import can
import threading
import time
import random

def print_message(msg):
    print(msg)

class tx_thread_cl:

    def __init__(self, bus):
        self.bus = bus
        self.running = True
        self.thread = threading.Thread(target=self.tx_callback, args=(self.bus,))
        self.finished = False
    
    def start(self):
        self.thread.start()

    def tx_callback(self, bus):
        while self.running:
            data = [random.randint(0,15) for i in range(0,8)]
            msg = can.Message(is_extended_id=False, arbitration_id=0x7E0, data=data)
            bus.send(msg)
            time.sleep(0.5)
        self.finished = True
    
    def stop(self):
        self.running = False

if __name__ == "__main__":
    # RX part
    bus_rx = can.interface.Bus('virtual_ch', bustype='virtual')
    logger = can.Logger("logfile.asc")  # save log to asc file
    listeners = [
        print_message,  # Callback function, print the received messages
        logger,  # save received messages to asc file
    ]
    notifier = can.Notifier(bus_rx, listeners)

    # TX part
    bus_tx = can.interface.Bus('virtual_ch', bustype='virtual')
    tx_service = tx_thread_cl(bus_tx)
    tx_service.start()

    running = True
    while running:
        input()
        running = False
    
    while not tx_service.finished:
        tx_service.stop()

    # It's important to stop the notifier in order to finish the writting of asc file
    notifier.stop()
    # stops the bus
    bus_tx.shutdown()
    bus_rx.shutdown()