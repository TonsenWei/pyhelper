# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/11/1 9:22
@File : 001_image2video.py
@Desc : 
"""
import cv2

from src.myutils.file_util import FileUtil


def main():
    # filename：需要生成的视频的路径及文件名；
    # fourcc：用于压缩框架的解码器的4位编码（four
    # code
    # of
    # codec），在此查询可用的4位码（http: // www.fourcc.org / codecs.php）
    # fps：视频帧率
    # frameSize：视频分辨率
    # isColor：如果该位值为Ture，解码器会进行颜色框架的解码，否则会使用灰度进行颜色架构（该功能仅支持在Windows系统中使用）
    # data_path = "2017-06-13-29/images/"
    fps = 20  # 视频帧率
    size = (1920, 720)  # 需要转为视频的图片的尺寸
    # video = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps, size)
    video = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, size)

    pngs = FileUtil.get_files_path_list(
        r"D:\projects\python\pyside2_prjs\std_autotest\src\myutils\imgs",
        ".png")
    # for png in pngs:
    for i, png in enumerate(pngs, 1):
        print(f"i={i}, png={png}")
        # for i in range(1041):
        #     image_path = data_path + "%010d_color_labels.png" % (i + 1)
        # print(png)
        img = cv2.imread(png)
        print(type(img))  # <class 'numpy.ndarray'>
        # 如果没有这句，图片尺寸与设置的分辨率不一样输出的视频为0k
        frame = cv2.resize(img, size, interpolation=cv2.INTER_CUBIC)
        video.write(frame)

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
