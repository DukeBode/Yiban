'''
@Author: your name
@Date: 2020-05-08 00:05:45
@LastEditTime: 2020-06-06 11:09:57
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \Yiban\yiban\client.py
'''
from .core import Uri

from http import cookiejar
from urllib import request, parse, error
import json,re
import ssl

class WWW(Uri):
    def www(self,data):
        return super().uri('www',data)
        
    def json(self,url):
        req = request.Request(url,method='POST')
        content = super().data(req)
        return json.loads(content)

    def captcha(self,keyTime):
        url = self.www(f'captcha/index?{keyTime.split(".")[0]}')
        with self.opener.open(url) as res:
            return res.read()
        return None
    
    def login(self,go=None):
        url = self.www('login')
        return super().data(url)
    
    def doLoginAjax(self,login_dict):
        login_url = self.www('login/doLoginAjax')
        login_data = parse.urlencode(login_dict).encode('utf-8')
        req = request.Request(login_url,data=login_data,method='POST')
        return super().data(req)

    def getLogin(self):
        url = self.www('ajax/my/getLogin')
        return self.json(url)
        req = request.Request(url,method='POST')
        return super().data(req)
        
    def rsaEncrypt(self,password,data_keys):
        '''
        @description: 
            RSA 加密
        @param
            password:
            data_keys:
        @return: 
        '''
        from base64 import b64encode
        from Crypto.PublicKey import RSA
        from Crypto.Cipher import PKCS1_v1_5
        rsa = RSA.importKey(data_keys)
        cipher = PKCS1_v1_5.new(rsa)
        pwd = cipher.encrypt(password.encode())
        return b64encode(pwd)

class User:
    def __init__(self,account,password):
        self.yiban = WWW()
    
    def getLogin(self):
        yiban = self.yiban
        url = yiban.www('ajax/my/getLogin')
        req = request.Request(url,method='POST')
        return json.loads(yiban.data(req))

    def checkin(self):
        yiban = self.yiban
        url = yiban.www('ajax/checkin/checkin')
        req = request.Request(url,method='POST')
        return json.loads(yiban.data(req))
    