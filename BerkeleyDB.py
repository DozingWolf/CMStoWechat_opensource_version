#coding=utf-8
__author__ = 'DozingWolf'
from json2para import ParaLoder
from hashcheck import ParaHashcheck
from bsddb3 import db
import bsddb3
import time,sys
import struct
import os,stat

'''
only support btree mode
'''
'''
需要考虑把数据类型转换模块抽象化成一个方法
'''
class BerkeleyDB(object):
    def __init__(self,b_path,b_file):
        self.__os = os.name
        self.dbenv = db.DBEnv()
        self.bsddb_path = b_path
        if self.__os == 'posix':
            os.makedirs(name=self.bsddb_path,mode=0o666,exist_ok=True)
        else:
            # os windows
            pass
        self.bsddb_file = b_file
        self.dbenv.open(b_path,db.DB_CREATE | db.DB_INIT_MPOOL)
        self.dbinst = db.DB(self.dbenv)
        self.dbinst.open(b_file,db.DB_BTREE,db.DB_CREATE,mode=0o666)
        print(self.bsddb_path+self.bsddb_file)
        if self.__os == 'posix':
            # if os = posix, add chmod
            os.chmod(self.bsddb_path+'/'+self.bsddb_file,stat.S_IRWXU)
        else:
            # os windows
            pass
    def __pint2cint(self,indata):
        return struct.pack('i', indata)
    def insertdata(self,key,value):
        if isinstance(key, int):
            # print(key,'is int')
            inner_key = self.__pint2cint(indata=key)
        else:
            # print(key,'is str')
            inner_key = key.encode(encoding='utf-8')
        try:
            self.dbinst.put(inner_key,value)
            self.dbinst.sync()
        except Exception as e:
            raise
    def readalldata(self):
        result = self.dbinst.items()
        return result
    def readpairdate(self,key):
        if isinstance(key, int):
            inner_key = self.__pint2cint(indata=key)
        else:
            inner_key = key.encode(encoding='utf-8')
        result = self.dbinst.get(inner_key)
        return result
    def droppairdata(self,key):
        if isinstance(key, int):
            inner_key = self.__pint2cint(indata=key)
        else:
            inner_key = key.encode(encoding='utf-8')
        try:
            self.dbinst.delete(inner_key)
            self.dbinst.sync()
        except Exception as e:
            raise
    def closedb(self):
        self.dbinst.close()
    def closeenv(self):
        self.dbenv.close()
# #20190325 start
# # demo
# file_path = './parameter/SHA1'
# para_path = './parameter/parameter.json'
# # hash data check
# newPareChecker = ParaHashcheck(f_path=file_path, p_path=para_path)
# checkResultFlag = newPareChecker.checkparameter()
# # load parameter
# paraLoder = ParaLoder(para_path, checkResultFlag, 'BerkeleyDB' )
# paraIteam = paraLoder.loadParameter()
#
# bsddb_path = paraIteam['BerkeleyDB']['bdb_path']
# bsddb_file = paraIteam['BerkeleyDB']['Token_DB']
#
# bdb = BerkeleyDB(b_path=bsddb_path, b_file=bsddb_file)
# dataresult = bdb.readpairdate(key='TOKEN')
# dataresult = dataresult.decode(encoding='utf-8')
# print(dataresult)
# bdb.closedb()
# bdb.closeenv()
#
# # bdb.droppairdata(key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb3JwaWQiOiJDTVNzUm8yTnIxZjZnWXkzclI3IiwiZXhwIjoxNTUzNzc1MTUzLCJpYXQiOjE1NTM1MTU5NTN9.B4ZzWkvCWEQ4ErP5FlEf9o-wwwpHNLbMpVCr_uJb-Dg')
# # #
# # # bdb.insertdata(key='tokenAjmbasjfhGJjkyhgrfaw&^%$1293871kjhasfdk', value='this is a test token')
# readdata = bdb.readalldata()
# print(readdata)
# print(type(readdata))
# #print(readdata[0][0])
# # new_data = readdata[0][0].decode(encoding='utf-8')
# # print(new_data)
# # print('===================')
# readpairdatecollection = bdb.readpairdate(key='TOKEN')
# bdb.closedb()
# bdb.closeenv()
# 20190325 end
#
# dbenv = db.DBEnv()
# dbenv.open(bsddb_path,db.DB_CREATE | db.DB_INIT_MPOOL)
#
# dbinst = db.DB(dbenv)
# dbinst.open(bsddb_file,db.DB_BTREE,db.DB_CREATE,666)
# # for calc in range(10001,30000):
# #     pass
# #     num = struct.pack('i', calc)
# #     str_clc = str(calc)
# #     str_line = 'number is ' + str_clc
# #     dbinst.put(num,str_line)
#
# print(dbinst.items())
#
# dbinst.sync()
#
# key_list = dbinst.keys()
# print('keylist is:',key_list)
# dbinst.close()
#
# dbenv.close()
#
# # # finally,it's done!!!welldone guys!
# # num = struct.pack('i', 1)
# # print('num struct is:',num)
# # print(type(num))
# # d = bsddb3.hashopen('./BSDDB/TEST_DB','c')
# # d[num] = 'csy'
# # print(d.items())
# # d.close()
