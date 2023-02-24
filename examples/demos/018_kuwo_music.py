# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/11/16 11:52
@File : 018_kuwo_music.py
@Desc : 
"""
import asyncio
from urllib.parse import quote
import aiohttp
import logging
import aiofiles

referer = 'https://www.kuwo.cn'
# 请求头
headers = {
    "Cookie": "_ga=GA1.2.2021007609.1602479334; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1602479334,1602673632; "
              "_gid=GA1.2.168402150.1602673633; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1602673824; "
              "kw_token=5LER5W4ZD1C",
    "csrf": "5LER5W4ZD1C",
    "Referer": "{}".format(referer),
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/86.0.4240.75 Safari/537.36",
}

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


async def searchSong(session, song_name):
    encodeName = quote(song_name)
    url = f'https://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={encodeName}&pn=1&rn=30&httpsStatus=1'
    res = await session.get(url=url, headers=headers)
    return await res.json()


async def downloadSong(session, rid, name, singer):
    url = f'http://www.kuwo.cn/api/v1/www/music/playUrl?mid={rid}&type=convert_url3&br=320kmp3'
    res = await session.get(url=url, headers=headers)
    res_json = await res.json()
    download_url = res_json['data']['url']
    response = await session.get(download_url, headers=headers)
    data = await response.content.read()
    async with aiofiles.open(f'music/{name}-{singer}.mp3', mode='wb') as f:
        logging.info(f"{name}-{singer}.mp3下载完成")
        await f.write(data)


async def main(song_name):
    async with aiohttp.ClientSession() as session:
        song_json = await searchSong(session, song_name)
        songs_info = song_json['data']['list']
        tasks = []
        for song_info in songs_info:
            name = song_info['name'].replace(' ', '').replace('へ-', '').replace('|', '')
            artist = song_info['artist']
            rid = song_info['rid']
            logging.info(f"歌曲名称:{name}|歌手:{artist}|id:{rid}")
            tasks.append(asyncio.create_task(downloadSong(session, rid, name, artist)))
        await asyncio.wait(tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main("满天星辰不及你"))
