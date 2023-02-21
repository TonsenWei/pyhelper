# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/2/7 18:03
@File : meter_detet_main.py
@Desc : 
"""
from examples.demos.meter_read.meter_detect.meter_detect_util.meter_util import MeterUtil
from examples.demos.meter_read.meter_detect.meter_detect_util.template_bean import TemplateBean


class MeterBean:

    def __init__(self):
        self.id = "2"
        self.name = "002_meter.png"
        self.img_template = r"002_meter.png"

        self.value = {0.0: (85.0, 233.0),
                      20.0: (77.0, 193.0),
                      40.0: (71.0, 163.0),
                      60.0: (74.0, 127.0),
                      80.0: (90.0, 102.0),
                      100.0: (119.0, 74.0),
                      120.0: (153.0, 59.0),
                      140.0: (192.0, 60.0),
                      160.0: (225.0, 75.0),
                      180.0: (250.0, 99.0),
                      200.0: (270.0, 134.0),
                      220.0: (277.0, 167.0),
                      240.0: (268.0, 204.0),
                      260.0: (248.0, 230.0),
                      }
        self.a = "{0.0:(91.0,417.0),13.0:(58.0,298.0),25.0:(90.0,179.0),38.0:(179.0,91.0),50.0:(298.0,59.0),63.0:(418.0,93.0),75.0:(505.0,180.0),88.0:(537.0,298.0),100.0:(507.0,418.0)}"
        self.c_x = "171.00"  # 圆心(x,y)像素坐标
        self.c_y = "165.00"
        self.maxd = "260.00"  # 最大刻度值
        self.scale = "20.00"  # 刻度间隔
        self.fir_d = "240.00"  # 骤然变化最小点
        self.sec_d = "260.00"  # 骤然变化最大点


if __name__ == "__main__":
    pass
    # testPicPath = r"D:\projects\gits\yibiao_rec\django_yibiao\yibiao_ocr\img_test_2\1.jpg"
    # testPicPath = r"D:\projects\gits\yibiao_rec\django_yibiao\yibiao_ocr\img_test_2\(3).jpg"
    testPicPath = r"real.jpg"  # resultValue=59.84098902001376
    # testPicPath = r"D:\tmp\v3_test.png"
    # testPicPath = r"D:\tmp\v3_rpm.png"
    # templatePicPath = r"D:\projects\gits\yibiao_rec\django_yibiao\yibiao_ocr\TemplateLib\template.jpg"
    templatePicPath = r"002_meter.png"  # resultValue=59.84098902001376
    # templatePicPath = r"D:\tmp\v3_rpm_meter.png"
    # tempInfo = TemplateBean()
    tempInfo = MeterBean()
    for k, v in tempInfo.value.items():
        print(f"k={k}, v={v}")
    # resultValue = MeterUtil.img_rec_result(testPicPath, templatePicPath, tempInfo)
    # print(f"resultValue={resultValue}")  # resultValue=0.4534627915069202
