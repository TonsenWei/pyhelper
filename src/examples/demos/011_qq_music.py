# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @Administrator
@Time : 2022/10/4 2:11
@File : 011_qq_music.py
@Desc : 
"""
import requests
import re
import os
import json
import time as t


class QQmusic():
    """代码仅供学习"""

    def __init__(self):
        """初始化"""
        self.headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'http://www.baidu.com/',
            'Connection': 'keep-alive',
        }
        self.names = []
        self.order = ' '

    def search(self):
        """搜索"""
        w = input("请输入歌曲名： ")
        url_0 = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=61460539676714578&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=10&w={0}&g_tk_new_20200303=5381&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0".format(
            w)
        res_0 = requests.get(url_0, headers=self.headers)  # 第一层，搜索页
        res_0.encoding = res_0.apparent_encoding
        print(res_0)
        res_0 = res_0.json()  # dict
        music_list = res_0["data"]["song"]["list"]
        print("共计" + str(len(music_list)) + "结果： ")

        all_singers = []
        a = 0
        for music in music_list:
            singer = music["singer"][0]["title"]  # 歌手名
            name = str(a) + "  " + music["title"]  # 歌曲名
            all_singers.append(singer)
            self.names.append(name)
            a = a + 1
        infs = dict(zip(self.names, all_singers))
        infs = json.dumps(infs, ensure_ascii=False, indent=4, separators=(',', ':'))
        infs = infs.replace('"', ' ')
        infs = infs.replace(':', '——————')
        print(infs)

        self.order = input("请输入歌曲前的序号：")
        songmid = res_0['data']['song']['list'][int(self.order)]['mid']
        url_1 = "https://u.y.qq.com/cgi-bin/musicu.fcg?format=json&data=%7B%22req_0%22%3A%7B%22module%22%3A%22vkey.GetVkeyServer%22%2C%22method%22%3A%22CgiGetVkey%22%2C%22param%22%3A%7B%22guid%22%3A%22358840384%22%2C%22songmid%22%3A%5B%22{}%22%5D%2C%22songtype%22%3A%5B0%5D%2C%22uin%22%3A%221443481947%22%2C%22loginflag%22%3A1%2C%22platform%22%3A%2220%22%7D%7D%2C%22comm%22%3A%7B%22uin%22%3A%2218585073516%22%2C%22format%22%3A%22json%22%2C%22ct%22%3A24%2C%22cv%22%3A0%7D%7D".format(songmid)

        res_1 = requests.get(url_1, headers=self.headers)
        res_1.encoding = res_1.apparent_encoding
        res_1 = res_1.json()  # dict
        purl = res_1['req_0']['data']['midurlinfo'][0]['purl']
        url_2 = "https://isure.stream.qqmusic.qq.com/" + purl
        return url_2

    def download(self):
        """下载"""
        res_2 = requests.get(self.search(), headers=self.headers).content
        fir = self.names[int(self.order)]
        tit = re.sub(r'\d+', '', fir)
        now = os.getcwd()
        now = os.path.join(now, "qq音乐 ")
        if not os.path.exists(now):
            os.mkdir(now)
        os.chdir(now)
        file_name = tit + '.m4a'
        with open(file_name, 'wb') as f:
            f.write(res_2)


one_file = QQmusic()
one_file.download()
