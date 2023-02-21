import threading
import time
import inspect
import ctypes

import multiprocessing
from playsound import playsound


class Mp3PlayerThread (threading.Thread):
    """线程的方式播放mp3

    Args:
        threading ([type]): [description]
    """
    def __init__(self, filepath, timeout):
        threading.Thread.__init__(self)
        self.filepath = filepath
        self.timeout = timeout
        self.player = Mp3Player()

    def run(self):
        self.player.play(self.filepath, self.timeout)  # 阻塞方式播放

    def stop(self):
        self.player.stop()  # 停止播放


class Mp3Player(object):
    """mp3播放器
    使用playsound库（或Play_mp3, pip install Play_mp3）

    Args:
        object ([type]): [使用多进程方式播放mp3]
    """
    def __init__(self):
        self.filepath = ""
        self.process = multiprocessing.Process(
            target=playsound, args=(self.filepath,))

    def play(self, filepath, timeout=0):
        """开始播放mp3

        Args:
            filepath ([str]): [mp3文件路径]
            timeout (int, optional): [播放超时时间]. Defaults to 0.
        """
        self.filepath = filepath
        if self.process:
            if self.process.is_alive():
                self.process.terminate()
        self.process = multiprocessing.Process(target=playsound, args=(self.filepath,))
        self.process.start()
        if timeout is None or timeout == 0:  # 如果没有输入超时时间或超时时间为0，则播放到自动结束
            while self.process.is_alive():
                time.sleep(0.3)
        else:  # 如果设置了超时时间，则超时时间到则退出，超时时间到之前如果播放完毕也直接退出
            start_time = time.time()
            time_counter = 0
            while self.process.is_alive() and time_counter < timeout:
                time.sleep(0.3)
                time_counter = time.time() - start_time
            if self.process.is_alive():
                self.process.terminate()

    def stop(self):
        """停止播放，使用停止进程的方式停止
        """
        if self.process:
            if self.process.is_alive():
                self.process.terminate()


if __name__ == "__main__":
    """使用Play_mp3模块播放MP3测试
    需要pip install Play_mp3安装模块，其实底层也是使用了playsound模块
    """
    # Play_mp3.play(r"D:\uidq0460\Music\ABV-Sarvar.mp3")
    print("thread 1...")
    thread1 = Mp3PlayerThread(r"D:\Users\Music\流行\错位时空.mp3", 20)
    thread2 = Mp3PlayerThread(r"D:\Users\Music\流行\广寒宫 - 糯米Nomi.mp3", 20)
    thread1.start()
    thread2.start()
    print("stop...")
    time.sleep(20)
    # print("thread 2...")
    # thread1 = Mp3PlayerThread(r"D:\Users\Music\流行\广寒宫 - 糯米Nomi.mp3", 3)
    # thread1.start()
    # # thread1.join()
    # time.sleep(15)
    # print("thread 3...")
    # thread1 = Mp3PlayerThread(r"D:\Users\Music\流行\广寒宫 - 糯米Nomi.mp3", 3)
    # thread1.start()
    # # thread1.join()
    # time.sleep(1)
    # print("thread 4...")
    # thread1 = Mp3PlayerThread(r"D:\Users\Music\流行\广寒宫 - 糯米Nomi.mp3", 3)
    # thread1.start()
    # # thread1.join()
    # print("wait...")
    # # thread1.stop()
    # # thread1.stop()
    # time.sleep(30)
    print("exit main...")
