# -*- coding: utf-8 -*-
import time
import datetime

class TimeUtil():
    '''
    get current system time,with millsecond
    获取系统当前时间，精确到毫秒
    '''
    @staticmethod
    def get_now_time_mill():
        """
        get current system time
        获取系统当前时间，精确到毫秒
        :return: current time, format: 2019-11-25_16-59-16.777
        """
        ct = time.time()  # current time，float
        local_time = time.localtime(ct)  # traslate to local time
        data_head = time.strftime("%Y-%m-%d_%H-%M-%S", local_time)
        data_secs = (ct - int(ct)) * 1000
        time_stamp = "%s.%03d" % (data_head, data_secs)
        return time_stamp
    '''
    get current system time,with second
    获取系统当前时间，精确到秒
    :return: 2021-11-16_15-47-30
    '''
    @staticmethod
    def get_now_time_second():
        """
        get current system time
        获取系统当前时间，精确到秒
        :return: current time, format: 2019-11-25_16-59-16
        """
        ct = time.time()  # current time，float
        local_time = time.localtime(ct)  # traslate to local time
        data_head = time.strftime("%Y-%m-%d_%H-%M-%S", local_time)
        # data_secs = (ct - int(ct)) * 1000
        # time_stamp = "%s.%03d" % (data_head, data_secs)
        # return time_stamp
        return data_head
    
    @staticmethod
    def log_with_time(message):
        '''
        打印时间戳
        '''
        print(TimeUtil.get_now_time_mill() + "> "
              + str(message).replace("\r\n", "\r\n"
              + TimeUtil.get_now_time_mill() + "> "))  # if want to not \n, use end param

    @staticmethod
    def caculate_time_millisecond(time_str_start="", time_str_end=""):
        '''
        get milliseconds between two time
        获取两个时间的时间间隔
        make sure start time and end time is in 24 hours, and end time > start time
        '''
        start_time = datetime.datetime.strptime(time_str_start, "%m-%d %H:%M:%S:%f")
        end_time = datetime.datetime.strptime(time_str_end, "%m-%d %H:%M:%S:%f")
        month = end_time.month - start_time.month
        day = end_time.day - start_time.day
        hour = end_time.hour - start_time.hour
        minute = end_time.minute - start_time.minute
        second = end_time.second - start_time.second
        microsecond = end_time.microsecond - start_time.microsecond
        millisecond = int(microsecond/1000);
        last_microsecond = microsecond%1000;
        # print("cost time = " + str(month) + " months, " + str(day) + " days," + \
        #     str(hour) + " hours, " + str(minute) + " minutes, " + str(second) + " seconds, " + \
        #     str(millisecond) + " milliseconds, " + str(last_microsecond) + " microseconds")
        total_millisecond = day*24*60*1000 + hour**60*1000 + second*1000 + microsecond/1000
        # print("total_millisecond = " + str(total_millisecond))
        return total_millisecond

if __name__ == "__main__":
    TimeUtil.log_with_time("test")
    TimeUtil.caculate_time_millisecond("09-28 06:35:20:050930", "09-28 06:35:20:051152")
