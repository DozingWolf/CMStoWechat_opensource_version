#coding=utf-8
__author__ = 'DozingWolf'
import json
import logging
import logging.config
import time
from logging.handlers import TimedRotatingFileHandler
import sys,os


class NewLogger(object):

    def __init__(self,m_path,f_path):
        self.__format = '%(asctime)s : %(levelname)s - %(message)s'
        if os.path.exists(path=m_path)  == False:
            os.makedirs(name=m_path,mode=0o777,exist_ok=True)
        self.__mainpath = m_path+f_path
        self.__filepath = f_path

    def setting(self):  #''',filename'''
        print('logpath =',self.__mainpath )
        logger = logging.getLogger()  #'''name=filename'''
        logger.setLevel(logging.INFO)
        logformat = logging.Formatter(self.__format)

        handle_file = TimedRotatingFileHandler(filename=self.__mainpath,when='D',interval=1)
        handle_file.setFormatter(logformat)
        handle_file.setLevel(logging.INFO)

        handle_console = logging.StreamHandler(sys.stdout)
        handle_console.setFormatter(logformat)
        handle_console.setLevel(logging.INFO)

        logger.addHandler(handle_file)
        logger.addHandler(handle_console)

        return logger


# demo
# mainpath = './log/'
# filepath = 'READER_TEST_LOG.log'
# baselog = NewLogger(m_path=mainpath, f_path=filepath)
# newlog = baselog.setting()
# newlog.info('this is a info create by %s'%filepath)
# newlog.error('this is a error create by %s'%mainpath)
