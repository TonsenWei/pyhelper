import base64
import json

import cv2
import numpy as np


def extend_list():
    list_str = ["a", "b", "c", "d"]
    list_b = ["1", "2", "3"]
    print(list_str)
    list_str.extend(list_b)
    print(list_str)

def insert_list():
    list_str = ["a", "b", "c", "d"]
    list_b = ["1", "2", "3"]
    print(list_str)
    list_str.insert(0, list_b)
    print(list_str)

def frame2base64(frame):
    image = cv2.imencode('.png', frame)[1]
    print(type(base64.b64encode(image)))
    image_code = str(base64.b64encode(image))[2:-1]
    return image_code

def base64ToImage(base64_code):
    # base64解码
    img_data = base64.b64decode(base64_code)
    # 转换为np数组
    # img_array = np.fromstring(img_data, np.uint8)  # is deprecated
    img_array = np.frombuffer(img_data, np.uint8)
    # 转换成opencv可用格式
    img = cv2.imdecode(img_array, cv2.COLOR_RGB2BGR)
    return img

def removeListTest():
    listData = [0, 1, 2, 3, 4, 5]
    print(f"before remove： {listData}")
    for i in range(2):
        listData.remove(i)
        print(f"index={i}, listData={listData}")
    print(f"after remove: {listData}")


def jsonTest():
    # param2 = "[{'占空比':0.8,'偏移量':0.1},{'频率':0.8,'偏移量':0.1}]"
    param2 = '{"占空比":{"值":0.8, "偏移量":0.1}, "频率":{"值":0.9,"偏移量":0.1}}'
    param2Obj = json.loads(param2)
    print(param2Obj)
    print(param2Obj["占空比"])
    print(param2Obj["频率"])

def evalTest():
    ret = eval(r"['D:\\projects\\python\\pyside2_prjs\\std_autotest\\output\\report\\2023-02-10_11-43-25\\images\\2023-02-10_11-43-29_469.png', 'D:\\projects\\python\\pyside2_prjs\\std_autotest\\output\\report\\2023-02-10_11-43-25\\images\\2023-02-10_11-43-29_701_2023-02-10_11-32-51_976.png']")
    print(ret[0])
    print(ret[1])

    dic = f'{{"key":"value", "test":"valuetest"}}'
    res = eval(dic)
    print(res["key"])
    print(res["test"])

def switchParamTest():
    a = "test"
    b = a
    a = "jojo"
    print(a)
    print(b)


import glob


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y


def GetCross(p1, p2, p):
    return (p2.x - p1.x) * (p.y - p1.y) - (p.x - p1.x) * (p2.y - p1.y)


def IsPointInMatrix(p1, p2, p3, p4, p):
    isPointIn = GetCross(p1, p2, p) * GetCross(p3, p4, p) >= 0 and GetCross(p2, p3, p) * GetCross(p4, p1, p) >= 0
    return isPointIn


if __name__ == '__main__':
    p1 = Point(1, 1)
    p2 = Point(3, 1)
    p3 = Point(4, 4)
    p4 = Point(1, 3)

    pp = Point(2, 2)
    pp2 = Point(4, 2)

    # print(IsPointInMatrix(p1, p2, p3, p4, pp))
    # print(IsPointInMatrix(p1, p2, p3, p4, pp2))
    print(IsPointInMatrix(p1, p2, p3, p4, Point(2, 1)))
    print(IsPointInMatrix(p1, p2, p3, p4, Point(2, 0)))
    # print(IsPointInMatrix(Point(396, 74), Point(407, 74), Point(396, 404), Point(410, 404), Point(405, 74)))
    print(IsPointInMatrix(Point(375, 77), Point(407, 76), Point(391, 440), Point(425, 441), Point(390, 54)))
    print(IsPointInMatrix(Point(375, 77), Point(407, 76), Point(391, 440), Point(425, 441), Point(389, 63)))


#
# if __name__ == "__main__":
#     # insert_list()
#     # png_path = r"C:\Users\tonse\Pictures\机器人图.png"
#     # png64Str = frame2base64(cv2.imdecode(np.fromfile(png_path, dtype=np.uint8), cv2.IMREAD_COLOR))
#     # cvimg = base64ToImage(png64Str)
#     # cv2.imshow('real_img', cvimg)
#     # cv2.waitKey()
#     # removeListTest()
#     # jsonTest()
#     # evalTest()
#     line = "test_code_run"
#     print(line.split("test_"))
#     pts = np.array([[100, 100], [200, 20], [370, 6], [450, 200]], np.int32)
#     dst0 = cv2.pointPolygonTest([pts], 0, 1)
