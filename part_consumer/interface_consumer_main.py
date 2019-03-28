__author__ = 'DozingWolf'
from basic_consumer_database_option import *
from basic_consumer_mq_option import *
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
db_user = 'MQ_IN'
db_password = 'MQ_IN'
# 创建mq链接
print('createMQ')
rtflag,connect,parameter = createMQengine(mq_ip, mq_user, mq_password)
print('createChannel')
channel = connect.channel()
# random_queue = channel.queue_declare(exclusive=True,durable=True)
# queue_name = random_queue.method.queue
print('declareQueue')
queue_name = channel.queue_declare(queue=mq_queue,durable=True)
print('bindQueue')
channel.queue_bind(exchange=mq_exchange, queue=mq_queue, routing_key=mq_routing_ket)
# 从MQ获取数据后解析
def cb(ch,method,properties,body):
    print('============================')
    print('body is',body)
    print('routing_key is',method.routing_key)
    ch.basic_ack(delivery_tag = method.delivery_tag)
print('defineQoS')
channel.basic_qos(prefetch_count=1)
channel.basic_consume(cb, queue=mq_queue) # ,no_ack=False
# 开始获取
print('please wait for message , to exit press ctrl+c')
channel.start_consuming()
# 创建DB链接
print('createDBEngine')
engine = createEngine(db_user, db_password, db_ip, db_port, db_sid)
# 接受方暂时不使用映射
# CreateorReplaceTable(engine)
print('createSession')
session = sessionmaker()
session.configure(bind=engine)
sess = session()
sess.commit()
