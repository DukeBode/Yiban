'''
@Author: your name
@Date: 2020-05-07 23:08:55
@LastEditTime: 2020-05-08 18:14:29
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \Yiban\yiban\core.py
'''
import ssl
from http import cookiejar
from urllib import request

class Uri:
    ssl._create_default_https_context = ssl._create_unverified_context
    def __init__(self,ssl=True):
        self.protocol = 'https' if ssl else 'http'
        self.host = 'yiban.cn'
        self.cookie = cookiejar.CookieJar()
        handlers = request.HTTPCookieProcessor(self.cookie)
        self.opener = request.build_opener(handlers)
    
    def __call__(self,data):
        return f'{self.protocol}://{self.host}/{data}'

    def uri(self,address,data):
        return f'{self.protocol}://{address}.{self.host}/{data}'
    
    def data(self,request,code='utf-8'):
        with self.opener.open(request) as res:
            return res.read().decode(code)
        return None
