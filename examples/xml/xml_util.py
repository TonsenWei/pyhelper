# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/10/17 18:05
@File : xml_util.py
@Desc : 
"""


def read_xml(filePath):
    from bs4 import BeautifulSoup  # 需要 pip install beautifulsoup4
    from lxml import etree  # 需要pip install lxml

    # 先从xml文件读取到内存
    content_str = ""
    with open(filePath, "r", encoding="utf8") as f:
        line = f.readline()
        content_str += line
        while line:
            line = f.readline()
            content_str += line
    xml_tree = BeautifulSoup(content_str, "lxml-xml")  # 字符串读取为bs4的xml对象
    datasource = xml_tree.findAll("datasource")
    source_0 = datasource[0].findAll("source")
    print(source_0[0])  # 找到<source name="speed_value" type="string" value="0"/>
    print(source_0[0]["name"] + " = " + source_0[0]["value"])  # 获取速度值，打印speed_value = 0


if __name__ == "__main__":
    print("start ...")
    read_xml(r"V3_master_bp.xml")
    print("end ...")
