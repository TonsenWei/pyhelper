# -*- coding: utf-8 -*-
import logging
import colorlog
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

log_colors_config = {
    'DEBUG': 'white',  # cyan white
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

class LogUtil(object):
    LOGGER = None
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            cls.LOGGER = logging.getLogger(__name__)
            cls.LOGGER.setLevel(level = logging.DEBUG)

            # mode = w, rewrite
            # mode = a, append
            file_handler = logging.FileHandler(filename="py_log.txt", mode="w", encoding="utf8")
            file_handler.setLevel(logging.INFO)
            # log output formatter
            file_formatter = logging.Formatter(
                fmt='[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
                datefmt='%Y-%m-%d  %H:%M:%S'
            )
            console_formatter = colorlog.ColoredFormatter(
                fmt='%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
                datefmt='%Y-%m-%d  %H:%M:%S',
                log_colors = log_colors_config
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
            # cls.LOGGER.addHandler(handler)
            # cls.LOGGER.addHandler(console)

            orig = super(LogUtil, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
            cls._instance.LOGGER = cls.LOGGER
        return cls._instance


if __name__ == "__main__":
    '''
    demo test of LogUtil
    '''
    log_util = LogUtil().LOGGER
    log_util.info("test log_util.py")

    test = LogUtil().LOGGER
    test.warning("gagjlsjglsgj")

    test1 = LogUtil().LOGGER
    test1.error("hah")

    test2 = LogUtil().LOGGER
    test2.critical("heihei")

    test3 = LogUtil().LOGGER
    test3.debug("lalala")