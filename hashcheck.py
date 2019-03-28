#coding=utf-8
__author__ = 'DozingWolf'
import hashlib
import sys
import json
from logger import NewLogger

# baselog = newLog()
# baselog.setMyLogPath(f_path = 'HASHCHECK_LOG.log') #logpath='./log/SYS_LOG.log', filename='./log/Log.log'
# newlog = baselog.setting()

class ParaHashcheck(object):
    def __init__(self,f_path,p_path):
        self.__PHlogpath = './log/'
        self.__logfilepath = 'HASHCHECK_LOG.log'
        self.__baselog = NewLogger(m_path=self.__PHlogpath, f_path=self.__logfilepath)
        self.__hashlog = self.__baselog.setting()

        self.__hash_text = hashlib.sha1(open(file=p_path,mode='r').read().encode('utf-8')).hexdigest()
        self.__hashlog.info('calc\'s hash was: %s'%self.__hash_text)
        self.__file = open(file=f_path,mode='r')
        self.__sha1code = json.loads(self.__file.read())
        self.__hashlog.info('file\'s hash was: %s'%self.__sha1code['para_hashcode'])
    def checkparameter(self):
        if self.__sha1code['para_hashcode'] == self.__hash_text:
            self.__hashlog.info('Hash check was successful')
            return 1
        else:
            self.__hashlog.info('Hash check was failure!')
            return 0

# def para_hashcheck(f_path,p_path):
#
#     mainpath = './log/'
#     filepath = 'HASHCHECK_LOG.log'
#     baselog = NewLogger(m_path=mainpath, f_path=filepath)
#     hashlog = baselog.setting()
#
#     hash_text = hashlib.sha1(open(file=p_path,mode='r').read().encode('utf-8')).hexdigest()
#     hashlog.info('calc\'s hash was: %s'%hash_text)
#     file = open(file=f_path,mode='r')
#     sha1code = json.loads(file.read())
#     hashlog.info('file\'s hash was: %s'%sha1code['para_hashcode'])
#     if hash_text == sha1code['para_hashcode']:
#         # print('success!')
#         hashlog.info('Hash check was successful')
#         # newlog.info('Hash check success!')
#         return 1
#     else:
#         # print('hash check was failure!')
#         hashlog.warning('Hash check was failure!')
#         # newlog.error('Hash check was failed!')
#         return 0

#
file_path = './parameter/SHA1'
para_path = './parameter/parameter.json'
#
# rst = para_hashcheck(file_path, para_path)
newPareChecker = ParaHashcheck(f_path=file_path, p_path=para_path)
checkFlag = newPareChecker.checkparameter()
print(checkFlag)
