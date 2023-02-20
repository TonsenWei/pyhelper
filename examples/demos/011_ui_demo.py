import os
import time

import uiautomator2 as ut2
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

from utils.log_util import logger

project_path = os.path.dirname(os.path.abspath(__file__))

def test_pinch():
    # 8d964c8c
    device = ut2.connect_usb("4423a4c9")
    device.uiautomator.start()
    logger.info("connect ok...")
    device.implicitly_wait(20)
    logger.info("start pinch...")
    # 从屏幕中心向外侧滑动，percent为左右起始位置占两边的比例，放大对象操作
    device().pinch_out(percent=10, steps=10)
    time.sleep(1)
    # 从屏幕外侧向中心滑动，percent为左右起始位置占两边的比例，缩小对象操作
    device().pinch_in(percent=100, steps=10)
    # device.uiautomator.stop()
    # device().gesture()

def touchAndDrage():
    """
    模拟 按下-滑动-抬起
    """
    d = ut2.connect_usb("4423a4c9")
    pos_y = 880
    # d = ut2.connect_usb("8d964c8c")
    start_x = 1920 - 20
    d.touch.down(start_x, pos_y)  # 模拟按下
    end_x = 0
    total_pix = start_x - 10
    step_count = 10
    step_pic = total_pix/step_count
    for i in range(1, step_count + 1):
        end_x = start_x - i*step_pic
        d.touch.move(end_x, pos_y)
    d.touch.up(end_x, pos_y)  # 模拟抬起

def frameRateTest():
    """
    截图帧率测试
    """
    d = ut2.connect_usb("4423a4c9")
    d.uiautomator.start()
    start_time = time.time()
    frame_counter = 0
    while True:
        frame_counter += 1
        d.screenshot(project_path + "\\pics\\" + str(frame_counter) + ".png")
        cost_time = time.time() - start_time
        if cost_time >= 1:
            print("ui2 screencap frame = " + str(frame_counter))
            frame_counter = 0
            start_time = time.time()


if __name__ == "__main__":
    '''
    # pytest -v 说明：可以输出用例更加详细的执行信息，比如用例所在的文件及用例名称等
    # pytest -s 说明：输入我们用例中的调式信息，比如print的打印信息等
    # pytest -m ”标记“ 说明：执行特定的测试用例,如下：
    # @pytest.mark.run_this_testcase
    # def testOpenUrl():
    #     pass
    # pytest -m run_this_testcase,就是mark后面的参数
    # pytest -k "关键字" 说明：执行用例包含“关键字”的用例，比如：
    # pytest -k 'OpenUrl'
    # -x ：用例失败时立即停止测试；
    # "--reruns=2"

    project_path + "/tests" : 查找case目录
    --html=report.html ： 输出html报告
    '''
    # pytest.main(["-v", "-s", project_path, "--html=report.html"])
    # poco = AndroidUiautomationPoco()
    # poco.device.wake()
    # poco(text='显示').click()
    # touchAndDrage()
    test_pinch()
    # frameRateTest()
    # d = ut2.connect_usb("4423a4c9")
    # print("start ...")
    # print("is running? = " + str(d.uiautomator.running()))
    # print("stop uiautomator ...")
    # # d.uiautomator.stop()
    # time.sleep(5)
    # print("check uiautomator is stop ...")
    # print("is running? = " + str(d.uiautomator.running()))
    # print("start uiautomator ...")
    # d.uiautomator.start()
    # time.sleep(10)
    # print("check is started ...")
    # print("is running? = " + str(d.uiautomator.running()))
