__author__ = 'DozingWolf'
from basic_producer_mq_option import *
from basic_producer_database_option import *
# from basic_tool import *
import json
import io
import sys
import _pickle as cPickle
#用于解决print乱码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
# MQ parameter
mq_ip = '10.62.24.70'
mq_user = 'admin'
mq_password = 'admin@123'
mq_exchange = 'TEST_EXCHANGE_TOPIC'
mq_routing_ket = 'interface.001'
mq_queue = 'interface'
# DB parameter
db_ip = '10.62.24.24'
db_port = 1521
db_sid = 'orcl12c'
db_user = 'MQ_OUT'
db_password = 'MQ_OUT'
# 创建mq链接
rtflag,connect,parameter = createMQengine(mq_ip, mq_user, mq_password)
channel = connect.channel()
channel.exchange_declare(exchange=mq_exchange,exchange_type='topic')
channel.queue_declare(queue=mq_queue,durable=True)
# 创建DB链接
engine = createEngine(db_user, db_password, db_ip, db_port, db_sid)
CreateorReplaceTable(engine)
session = sessionmaker(bind=engine)
sess = session()
# 取DB中数据
for row in sess.query(T_OUT_TP_D).filter_by(sendfg = '00'):
    print('======================')
    print(cPickle.dumps(row))
    msgbody = cPickle.dumps(row)
    channel.basic_publish(exchange=mq_exchange,routing_key=mq_routing_ket,body=msgbody,properties=parameter)
    # row.sendfg = '20'
    print('success!')
sess.commit()
connect.close()
