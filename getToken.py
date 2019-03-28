#coding=utf-8
__author__ = 'DozingWolf'
import requests
import json
import time
from BerkeleyDB import BerkeleyDB
from logger import NewLogger
from hashcheck import ParaHashcheck
from json2para import ParaLoder
'''
设计思路：
    获取token
        输入密钥，获取返回值
    解释token状态
    验证token
        是否需要设计重连计数器？？
        还是把重连计数器设计在验证里面？？
    传输数据放到另一个py包里面去
    这个py包仅进行token获取验证的相关工作
    未来corpid和secret等参数考虑使用json或xml在外部定义后传入
'''
# 20190325 先注释下
# file_path = './parameter/SHA1'
# para_path = './parameter/parameter.json'
# # hash data check
# newPareChecker = ParaHashcheck(f_path=file_path, p_path=para_path)
# checkResultFlag = newPareChecker.checkparameter()
# # load parameter
# paraLoder = ParaLoder(para_path, checkResultFlag, 'Wechat_interface', 'BerkeleyDB' )#'''checkResultFlag'''
# parameter = paraLoder.loadParameter()
#
# if parameter['result'] == 1:
#     data = {'corpid': parameter['Wechat_interface']['corpid'],'secret': parameter['Wechat_interface']['secret']}
#     url = parameter['Wechat_interface']['gettokenurl']
# else:
#     print('Error , systeam will be exited by parameter_hash_check_error')
#     exit()
# response = requests.post('http://www.umisu.com/api/wechat-v1/token/get', data=data)

class TokenOperator(object):
    def __init__(self):
        self.__timer = 0
        self.__paraSHA1Path = './parameter/SHA1'
        self.__paraFilePath = './parameter/parameter.json'
        self.__tokenLogpath = './log/'
        self.__logfilepath = 'TOKENOPERSTOR_LOG.log'
        # check
        self.__newParaChecker = ParaHashcheck(f_path=self.__paraSHA1Path, p_path=self.__paraFilePath)
        self.__checkResulfFlag = self.__newParaChecker.checkparameter()
        # parameter
        self.__paraLoder = ParaLoder(self.__paraFilePath, self.__checkResulfFlag,'Wechat_interface', 'BerkeleyDB')
        self.__parameter = self.__paraLoder.loadParameter()
        # log handlers
        self.__baseTokenLogger = NewLogger(m_path=self.__tokenLogpath, f_path=self.__logfilepath)
        self.__tokenLogger = self.__baseTokenLogger.setting()
        # create data dict
        self.__data = {'corpid': self.__parameter['Wechat_interface']['corpid'],'secret': self.__parameter['Wechat_interface']['secret']}
        self.__url = self.__parameter['Wechat_interface']['gettokenurl']
        # bsddb
        self.__dbHandle = BerkeleyDB(b_path=self.__parameter['BerkeleyDB']['bdb_path'], b_file=self.__parameter['BerkeleyDB']['Token_DB'])

    def getTokenFromServer(self):
        while self.__timer <= 2:
            response = requests.post(self.__url, data=self.__data)
            inner_resp = json.loads(response.text)
            if inner_resp['errcode']==0:
                self.__dbHandle.insertdata(key='TOKEN', value=inner_resp['AccessToken'])
                self.__timer = 999
                self.__tokenLogger.info('Get token success!')
                return inner_resp['AccessToken']
            else:
                self.__tokenLogger.warning('Get token failed ,system will be try it later...(%d/3)'%self.__timer+1)
                time.sleep(pow(self.__timer+1,3))
                self.__timer += 1
                if self.__timer == 2:
                    self.__tokenLogger.warning('Get token failed 3 times')
                    inner_resp = 0
                    return inner_resp

    def getTokenFromDB(self):
        innerdata = self.__dbHandle.readpairdate(key='Token')
        if innerdata:
            return innerdata.decode(encoding='utf-8')
        else:
            return 0

    def getToken(self,source='DB'):
        if source == 'DB':
            innerData = self.getTokenFromDB()
            if innerData == 0:
                innerData = self.getTokenFromServer()
            return innerData
        elif source == 'SERVER':
            innerData = self.getTokenFromServer()
            return innerData
        else:
            self.__tokenLogger.warning('getToken function parameter error')
            innerData = self.getTokenFromDB()
            return innerData

    def checkToken(self):
        pass

tokenGeter = TokenOperator()
accesstokenCode = tokenGeter.getToken(source='SERVER')
print(accesstokenCode)

# '''
# 封装一下getToken模块，设计未来调用
# 申明getToken类，实例化，
# 根据配置参数获取url地址与BerkeleyDB参数，
# 请求获取token
# 设置计数器
# 如果成功
#     写入BerkeleyDB，key=WechatToken，value=token
#     返回token给外部
# 如果失败
#     计数+1
#     如果计数器达到3
#     返回错误信息
# '''
# 20190325先注释下
# def getToken(access_group=data,url=url):
#     print('start get token')
#     response = requests.post(url, data=access_group)
#     inner_resp = json.loads(response.text)
#
#     return inner_resp
#
# def checkToken(resp):
#     print('start check token')
#     if resp['errcode'] == 0:
#         token_status = [1,0,'succ']
#     elif resp['errcode'] > 0:
#         token_status = [-1,resp['errcode'],resp['errmsg']]
#     elif resp['errcode'] < 0:
#         token_status = [-1,resp['reecode'],resp['errmsg']]
#     return token_status
#
# def checkValidity(token,url):
#     '''
#     等待国润微信平台侧提供正式有效性测试接口
#     微信平台不提供该接口，本方法作废
#     '''
#     pass

# test_code
# token_resp = getToken(data,url)
# check_rest = checkToken(token_resp)
# print(check_rest)
# headers = {'Content-Type': 'application/json',}
# service_url = 'http://www.umisu.com/api/wechat-v1/message/send'
# params = (('access_token',token_resp['AccessToken']),)
# data = '{"msgtype":"text","agentid":1,"text":{"content":"你好！"},"key":"CMSSyetemErr"}'
# data = data.encode('utf-8')
# response = requests.post(service_url, headers=headers, params=params, data=data)
#
# print(response)
# print(response.text)
# print(type(response.text))
# json_str = response.text
# print('json data was:',json_str)
# print(type(json_str))
# json_str_format = json.loads(json_str)
# print(type(json_str_format))
# print(json_str_format)
# print('=============================')
# print(json_str_format['errcode'])
# print(json_str_format['errmsg'])
# print(json_str_format['request_id'])
# print(json_str_format['data'])
# print(json_str_format['AccessToken'])
