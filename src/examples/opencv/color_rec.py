# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/11/2 15:48
@File : color_rec.py
@Desc : 
"""
import pandas as pd
import cv2


def get_color_name(r, g, b):
    min_diff = 10000
    color_name = ''
    for i in range(len(csv_df)):
        d = abs(r - int(csv_df.loc[i, "R"])) + abs(g - int(csv_df.loc[i, "G"])) + abs(b - int(csv_df.loc[i, "B"]))
        if d <= min_diff:
            min_diff = d
            color_name = csv_df.loc[i, "color_name"]
    return color_name


def click_info(event, x, y, flags, param):
    # 只处理双击事件
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        xpos = x
        ypos = y
        b, g, r = img[y, x]  # 获取b, g, r
        b = int(b)
        g = int(g)
        r = int(r)
        clicked = True


r = g = b = xpos = ypos = 0
clicked = False
img = cv2.imread('colorpic.jpg')
index = ["color", "color_name", "hex", "R", "G", "B"]
csv_df = pd.read_csv('colors.csv', names=index, header=None)

cv2.namedWindow('image')
cv2.setMouseCallback('image', click_info)

while True:
    cv2.imshow("image", img)
    if clicked:
        # 绘制显示文字的区域
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
        text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        # 显示文字内容
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # 如果像素点的颜色太偏向于白色,就用黑色来显示文字
        if (r + g + b >= 600):
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

    clicked = False
    # 点击 esc键
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
