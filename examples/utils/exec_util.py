# -*- coding: utf-8 -*-
import subprocess
import sys
import os
import time

sys.path.insert(0, '../')
from src.utils.log_util import LogUtil
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class ExecUtil():
    
    @staticmethod
    def exec_cmd(cmd, delay=0):
        '''
        test pass 2021-11-13
        '''
        LogUtil().LOGGER.info(cmd)
        obj = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            line = obj.stdout.readline().decode("utf-8", "replace")
            if not line:
                break
            LogUtil().LOGGER.info(line.replace("\n","").replace("\t",""))
        excute_cmd_result = obj.wait()
        time.sleep(delay)
        if excute_cmd_result != 0:
            LogUtil().LOGGER.error("excute_cmd_result = " + str(excute_cmd_result))
        else:
            LogUtil().LOGGER.debug("excute_cmd_result = " + str(excute_cmd_result))

    @staticmethod
    def exec_cmd_in_dir(cmd, cwd_dir="./", delay=0):
        '''
        test pass 2021-11-13
        '''
        LogUtil().LOGGER.info(cmd)
        obj = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd_dir)
        while True:
            line = obj.stdout.readline().decode("utf-8", "replace")
            if not line:
                break
            LogUtil().LOGGER.info(line.replace("\n","").replace("\t",""))
        excute_cmd_result = obj.wait()
        time.sleep(delay)
        if excute_cmd_result != 0:
            LogUtil().LOGGER.error("excute_cmd_result = " + str(excute_cmd_result))
        else:
            LogUtil().LOGGER.debug("excute_cmd_result = " + str(excute_cmd_result))


    @staticmethod
    def excute_cmd(cmd):
        LogUtil().LOGGER.info(cmd)
        obj = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while obj.poll() is None:
            # line = obj.stdout.readline().decode("utf-8", "replace").strip()
            # line = obj.stdout.readline().decode("utf-8", "replace")
            line = obj.stdout.readline().decode("utf-8", "replace")
            if line.strip() is not "":
                LogUtil().LOGGER.info(line.strip())
        excute_cmd_result = obj.wait()
        LogUtil().LOGGER.debug("excute_cmd_result = " + str(excute_cmd_result))

    
    @staticmethod
    def excute_cmd_in_dir(cmd, cwd_dir = "./"):
        LogUtil().LOGGER.info(cmd + ", dir: " + cwd_dir)
        obj = subprocess.Popen(cmd, \
            shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd_dir)
        while obj.poll() is None:
            # line = obj.stdout.readline().decode("utf-8", "replace").strip()
            line = obj.stdout.readline().decode("utf-8", "replace")
            if line.strip() is not "":
                LogUtil().LOGGER.info(line.strip())
        excute_cmd_result = obj.wait()
        LogUtil().LOGGER.debug("excute_cmd_in_dir = " + str(excute_cmd_result))

if __name__ == "__main__":
    ExecUtil.excute_cmd("dir")
    ExecUtil().exec_cmd("ls -l /work")