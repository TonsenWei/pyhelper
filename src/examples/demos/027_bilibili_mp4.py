# -*- coding: utf-8 -*-



import json

import os

import sys

import shutil

import datetime

import time




def get_info_list(src_dir):

    '''

    遍历目录，获取视频对应的.info文件，用于从里面提取视频的标题，专辑名字信息

    返回一个列表，列表中存储的是.info文件的绝对路径

    '''

    info_list = []

    for i,j,k in os.walk(src_dir):

        for file in k:

            if file.endswith('.info'):

                info_list.append(os.path.join(i,file))

    return info_list




def copy_mp4(list_info, to_dir):

    '''

    遍历info文件，读取文件中视频专辑名称和视频标题，

    把跟info文件同路径下的MP4文件改名复制到to_dir

    '''

    for info_path in list_info:

        album_str = ""

        title_str = ""

        with open(info_path, 'r', encoding='utf-8') as load_info_file:

            mv_info_json = json.load(load_info_file)

            print(mv_info_json)

            print("Title = " + mv_info_json["Title"])

            print("PartName = " + mv_info_json["PartName"])

            album_str = mv_info_json["Title"]

            title_str = mv_info_json["PartName"]

        if len(album_str)!=0 and len(title_str)!=0:

            album_dir = os.path.join(to_dir, album_str)

            if not os.path.exists(album_dir):

                os.mkdir(album_dir)

            info_dir = os.path.dirname(info_path)

            mp4_path = get_endstr_file(info_dir, ".mp4")

            new_mp4_path = os.path.join(album_dir, title_str + ".mp4")

            print("new_mp4_path = " + new_mp4_path)

            shutil.copy(mp4_path, new_mp4_path)

       



def get_endstr_file(dir_path, endstr):

    '''

    查找dir_path目录下后缀为endstr的文件，默认找到一个即返回，

    因为下载的视频每个文件夹只放一个MP4视频

    '''

    files = os.listdir(dir_path)

    for file in files:

        if os.path.isfile(os.path.join(dir_path, file)) and file.endswith(endstr):

            print("found: " + file)

            return os.path.join(dir_path, file)



def copy_mp4_by_date(root_dir, to_dir, year, month=None, day=None, hour=0, minute=0, second=0,

                microsecond=0):

    '''

    拷贝指定日期时间以后的MP4

    root_dir : 要扫描MP4的根目录，会在这个目录下查找所有文件夹，文件夹的创建时间比传入的日期新的话则拷贝里面的MP4

    to_dir : 拷贝MP4到哪个文件夹

    year,month,day,hour,minute,second,microsecond:日期时间传入

    '''

    t = datetime.datetime(year, month, day, hour, minute, second, microsecond)

    seconds = time.mktime(t.timetuple())



    root_dit_list = os.listdir(root_dir)

    for file in root_dit_list:

        dir_full_path = os.path.join(root_dir, file)

        if os.path.isdir(dir_full_path):

            t = os.path.getctime(dir_full_path)

            print("t = " + str(t))

            if seconds <= t:

                copy_mp4(get_info_list(dir_full_path), to_dir)



if __name__ == "__main__":

   

    copy_mp4_by_date(r"D:\Users\Downloads\Video\bilibili", r"D:\Users\Videos\mv",2022,12,12)
