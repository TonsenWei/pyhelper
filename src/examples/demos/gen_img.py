from PIL import Image
import time
import os

def get_now_time_mill():
    '''
    获取当前时间
    '''
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d_%H_%M_%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s_%03d" % (data_head, data_secs)
    return time_stamp
    
if __name__ == '__main__':
    """使用pillow生成纯色图片
    当前为单线程，效率较低，想提高效率可以使用多线程或多进程同时生成，如10种颜色可用10个线程去分别生成
    """
    try: 
        # 颜色RGB值，10种颜色
        color_rgb = [(64, 116, 52), (159, 125, 80), (254, 67, 101),
                     (249, 205, 173), (131, 175, 155), (200, 200, 169),
                     (244, 208, 0), (229, 131, 8), (220, 87, 18),
                     (114, 83, 52)]
        
        print("start " + get_now_time_mill())
        for color_counter in range(10):
            print("color_counter = " + str(color_counter) + ", " + get_now_time_mill())
            # 新建图片，写入RGB值
            p = Image.new('RGBA', [1080,720], color_rgb[color_counter]) 
            # 为将图片组合成视频，每种颜色生成1800张图片,为组成视频，可以另外写脚本使用FFMPEG转换
            for pic_counter in range(1800):
                save_dir = "D:\PythonProject\PyExam\\" + str(color_counter)
                file_path = save_dir + "\Color_" + str(color_counter) + "_" + str(pic_counter) + ".png"
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                if not os.path.exists(file_path):
                    p.save(file_path)
        print("Done " + get_now_time_mill())
    except Exception as e: 
        print(e)
        pass