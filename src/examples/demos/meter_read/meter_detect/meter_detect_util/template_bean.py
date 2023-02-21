# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/2/7 18:08
@File : template_bean.py
@Desc : 
"""


class TemplateBean:

    def __init__(self):
        self.id = "1"
        self.name = "template.jpg"
        self.img_template = r"D:\projects\gits\yibiao_rec\django_yibiao\yibiao_ocr\TemplateLib\template.jpg"

        self.a = "{0.0:(91.0,417.0),13.0:(58.0,298.0),25.0:(90.0,179.0),38.0:(179.0,91.0),50.0:(298.0,59.0),63.0:(418.0,93.0),75.0:(505.0,180.0),88.0:(537.0,298.0),100.0:(507.0,418.0)}"
        self.c_x = "296.00"  # 圆心(x,y)像素坐标
        self.c_y = "298.50"
        self.maxd = "100.00"
        self.scale = "12.50"
        self.fir_d = "88.00"  # 骤然变化最小点
        self.sec_d = "100.00"  # 骤然变化最大点

        # self.a = "{0.0:(61.5,152.5),0.1:(50.5,109.5),0.2:(61.5,152.5),0.3:(126.0,46.0),0.4:(169.0,70.0),0.5:(188.5,122.0),0.6:(164.0,168.5)}"
        # self.c_x = "120.00"
        # self.c_y = "114.50"
        # self.fir_d = "0.50"
        # self.maxd = "0.60"
        # self.scale = "0.10"
        # self.sec_d = "0.60"

        # self.name = "template.jpg"
        # self.name = "v3_rpm_meter.jpg"
        # # self.img_template = r"D:\projects\gits\yibiao_rec\django_yibiao\yibiao_ocr\TemplateLib\template.jpg"
        # self.img_template = r"D:\tmp\v3_rpm_meter.png"
        # self.a = "{0.0:(61.5,152.5),0.1:(50.5,109.5),0.2:(61.5,152.5),0.3:(126.0,46.0),0.4:(169.0,70.0),0.5:(188.5,122.0),0.6:(164.0,168.5)}"
        # # self.a = "{0.0:(113.0,472.0),1.0:(62.0,345.0),2.0:(78.0,206.0),3.0:(164.0,98.0),4.0:(304.0,63.0),5.0:(441.0,99.0),6.0:(527.0,205.0),7.0:(546.0,344.0),8.0:(493.0,474.0)}"
        # self.c_x = "306.50"  # 圆心(x,y)像素坐标
        # self.c_y = "308.00"
        # self.fir_d = "7.00"  # 配置0刻度线参数1
        # self.maxd = "8.00"  # 最大刻度值
        # self.scale = "1.00"  # 刻度间隔
        # self.sec_d = "7.00"  # 配置0刻度线参数2
