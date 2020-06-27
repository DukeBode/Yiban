'''
@Author: your name
@Date: 2020-05-08 00:05:45
@LastEditTime: 2020-06-06 11:09:57
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \Yiban\yiban\client.py
'''
from .core import Uri
from multiprocessing import Process
from http import cookiejar
from urllib import request, parse, error
import os, ssl, json, re

ssl._create_default_https_context = ssl._create_unverified_context

class WWW(Uri):
    def www(self,data):
        return super().uri('www',data)
        
    def json(self,url):
        req = request.Request(url,method='POST')
        content = super().data(req)
        print(content)
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

class Browser(Process):
    def set_browser(self,browser=None):
        if browser is not None:
            self.browser = browser
            return
        self.cookie = cookiejar.CookieJar()
        handlers = request.HTTPCookieProcessor(self.cookie)
        self.browser = request.build_opener(handlers)
    
    def rsa_Encrypt(self,data,data_keys):
        from base64 import b64encode
        from Crypto.PublicKey import RSA
        from Crypto.Cipher import PKCS1_v1_5
        rsa = RSA.importKey(data_keys)
        cipher = PKCS1_v1_5.new(rsa)
        data = cipher.encrypt(data.encode())
        return b64encode(data)
        
    def data_by_web(self, request):
        try:
            opener = self.browser
        except:
            self.set_browser()
            opener = self.browser
        with opener.open(request) as res:
            return res.read()
        return None
    
    def data_by_POST(self, url, data_dict=None, code='utf-8'):
        tmp_data = parse.urlencode(data_dict).encode(code)
        req = request.Request(url=url, method='POST', data=tmp_data)
        return self.data_by_web(req).decode(code)

    def data_by_GET(self, url, code='utf-8'):
        return self.data_by_web(url).decode(code)

    def run(self):
        print('用户',os.getpid())

class User(Browser):
    def __init__(self, account, password):
        self.account = account
        self.password = password
        super(User, self).__init__()
    
    def login_dict(self,content):
        try:
            url = URL.LOGIN_PAGE
        except:
            url = 'http://www.yiban.cn/login'
        login_re = re.compile('''(?sm)data-keys='([\s\S]*?)'.*'(.*?)'>''')
        if content is None:
            content = super().data_by_GET(url)
        data = login_re.search(content)
        data_keys, data_keys_time = data.groups()
        captcha = None if content is None else self.captcha(data_keys_time)
        return {
            'account': self.account,
            'password': super().rsa_Encrypt(self.password,data_keys),
            'captcha': captcha,
            'keysTimes': data_keys_time,
            # 'is_rember': 1
        }

    def captcha(self,keyTime):
        try:
            url = URL.LOGIN_CAPTCHA
        except:
            url = 'http://www.yiban.cn/captcha/index'
        finally:
            url = f'{url}?{keyTime.split(".")[0]}'
        data = super().data_by_web(url)
        with open(f'{keyTime}.png','wb') as f:
            f.write(data)
            f.flush()
            f.close()
        return input('请输入验证码：')

    def login(self,content=None):
        try:
            url = URL.LOGIN_URL
        except:
            url = 'http://www.yiban.cn/login/doLoginAjax'
        content =  self.data_by_POST(url,self.login_dict(content))
        try:
            json.loads(content)
        except:
            self.login(content)

    def logout(self):
        pass

    def checkin(self):
        try:
            url = URL.CHECK_IN
        except:
            url = 'http://www.yiban.cn/ajax/checkin/checkin'
        content = super().data_by_POST(url)
        json.loads(content)

    def forum(self):
        pass

    def run(self):
        super().run()

    # def getLogin(self):
    #     yiban = self.yiban
    #     url = yiban.www('ajax/my/getLogin')
    #     req = request.Request(url,method='POST')
    #     return json.loads(yiban.data(req))

    # def checkin(self):
    #     yiban = self.yiban
    #     url = yiban.www('ajax/checkin/checkin')
    #     req = request.Request(url,method='POST')
    #     return json.loads(yiban.data(req))