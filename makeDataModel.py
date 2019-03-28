#coding=utf-8
__author__ = 'DozingWolf'
import re
'''
in:COMPID,OWNERID,BUSTYPE,MESSAGE
out:message body
'''
# compile data replace method
class DataReplace(object):
    # string = ''
    def __init__(self):
        # self.string = in_string
        self.ruler_1 = re.compile(r'[\r]')
        '''
        future , u can add replace ruler @ here
        '''
    def datareplace(self,msg):
        inner_msg = self.ruler_1.sub('!',msg)
        return inner_msg

def dataModel(bustype,msg):
    datareplacer = DataReplace()
    inner_str = datareplacer.datareplace(msg)
    if bustype == 'SAL':
        msg_body = '订单员您好！您有信息发送自CMS6.0，请查阅～'+inner_str
    elif bustype == 'PUR':
        msg_body = '采购员您好！您有信息发送自CMS6.0，请查阅～'+inner_str
    elif bustype == 'SYS':
        msg_body = '系统出现错误，请尽快检查！'+inner_str
    # msg_body = msg_body.decode('utf-8')
    print('return message is :',msg_body)
    return msg_body

# print(sys.stdout.encoding)

# msg = dataModel('SAL','HELLO!')
# print(msg.__class__)
# print(msg.code('utf-8'))
