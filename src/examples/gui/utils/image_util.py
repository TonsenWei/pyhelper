import os
import time
import cv2
import numpy as np
from matplotlib import pyplot as plt

from utils.log_util import LogUtil

project_path = os.path.dirname(os.path.abspath(__file__))

class ImageUtil(object):
    
    # @staticmethod
    def match_image(self, value=0.95, screenshot_image="", imgs=[]):
        """图片对比
        Args:
            value (float, optional): [对比度]. Defaults to 0.95.
            screenshot_image (str, optional): [截图图片路径]. Defaults to "".
            imgs (list, optional): [图片路径数组，只要有一张存在就退出判断]. Defaults to [].

        Returns:
            [type]: [bool] 图片存在返回True否则返回False
        """
        start_time = time.time()
        exists = False
        for img in imgs:
            LogUtil().LOGGER.info("img_target = " + img)
            tpl_screenshot = cv2.imread(screenshot_image)
            tpl_img = cv2.imread(img)
            # 获取图标大小
            th_screenshot, tw_screenshot = tpl_screenshot.shape[:2]
            # 匹配函数
            result_match = cv2.matchTemplate(tpl_img, tpl_screenshot, cv2.TM_CCOEFF_NORMED)
            min_value, max_value, min_loc_value, max_loc_value = cv2.minMaxLoc(result_match)
            tl_rightlower = max_loc_value  # 是矩形右下角的点的坐标
            LogUtil().LOGGER.info("result = " + str(max_value))
            # cv.rectangle(tpl_target, tl, (tl[0] + tw, tl[1] + th), (7, 249, 151), 2)
            point_center = [int(tl_rightlower[0] + tw_screenshot / 2), int(tl_rightlower[1] + th_screenshot / 2)]
            if max_value >= value:
                LogUtil().LOGGER.info("center_point = " + str(point_center))
                LogUtil().LOGGER.info("target_exists,pass")
                exists = True
                break
        LogUtil().LOGGER.info("exists = " + str(exists))
        total_time = time.time() - start_time
        LogUtil().LOGGER.info("matchImage cost time = " + str(total_time))
        return exists
   
    def match_image_flann(self, tmplate_image, target_image):
        exists = False
        start_time = time.time()
        MIN_MATCH_COUNT = 10 #设置最低特征点匹配数量为10
        template = cv2.imread(tmplate_image,0) # queryImage
        target = cv2.imread(target_image,0) # trainImage
        # Initiate SIFT detector创建sift检测器
        sift = cv2.xfeatures2d.SIFT_create()
        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(template,None)
        kp2, des2 = sift.detectAndCompute(target,None)
        #创建设置FLANN匹配
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks = 50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1,des2,k=2)
        # store all the good matches as per Lowe's ratio test.
        good = []
        #舍弃大于0.7的匹配
        for m,n in matches:
            if m.distance < 0.7*n.distance:
                good.append(m)
        LogUtil().LOGGER.info("len(good) = " + str(len(good)))
        if len(good)>MIN_MATCH_COUNT:
            # 获取关键点的坐标
            src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
            dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
            LogUtil().LOGGER.info("src_pts = " + str(len(src_pts)))
            LogUtil().LOGGER.info("dst_pts = " + str(len(dst_pts)))
            LogUtil().LOGGER.info("dst_pts = " + str(dst_pts))
            # 计算变换矩阵和MASK
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            matchesMask = mask.ravel().tolist()
            h,w = template.shape
            # 使用得到的变换矩阵对原图像的四个角进行变换，获得在目标图像上对应的坐标
            pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
            dst = cv2.perspectiveTransform(pts,M)
            cv2.polylines(target,[np.int32(dst)],True,0,2, cv2.LINE_AA)
            LogUtil().LOGGER.info("found!")
            exists = True
            # print(good)
        else:
            print( "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
            matchesMask = None
        total_cost_time = time.time() - start_time
        LogUtil().LOGGER.info("cost time = " + str(total_cost_time))
        
    # 使用matplotlib这个库通过GUI显示出图片
        draw_params = dict(matchColor=(0,255,0), 
                    singlePointColor=None,
                    matchesMask=matchesMask, 
                    flags=2)
        result = cv2.drawMatches(template,kp1,target,kp2,good,None,**draw_params)
        plt.imshow(result, 'gray')
        plt.show()
        return exists
    
    # @staticmethod
    def wait_image_exists(self, value=0.95, screenshot_image="", imgs=[], timeout=3):
        start_time = time.time()
        imgs_exists = False
        time_counter = 0
        while imgs_exists == False and time_counter < timeout:
            imgs_exists = self.match_image(value, screenshot_image,imgs)
            time_counter = time.time() - start_time

if __name__ == "__main__":
    ImageUtil().wait_image_exists(screenshot_image=r"mi6_home.jpg", imgs=["mi6_settings_icon.jpg"])
