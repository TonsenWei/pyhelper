import time

import uiautomator2 as ui2

from utils.log_util import LogUtil


class Ui2Util:
    device = None

    def __init__(self, device_name=None):
        self.device = ui2.connect_usb(device_name)

    def click_by_id(self, res_id):
        self.device(resourceId=res_id).click()

    def click_by_desc(self, desc):
        self.device(description=desc).click()

    def get_text_by_id(self, res_id):
        return self.device(resourceId=res_id).get_text(timeout=3)

    def get_child(self):
        childen = self.device(resourceId="com.byd.moaais:id/recycler").child(className="android.widget.TextView")
        # print("childen_count = " + str(childen.count))
        for i in range(1, len(childen)):
            print(str(i) + ":" + childen[i].get_text())
        first_str = childen[5].get_text()
        last_str = childen[len(childen)-2].get_text()
        # print("第一次打卡：" + first_str)
        # print("最后打卡：" + last_str)
        first_time_str = first_str.split()[1]
        last_time_str = last_str.split()[1]
        # print("first_time_str = " + first_time_str)
        # print("last_time_str = " + last_time_str)
        first_times = first_time_str.split(":")
        first_minute = int(first_times[0]) * 60 + int(first_times[1])
        # print("first_minute = " + str(first_minute))
        last_times = last_time_str.split(":")
        last_minute = int(last_times[0]) * 60 + int(last_times[1])
        # print("last_minute = " + str(last_minute))
        workout_minute = (last_minute - first_minute) - 60*9
        print("加班分钟数 = " + str(workout_minute) + "分钟")
        print("加班小时数 = " + str(workout_minute/60) + "小时")

    def stop(self, timeout=10):
        self.device.uiautomator.stop()
        start_time = time.time()
        keep_wait = True
        while keep_wait:
            end_time = time.time() - start_time
            if not self.device.uiautomator.running() or end_time >= timeout:
                keep_wait = False
                LogUtil().LOGGER.info("stop uiautomator2 ok!")
                break
            else:
                time.sleep(0.3)


ui2_util = Ui2Util()

if __name__ == "__main__":
    ui2_util.stop()
    # ui2_util.click_by_desc("考勤系统")
    ui2_util.device.app_start("com.byd.moaais")
    # print(ui2_util.get_text_by_id("com.byd.moaais:id/tv_date"))
    # print(ui2_util.get_text_by_id("com.byd.moaais:id/title"))
    ui2_util.get_child()
    ui2_util.stop()
