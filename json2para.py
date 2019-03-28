#coding=utf-8
__author__ = 'DozingWolf'
from logger import NewLogger
import json
import os
import io
import time
from hashcheck import ParaHashcheck

file_path = './parameter/SHA1'
para_path = './parameter/parameter.json'

# rst = para_hashcheck(file_path, para_path)

class ParaLoder(object):
    def __init__(self,p_path,chk_result,*p_item):
        self.__checkResult = chk_result
        self.__parameterPath = p_path
        self.__PHlogpath = './log/'
        self.__logfilepath = 'JSON2PARA_LOG.log'
        self.__baselog = NewLogger(m_path=self.__PHlogpath, f_path=self.__logfilepath)
        self.__hashlog = self.__baselog.setting()
        self.__parameterIteam = p_item
        self.resultDict = {}

    def loadParameter(self):
        if self.__checkResult == 1:
            parameter_dict = open(file=self.__parameterPath,mode='r')
            para_dict = json.loads(parameter_dict.read())
            for key,iteam in enumerate(self.__parameterIteam):
                self.__hashlog.info('load parameter iteam %s'%iteam)
                self.resultDict.update({iteam:para_dict[iteam]})

            # self.resultDict.update(DB_readonly=para_dict['DB_readonly'])
            # self.resultDict.update(DB_wrightonly=para_dict['DB_wrightonly'])
            # self.resultDict.update(MQ=para_dict['MQ'])
            # self.resultDict.update(Wechat_interface=para_dict['Wechat_interface'])
            # self.resultDict.update(BerkeleyDB=para_dict['BerkeleyDB'])
            self.resultDict.update(result=1)
            self.__hashlog.info('Hash check was success!')
            return self.resultDict
        else:
            self.resultDict.update(result=0)
            self.__hashlog.info('parameter check was failed, please check parameter file :%s')
            return self.resultDict

# def load_para(p_path, chk_result):
#     result_dict = {}
#     if chk_result == 1:
#         parameter_dict = open(file=p_path,mode='r')
#         para_dict = json.loads(parameter_dict.read())
#         result_dict.update(DB_readonly=para_dict['DB_readonly'])
#         result_dict.update(DB_wrightonly=para_dict['DB_wrightonly'])
#         result_dict.update(MQ=para_dict['MQ'])
#         result_dict.update(Wechat_interface=para_dict['Wechat_interface'])
#         result_dict.update(BerkeleyDB=para_dict['BerkeleyDB'])
#         result_dict.update(result=1)
#         return result_dict
#     else:
#         result_dict.update(result=0)
#         print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),' parameter check was failed, please check parameter file :',para_path)
#         return result_dict

# result = load_para(para_path, rst)
# print(result)
# print(result)# ['DB_readonly']['ip']
# 20190325
# parameterloder = PrarLoder('./parameter/parameter.json',1,'DB_readonly','MQ')
# iteam = parameterloder.loadParameter()
# print('iteam is :',iteam)
