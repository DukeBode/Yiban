
from urllib import request
from http import cookiejar
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
class Browser:
    def __init__(self,browser=None):
        if browser is None:
            self.cookie = cookiejar.CookieJar()
            handlers = request.HTTPCookieProcessor(cookie)
            self.opener = request.build_opener(handlers)
        else:
            self.opener = browser
    
    def data(self,request,code='utf-8'):
        with self.opener.open(request) as res:
            return res.read().decode(code)
        return None

    def json(self,request,method='POST'):
        req = request.Request(url,method=method)
        content = self.data(req)
        return json.loads(content)

    def img(self,url):
        with self.opener.open(url) as res:
            return res.read()
        return None
        
class User:
    def __init__(self,account,password):
        self.cookie = cookiejar.CookieJar()
        handlers = request.HTTPCookieProcessor(cookie)
        self.opener = request.build_opener(handlers)
        self.account = account
        self.password = password
    
    # 浏览器
    @property
    def browser(self):
        return self.opener
    
    # 登录状态
    @property
    def status(self):
        url = self.www('ajax/my/getLogin')
        req = request.Request(url,method='POST')
        import json
        tmp = json.loads(content)
        print(tmp['data']['isLogin'])

    def rsaEncrypt(self,data,data_keys):
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
        data = cipher.encrypt(data.encode())
        return b64encode(data)
    
    # 登录所需信息
    def login_dict(self,content=None):
        login_re = re.compile('''(?sm)data-keys='([\s\S]*?)'.*'(.*?)'>''')
        if content is None:
            pass
        data = login_re.search(content)
        data_keys,data_keys_time = data.groups()
        return {
            'account': self.account,
            'password': self.rsaEncrypt(self.password,data_keys),
            'captcha': captcha,
            'keysTime': data_keys_time,
            # 'is_rember': 1
        }

    # 登录
    def login(self):
        login_dict()

    # 登出
    def logout(self):pass

class Status:
    pass

if __name__ == "__main__":
    mymethod(2) 
        