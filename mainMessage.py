#coding=utf-8
__author__ = 'DozingWolf'
from getData import *
from part_producer.basic_producer_mq_option import *
from json2para import ParaLoder
from hashcheck import ParaHashcheck
from logger import NewLogger
import requests
import json
import pika
import _pickle as cPickle
# import io
# import sys
#
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
'''
设计思路:
    所有连接参数调用getToken.py
    建立数据模板，供业务调用

'''

paraSHA1Path = './parameter/SHA1'
filePath = './parameter/SHA1'
paraFilePath = './parameter/parameter.json'
getDataLogpath = './log/'
getDataLogFilePath = 'GETDATA_LOG.log'
# check
newParaChecker = ParaHashcheck(f_path=paraSHA1Path, p_path=paraFilePath)
checkResulfFlag = newParaChecker.checkparameter()
# parameter
getDataParaLoder = ParaLoder(paraFilePath, checkResulfFlag,'MQ', 'DB_readonly', 'DB_wrightonly')
getDataParameter = getDataParaLoder.loadParameter()
# log handlers
basegetDataLogger = NewLogger(m_path=getDataLogpath, f_path=getDataLogFilePath)
getDataLogger = basegetDataLogger.setting()
# initial MQ parameter
mq_ip = getDataParameter['MQ']['ip']
mq_user = getDataParameter['MQ']['user']
mq_password = getDataParameter['MQ']['passwd']
mq_exchange = getDataParameter['MQ']['exchange']
mq_routing_key = getDataParameter['MQ']['routingkey']
mq_queue = getDataParameter['MQ']['queue']

# DB parameter
# 20190131 DB 库出错，暂时以正式环境替换readonly
# read only instance
db_ip = getDataParameter['DB_readonly']['ip']
db_port = int(getDataParameter['DB_readonly']['port'])
db_sid = getDataParameter['DB_readonly']['sid']
db_user = getDataParameter['DB_readonly']['user']
db_password = getDataParameter['DB_readonly']['passwd']

# db_ip = '10.42.0.198'
# db_port = 1521
# db_sid = 'GRYLDG'
# db_user = 'GRYL_TEST'
# db_password = 'sph'
# write only instance
db_ip_wr = getDataParameter['DB_wrightonly']['ip']
db_port_wr = int(getDataParameter['DB_wrightonly']['port'])
db_sid_wr = getDataParameter['DB_wrightonly']['sid']
db_user_wr = getDataParameter['DB_wrightonly']['user']
db_password_wr = getDataParameter['DB_wrightonly']['passwd']

# mq parameters
# send
mq_ip = getDataParameter['MQ']['ip']
mq_user = getDataParameter['MQ']['user']
mq_password = getDataParameter['MQ']['passwd']
mq_exchange = getDataParameter['MQ']['exchange']
mq_routing_ket = getDataParameter['MQ']['routingkey']
mq_queue = getDataParameter['MQ']['queue']


print('db_ip=',db_ip,type(db_ip))
print('db_port=',db_port,type(db_port))
print('db_sid=',db_sid,type(db_sid))
print('db_user=',db_user,type(db_user))
print('db_password=',db_password,type(db_password))
engine = createEngine(db_user, db_password, db_ip, db_port, db_sid)
CreateorReplaceTable(engine)
session = sessionmaker(bind=engine)
sess = session()
msg = []
flag = 0

if flag == 0:
    # get db data
    print('start get data')
    for row in sess.query(ALM_WECHAT_LIST).filter_by(TRANSFLAG = '00'):
        print('get data',row)
        row_data = []
        # print(row.ID)
        # print(row.MESSAGE)
        row_data.append(int(row.ID))
        row_data.append(row.COMPID)
        row_data.append(row.OWNERID)
        row_data.append(row.BUSTYPE)
        row_data.append(row.MESSAGE)
        row_data.append(row.USERCD)
        row_data.append(row.USERGRP)
        msg.append(row_data)
        print(msg)
        '''
        此处填写调用微信接口内容
        利用makedatamodel.py来构造推送信息体
        把传输的动作抽出来，利用下mq的队列，使微信的提醒不会报错或超出数量
        row==>makeDataModel==>mq==>sendMessage
        '''
        '''
        此处写一个MQ调用
        '''
    # send message to mq
    # update flag
    '''
    实现读写分离
    此处先回写10标记，表示已被传输。
    MQ处理完成后回传id，根据id变更标记为20，表示已被执行完毕
    '''
    if len(msg) == 0:
        print('no message needs to pushed!')
    else:
        # 创建mq链接
        rtflag,connect,parameter = createMQengine(mq_ip, mq_user, mq_password)
        channel = connect.channel()
        channel.exchange_declare(exchange=mq_exchange,exchange_type='direct')
        channel.queue_declare(queue=mq_queue,durable=True)
        # 把接收到的数据传输到sengMessage端
        # 序列化数据
        # 尝试用json序列化试试看
        # send_msg = cPickle.dumps(msg)
        print('msg type = ',type(msg))
        send_msg = json.dumps(msg)
        print('send_msg type = ',type(send_msg))
        # 推送数据
        channel.basic_publish(exchange=mq_exchange,routing_key=mq_routing_ket,body=send_msg,properties=parameter)
        connect.close()
        # 实例化writeback数据库连接
        engine_wr = createEngine(db_user_wr, db_password_wr, db_ip_wr, db_port_wr, db_sid_wr)
        CreateorReplaceTable(engine_wr)
        session_wr = sessionmaker(bind=engine_wr)
        sess_wr = session_wr()
        for i in msg:
            print(i[0])
            print('====================')
            query_str = sess_wr.query(ALM_WECHAT_LIST).filter_by(ID = i[0]).first()
            query_str.TRANSFLAG = '10'
        sess_wr.commit()
else:
    pass
    '''
    暂时没想到哪些可以在前面过滤的，待定
    '''
