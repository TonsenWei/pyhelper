"""
Author: Wei Dongcheng
Date: 2022-03-20 15:57:38
LastEditTime: 2022-03-20 16:07:39
LastEditors: Wei Dongcheng
Description:
"""
import logging
import colorlog
import sys
import os

project_path = os.path.dirname(os.path.realpath(sys.argv[0]))

log_colors_config = {
    'DEBUG': 'white',  # cyan white
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}


class LogUtil(object):
    """
    日志工具类
    """
    LOGGER = None

    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            cls.LOGGER = logging.getLogger(__name__)
            cls.LOGGER.setLevel(level=logging.DEBUG)

            file_handler = logging.FileHandler(filename=project_path + "\\output.txt", mode="w", encoding="utf8")
            file_handler.setLevel(logging.INFO)
            # log output formatter
            file_formatter = logging.Formatter(
                fmt='[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
                datefmt='%Y-%m-%d  %H:%M:%S'
            )
            console_formatter = colorlog.ColoredFormatter(
                fmt='%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
                datefmt='%Y-%m-%d  %H:%M:%S',
                log_colors=log_colors_config
            )
            file_handler.setFormatter(file_formatter)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(console_formatter)
            console_handler.setLevel(logging.DEBUG)
            # repeat log issue：
            # 1、avoid addHandler multi times；
            # 2、loggername ensure not the same；
            # 3、after show log, call removeHandler
            if not cls.LOGGER.handlers:
                cls.LOGGER.addHandler(console_handler)
                cls.LOGGER.addHandler(file_handler)

            console_handler.close()
            file_handler.close()

            orig = super(LogUtil, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
            cls._instance.LOGGER = cls.LOGGER
        return cls._instance


logger = LogUtil().LOGGER
