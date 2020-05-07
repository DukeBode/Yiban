'''
@Author: your name
@Date: 2020-05-08 00:05:45
@LastEditTime: 2020-05-08 00:43:57
@LastEditors: your name
@Description: In User Settings Edit
@FilePath: \Yiban\yiban\client.py
'''
from core import Uri

from http import cookiejar
from urllib import request, parse, error
import json,re
import ssl
 
ssl._create_default_https_context = ssl._create_unverified_context

cookie = cookiejar.CookieJar()
handlers = request.HTTPCookieProcessor(cookie)
opener = request.build_opener(handlers)

class WWW(Uri):
    def www(self,data):
        return super().uri('www',data)
    
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