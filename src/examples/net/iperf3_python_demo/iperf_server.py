import os
import atexit  # 退出处理
import threading
import subprocess  # 进程，管道
from sys import platform as sysPlatform  # popen静默模式

InitTimeout = 20  # 初始化超时时间，秒


class IperfServer:

    def __init__(self, exePath, argsStr="") -> object:
        self.exePath = exePath
        self.cwd = os.path.abspath(os.path.join(exePath, os.pardir))  # 获取exe父文件夹
        # 处理启动参数
        args = ' -s'
        if argsStr:  # 添加用户指定的启动参数
            args += f' {argsStr}'
        self.args = args
        self.ret = None

    def run(self):
        # 设置子进程启用静默模式，不显示控制台窗口
        startupinfo = None
        if 'win32' in str(sysPlatform).lower():
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
        self.ret = subprocess.Popen(  # 打开管道
            self.exePath + self.args, cwd=self.cwd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            startupinfo=startupinfo  # 开启静默模式
        )
        atexit.register(self.stop)  # 注册程序终止时执行强制停止子进程
        # self.psutilProcess = psutilProcess(self.ret.pid)  # 进程监控对象

        self.initErrorMsg = f'iperf3 init fail.\n程序路径：{self.exePath}\n启动参数：{self.args}'

        # 子线程检查超时
        # def cancelTimeout():
        #     # print('进程启动计时器取消')
        #     checkTimer.cancel()
        #
        # def checkTimeout():
        #     # print('进程启动计时器触发')
        #     self.initErrorMsg = f'iperf3 init timeout: {InitTimeout}s.\n{self.exePath}'
        #     self.ret.kill()  # 关闭子进程

        # checkTimer = threading.Timer(InitTimeout, checkTimeout)
        # checkTimer.start()

        # 循环读取，检查成功标志
        initStr = ""
        while True:
            # if not self.ret.poll() == None:  # 子进程已退出，初始化失败
            #     cancelTimeout()
            #     raise Exception(self.initErrorMsg)
            # 必须按行读，所以不能使用communicate()来规避超时问题
            initStr = self.ret.stdout.readline().decode('utf-8', errors='ignore')
            if initStr.strip():
                # print(f"line: {initStr.strip()}")
                print(initStr.replace("\n", ""))
            # if 'Server listening on' in initStr:  # 初始化成功
            #     break
        # cancelTimeout()

    def stop(self):
        try:
            if self.ret is not None:
                self.ret.kill()  # 关闭子进程。误重复调用似乎不会有坏的影响
        except Exception as e:
            print(e)

    def __del__(self):
        self.stop()
        atexit.unregister(self.stop)  # 移除退出处理
        print('IperfServer 析构！')


if __name__ == "__main__":
    print("start")
    # server = IperfServer(r"iperf3.exe", argsStr="-J")  # -J: json格式返回
    server = IperfServer(r"iperf3.exe", argsStr="")  # -J: json格式返回
    server.run()  # 会发生阻塞，若在GUI中需在线程中启动，通过线程控制服务启动和停止
    server.stop()
    print('end')
