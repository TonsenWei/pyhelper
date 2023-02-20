# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @Administrator
@Time : 2022/10/4 2:47
@File : 014_music_dll.py
@Desc :
下载付费内容失败
{'code': -1, 'msg': '该歌曲为付费内容，请下载酷我音乐客户端后付费收听', 'reqId': 'bfcb99fc7161965989a3dcd612668d50', 'profileId': 'site', 'curTime': 1664823022494, 'success': False}
"""
import requests, json
import prettytable as pt

name = input("输入歌手名字：")

headers = {
    'Cookie': 'Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1658299714; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1658299751; kw_token=TZQO49M946',
    'csrf': 'TZQO49M946',
    'Host': 'kuwo.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://kuwo.cn/search/list?key=%E6%9D%8E%E8%8D%A3%E6%B5%A9'
}
url = f"https://kuwo.cn/api/www/search/searchMusicBykeyWord?key={name}&pn=1&rn=30&httpsStatus=1&reqId=375dc750-07f8-11ed-ad5e-cfc18da03713"

req = requests.get(url, headers=headers).json()

table = pt.PrettyTable()
table.field_names = ["序号", "歌手", "歌名", "专辑"]

data_lists = req['data']['list']
count = 0
down_list = []
for data_list in data_lists:
    artist = data_list['artist']  # 歌手名字
    name = data_list['name']  # 歌名
    album = data_list['album']  # 歌曲专辑
    rid = data_list['rid']  # 歌曲id
    table.add_row([count, name, artist, album])
    down_list.append([rid, name, artist])
    count += 1
print(table)

while True:
    music_num = eval(input("请输入需要下载的歌曲序号(-1退出)："))
    if music_num == -1:
        break
    down_info = down_list[music_num]
    rid = down_info[0]
    music_href = f"https://kuwo.cn/api/v1/www/music/playUrl?mid={rid}&type=music&httpsStatus=1&reqId=066ef2b0-0800-11ed-a672-cbc2b530b095"
    print(requests.get(music_href).json())  #{'code': -1, 'msg': '该歌曲为付费内容，请下载酷我音乐客户端后付费收听', 'reqId': 'bfcb99fc7161965989a3dcd612668d50', 'profileId': 'site', 'curTime': 1664823022494, 'success': False}
    music_json = requests.get(music_href).json()['data']['url']
    music_data = requests.get(music_json).content
    with open(f'酷我/{down_info[1]}-{down_info[2]}.mp3', mode="wb") as f:
        f.write(music_data)
    print(f"已完成：{down_info[1]}-{down_info[2]}")
