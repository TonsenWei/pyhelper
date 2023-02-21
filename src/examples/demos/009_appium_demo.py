"""
pip install Appium-Python-Client
"""
# 导入webdriver
import time

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.multi_action import MultiAction
from appium.webdriver.common.touch_action import TouchAction

# 初始化参数
desired_caps = {
    'platformName': 'Android',  # 被测手机是安卓
    'platformVersion': '11',  # 手机安卓版本
    'deviceName': 'emulator-5554',  # 设备名，安卓手机可以随意填写
    'appPackage': 'crixec.adbtoolkitsinstall',  # 启动APP Package名称
    'appActivity': '.MainActivity',  # 启动Activity名称
    'unicodeKeyboard': True,  # 使用自带输入法，输入中文时填True
    'resetKeyboard': True,  # 执行完程序恢复原来输入法
    'noReset': True,  # 不要重置App，如果为False的话，执行完脚本后，app的数据会清空，比如你原本登录了，执行完脚本后就退出登录了
    'newCommandTimeout': 6000,
    'automationName': 'UiAutomator2'
}
# 连接Appium Server，初始化自动化环境
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

x = driver.get_window_size()['width']
y = driver.get_window_size()['height']
print("x = " + str(x) + ", y=" + str(y))

def pinch():
    action1 = TouchAction(driver)
    action2 = TouchAction(driver)
    zoom_action = MultiAction(driver)

    action1.press(x=x * 0.2, y=y * 0.2).wait(1000).move_to(x=x * 0.4, y=y * 0.4).wait(1000).release()
    action2.press(x=x * 0.8, y=y * 0.8).wait(1000).move_to(x=x * 0.6, y=y * 0.6).wait(1000).release()

    print('start pinch...')
    zoom_action.add(action1, action2)
    zoom_action.perform()


def zoom():
    action1 = TouchAction(driver)
    action2 = TouchAction(driver)
    zoom_action = MultiAction(driver)

    action1.press(x=x * 0.4, y=y * 0.4).wait(1000).move_to(x=x * 0.2, y=y * 0.2).wait(1000).release()
    action2.press(x=x * 0.6, y=y * 0.6).wait(2000).move_to(x=x * 0.8, y=y * 0.8).wait(2000).release()
    print('start zoom...')
    zoom_action.add(action1, action2)
    zoom_action.perform()


# 退出程序，记得之前没敲这段报了一个错误 Error: socket hang up 啥啥啥的忘记了，有兴趣可以try one try
print("send key 3 ...")
driver.press_keycode("3")
text_str = "Gallery"
time.sleep(1)
els = driver.find_elements_by_android_uiautomator("new UiSelector().text(\"" + str(text_str) + "\")")
AppiumBy.ANDROID_UIAUTOMATOR("new UiSelector().text(\"" + str(text_str) + "\")")
els[0].click()
driver.tap([(543, 818)], 100)
print("pinch ...")
pinch()
print("zoom ...")
zoom()
# pic_el_list = driver.find_elements("com.android.gallery3d:id/gl_root_view")
print("wait 5 sec ...")
time.sleep(5)
print("quit ...")
driver.quit()
