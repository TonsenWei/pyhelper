# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/2/17 14:44
@File : 041_point_in_rect.py
@Desc : 
"""


# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date : 2018-10-07 15:49:37
# @Author : Sheldon (thisisscret@qq.com)
# @Blog : 谢耳朵的派森笔记
# @Link : https://www.cnblogs.com/shld/
# @Version : 0.0.1

def isinpolygon(point, vertex_lst: list, contain_boundary=True):
    # 检测点是否位于区域外接矩形内
    lngaxis, lataxis = zip(*vertex_lst)
    minlng, maxlng = min(lngaxis), max(lngaxis)
    minlat, maxlat = min(lataxis), max(lataxis)
    lng, lat = point
    if contain_boundary:
        isin = (minlng <= lng <= maxlng) & (minlat <= lat <= maxlat)
    else:
        isin = (minlng < lng < maxlng) & (minlat < lat < maxlat)
    return isin


def isintersect(poi, spoi, epoi):
    # 输入：判断点，边起点，边终点，都是[lng,lat]格式数组
    # 射线为向东的纬线
    # 可能存在的bug，当区域横跨本初子午线或180度经线的时候可能有问题
    lng, lat = poi
    slng, slat = spoi
    elng, elat = epoi
    if poi == spoi:
        # print("在顶点上")
        return None
    if slat == elat:  # 排除与射线平行、重合，线段首尾端点重合的情况
        return False
    if slat > lat and elat > lat:  # 线段在射线上边
        return False
    if slat < lat and elat < lat:  # 线段在射线下边
        return False
    if slat == lat and elat > lat:  # 交点为下端点，对应spoint
        return False
    if elat == lat and slat > lat:  # 交点为下端点，对应epoint
        return False
    if slng < lng and elat < lat:  # 线段在射线左边
        return False
    # 求交点
    xseg = elng - (elng - slng) * (elat - lat) / (elat - slat)
    if xseg == lng:
        # print("点在多边形的边上")
        return None
    if xseg < lng:  # 交点在射线起点的左侧
        return False
    return True  # 排除上述情况之后


def isin_multipolygon(poi, vertex_lst, contain_boundary=True):
    # 判断是否在外包矩形内，如果不在，直接返回false
    if not isinpolygon(poi, vertex_lst, contain_boundary):
        return False
    sinsc = 0
    for spoi, epoi in zip(vertex_lst[:-1], vertex_lst[1::]):
        intersect = isintersect(poi, spoi, epoi)
        if intersect is None:
            return (False, True)[contain_boundary]
        elif intersect:
            sinsc += 1
    return sinsc % 2 == 1


if __name__ == '__main__':
    # 最大值的角度 = 46, 圆心(406, 409), 线的点(631.6250387250823, 642.6415671499939), disMax = 1.3825269801818114
    vertex_lst = [[406, 409], [631, 642], [407, 410], [632, 643]]
    # vertex_lst = [[375, 77], [407, 76], [391, 440]]
    # poi = [390, 54]
    # poi = [394, 90]
    # poi = [375, 441]
    poi = [547, 557]
    # print(IsPointInMatrix(Point(375, 77), Point(407, 76), Point(391, 440), Point(425, 441), Point(390, 54)))
    print(isin_multipolygon(poi, vertex_lst, contain_boundary=True))
