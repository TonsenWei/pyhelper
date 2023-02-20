# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @Administrator
@Time : 2022/10/4 3:00
@File : 015_music_dl.py
@Desc :
可以下载，下载列表
"""
import requests
from lxml import etree

#网易云音乐的网址
url = "https://music.163.com/discover/toplist?id=3778678"
#下载歌曲的网址，可以用第三方工具获取
url_base = "http://music.163.com/song/media/outer/url?id="
#向网址发起请求
response = requests.get(url=url)
#将获取到的HTML代码进行数据解析
html = etree.HTML(response.text)
#获取id列表
id_list = html.xpath("//a[contains(@href,'song?')]")

counter = 0
for data in id_list:
    try:
        href = data.xpath("./@href")[0]
        music_id = href.split("=")[1]
        music_name = data.xpath("./text()")[0]
        counter += 1
        print(music_name)
    except Exception as e:
        print(e)
print(counter)

    #拼接下载地址
    # music_url = url_base + music_id
    #
    # music = requests.get(url=music_url)
    # with open("./music/%s.mp3" % music_name, "wb") as file:
    #     file.write(music.content)
    #     print("<%s>下载成功。。。" % music_name)
    #学习加喂：lbt13732741834