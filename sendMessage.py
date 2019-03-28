#coding=utf-8
__author__ = 'DozingWolf'
'''
getMQ==>send2WechatInterface
'''
from getToken import TokenOperator
from BerkeleyDB import BerkeleyDB
from makeDataModel import DataReplace
from makeDataModel import dataModel
from part_consumer.basic_consumer_mq_option import *
from json2para import ParaLoder
from hashcheck import ParaHashcheck
from logger import NewLogger
import requests
import json
import pika
import _pickle as cPickle
import time
import re

class SendMessagetoWechat(object):
    def __init__(self):
        # initial
        self.__paraSHA1Path = './parameter/SHA1'
        self.__filePath = './parameter/SHA1'
        self.__paraFilePath = './parameter/parameter.json'
        self.__smwLogpath = './log/'
        self.__smwLogFilePath = 'SMW_LOG.log'
        # check
        self.__newParaChecker = ParaHashcheck(f_path=self.__paraSHA1Path, p_path=self.__paraFilePath)
        self.__checkResulfFlag = self.__newParaChecker.checkparameter()
        # parameter
        self.__smwParaLoder = ParaLoder(self.__paraFilePath, self.__checkResulfFlag,'MQ', 'BerkeleyDB')
        self.__smwParameter = self.__smwParaLoder.loadParameter()
        # log handlers
        self.__baseSMWLogger = NewLogger(m_path=self.__smwLogpath, f_path=self.__smwLogFilePath)
        self.__smwLogger = self.__baseSMWLogger.setting()
        # create data dict
        self.__headers = {'Content-Type': 'application/json',}
        self.__service_url = 'http://www.umisu.com/api/wechat-v1/message/send'
        # initial datamodel
        self.__smwDataReplace = DataReplace()
        # bsddb
        self.__dbHandle = BerkeleyDB(b_path=self.__smwParameter['BerkeleyDB']['bdb_path'], b_file=self.__smwParameter['BerkeleyDB']['SMW_IN_FAIL'])
        # initial MQ parameter
        self.__mq_ip = self.__smwParameter['MQ']['ip']
        self.__mq_user = self.__smwParameter['MQ']['user']
        self.__mq_password = self.__smwParameter['MQ']['passwd']
        self.__mq_exchange = self.__smwParameter['MQ']['exchange']
        self.__mq_routing_key = self.__smwParameter['MQ']['routingkey']
        self.__mq_queue = self.__smwParameter['MQ']['queue']
    def SendMessage(self):
        # get token
        mainToken = TokenOperator()
        token_resp = mainToken.getToken()
        # connect to mq
        rtflag,connect,parameter = createMQengine(self.__mq_ip, self.__mq_user, self.__mq_password)
        self.__smwLogger.info('createChannel')
        channel = connect.channel()
        self.__smwLogger.info('declareQueue')
        queue_name = channel.queue_declare(queue=self.__mq_queue,durable=True)
        self.__smwLogger.info('bindQueue')
        channel.queue_bind(exchange=self.__mq_exchange, queue=self.__mq_queue, routing_key=self.__mq_routing_key)

        def cb(ch,method,properties,body):
            # 取出accesstoken值
            return_status = ''
            # access_token = token_resp['AccessToken'] #20190326
            access_token = token_resp
            self.__smwLogger.warning('access token : %s'%access_token)
            rcv_msg = json.loads(body)
            # check_rest = checkToken(token_resp) #20190326 去除
            fail_id = []
            succ_id = []
            for enu,rcv_list in enumerate(rcv_msg):
                broken_timer = 0
                # print(enu,rcv_list,'out')
                while broken_timer <=2:
                    # 每次计数，最多发送三次，失败计数
                    msg_body = dataModel(rcv_list[3], rcv_list[4])
                    params = (('access_token',token_resp),)
                    data = '{"msgtype":"text","agentid":1,"text":{"content":"%s"},"key":"SALPRC_FB_GRP"}'%(msg_body)
                    data = data.encode('utf-8').decode('latin1')
                    response = requests.post(self.__service_url, headers=self.__headers, params=params, data=data)
                    response_text = json.loads(response.text)

                    if response_text['errcode'] == 0:
                        # 确认发送完成后重置计数器
                        broken_timer = 999
                        return_status = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+' '+'success!'
                        self.__smwLogger.info('send message success!')
                        # print(return_status)
                        succ_id.append(rcv_list[0])
                    else:
                        # 发送失败后记录
                        broken_timer += 1
                        return_status = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+' '+'failed to send message ,please check interface return message:'+response_text['errmsg']
                        self.__smwLogger.warning('failed to send message ,please check interface return message: %s'%response_text['errmsg'])
                        if broken_timer == 2:
                            '''
                            记录没有发送成功的这个数据行id
                            '''
                            return_status = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+' '+'access token was failure 3 times ,system will be record failured event'
                            self.__smwLogger.warning('access token was failure 3 times ,system will be record failured event')
                            # print(return_status)
                            fail_id.append(rcv_list[0])
                            # 此处将发送失败的rcv_list[0]记入BerkeleyDB，用于返回信息
                        else:
                            return_status = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+' '+'something was wrong, system will try again'
                            self.__smwLogger.warning('something was wrong, system will try again')
                            # print(return_status)
                            access_token = mainToken.getToken(source='SERVER')

            ch.basic_ack(delivery_tag = method.delivery_tag)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(cb, queue=self.__mq_queue,no_ack=False) #
        print('please wait for message , to exit press ctrl+c')
        # start get data
        channel.start_consuming()

# file_path = './parameter/SHA1'
# para_path = './parameter/parameter.json'
# # load parameter
# para_rst = para_hashcheck(file_path, para_path)
# result = load_para(para_path, para_rst)
# if result['result'] == 0:
#     print('result is :',result['result'])
#     print('check result was failed, system will be finished')
#     exit()
# else:
#     print('result is :',result['result'])
# # initial logger
# mainpath = './log/'
# filepath = 'SENDMESSAGE_LOG.log'
# baselog = NewLogger(m_path=mainpath, f_path=filepath)
# sendlog = baselog.setting()
#
# # post parameter
# headers = {'Content-Type': 'application/json',}
# service_url = 'http://www.umisu.com/api/wechat-v1/message/send'
# # MQ parameter
# mq_ip = result['MQ']['ip']
# mq_user = result['MQ']['user']
# mq_password = result['MQ']['passwd']
# mq_exchange = result['MQ']['exchange']
# mq_routing_ket = result['MQ']['routingkey']
# mq_queue = result['MQ']['queue']
# # get mq data
#
# # 循环判断token的返回值，token有问题重新取token
# # 前端没有提供接口，所以这里写得比较纸张。。。。
# '''
# 同一批消息取token，如果三次获取失败，回置数据库状态为未发送，等待下次继续发送。
# 伪代码：
#     要在ch方法内实现以下内容
#     getmqdata()
#     var information[] = getmqdata.data
#     gettoken()
#     var calc = 0
#     var success_flag = -9
#     var get_token_response = gettoken.response
#     while calc < 3 and success_flag != 0:
#         if calc == 0:
#             gettoken
#         if token is useable:
#             for message in information:
#                 send information to wechat
#                 get return message
#                 check return message
#                 if send success:
#                     calc = 100
#                     success_flag = 0
#                 else:
#                     calc = calc+1
#                     success_flag = -1
#         else:
#             get a new token
#             calc = calc+1
#             success_flag = -1
#     if success_flag == 0:
#         write back database 'success flag'
#     else:
#         write back database 'failure flag'
# '''
# # get token
# mainToken = TokenOperator()
# token_resp = mainToken.getToken()
# # connect to mq
# rtflag,connect,parameter = createMQengine(mq_ip, mq_user, mq_password)
# sendlog.info('createChannel')
# channel = connect.channel()
# sendlog.info('declareQueue')
# queue_name = channel.queue_declare(queue=mq_queue,durable=True)
# sendlog.info('bindQueue')
# channel.queue_bind(exchange=mq_exchange, queue=mq_queue, routing_key=mq_routing_ket)
# # get mq data
# def cb(ch,method,properties,body):
#     # 取出accesstoken值
#     return_status = ''
#     # access_token = token_resp['AccessToken'] #20190326
#     access_token = token_resp
#     sendlog.warning('access token : %s'%access_token)
#     rcv_msg = json.loads(body)
#     # check_rest = checkToken(token_resp) #20190326 去除
#     fail_id = []
#     succ_id = []
#     for enu,rcv_list in enumerate(rcv_msg):
#         broken_timer = 0
#         # print(enu,rcv_list,'out')
#         while broken_timer <=2:
#             # 每次计数，最多发送三次，失败计数
#             msg_body = dataModel(rcv_list[3], rcv_list[4])
#             params = (('access_token',token_resp),)
#             data = '{"msgtype":"text","agentid":1,"text":{"content":"%s"},"key":"SALPRC_FB_GRP"}'%(msg_body)
#             data = data.encode('utf-8').decode('latin1')
#             response = requests.post(service_url, headers=headers, params=params, data=data)
#             response_text = json.loads(response.text)
#
#             if response_text['errcode'] == 0:
#                 # 确认发送完成后重置计数器
#                 broken_timer = 999
#                 return_status = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+' '+'success!'
#                 sendlog.info('send message success!')
#                 # print(return_status)
#                 succ_id.append(rcv_list[0])
#             else:
#                 # 发送失败后记录
#                 broken_timer += 1
#                 return_status = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+' '+'failed to send message ,please check interface return message:'+response_text['errmsg']
#                 sendlog.warning('failed to send message ,please check interface return message: %s'%response_text['errmsg'])
#                 if broken_timer == 2:
#                     '''
#                     记录没有发送成功的这个数据行id
#                     '''
#                     return_status = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+' '+'access token was failure 3 times ,system will be record failured event'
#                     sendlog.warning('access token was failure 3 times ,system will be record failured event')
#                     # print(return_status)
#                     fail_id.append(rcv_list[0])
#                     # 此处将发送失败的rcv_list[0]记入BerkeleyDB，用于返回信息
#                 else:
#                     return_status = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+' '+'something was wrong, system will try again'
#                     sendlog.warning('something was wrong, system will try again')
#                     # print(return_status)
#                     access_token = mainToken.getToken(source='SERVER')
#
#     ch.basic_ack(delivery_tag = method.delivery_tag)
#
# channel.basic_qos(prefetch_count=1)
# channel.basic_consume(cb, queue=mq_queue,no_ack=False) #
# print('please wait for message , to exit press ctrl+c')
# # start get data
# channel.start_consuming()
#
# '''
# 查了一下，好像需要使用mq的rpc调用方式进行，先写一个rpc调用的demo出来看一下
# '''

# check
# if check_rest[0] == 1:
#     token = token_resp['AccessToken']
#
# print('=============')
# msg_body = dataModel(row.BUSTYPE, row.MESSAGE)
# print(token_resp['AccessToken'])
# params = (('access_token',token_resp['AccessToken']),)
# print('=============')
# print(msg_body)
# data = '{"msgtype":"text","agentid":1,"text":{"content":"%s"},"key":"CMSSyetemErr"}'%(msg_body)
# print(data)
# data = data.encode('utf-8').decode('latin1')
# print(data)
# response = requests.post(service_url, headers=headers, params=params, data=data)
# print(response.text)
