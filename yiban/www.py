'''
@Author: your name
@Date: 2020-04-28 14:27:42
@LastEditTime: 2020-05-06 23:42:13
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \Yiban\yiban\www.py
'''

class User:
    def __init__(self):
        pass

# https://www.yiban.cn/ajax/my/getLogin
# https://www.yiban.cn/login/doLoginAjax
# https://www.yiban.cn/captcha/index
# yiban_user_token	
# https://www.yiban.cn/ajax/my/getLogin
# https://www.yiban.cn/ajax/user/isSchoolPop

headers = ( 'User-Agent' , 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36' )

from http import cookiejar
from urllib import request, parse, error
import json,re,base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import ssl
 
ssl._create_default_https_context = ssl._create_unverified_context

cookie = cookiejar.CookieJar()
handlers = request.HTTPCookieProcessor(cookie)
opener = request.build_opener(handlers)
# opener.addheaders = [headers]

def login_pr(content=False):
    login_re = re.compile('''(?sm)data-keys='([\s\S]*?)'.*'(.*?)'>''')
    if content:
        return login_re.search(content).groups()
    url = 'https://www.yiban.cn/login'
    with opener.open(url) as res:
        content = res.read().decode("utf-8")
        return login_re.search(content).groups()

def rsaEncrypt(password,data_keys):
    rsa = RSA.importKey(data_keys)
    cipher = PKCS1_v1_5.new(rsa)
    pwd = cipher.encrypt(password.encode())
    return base64.b64encode(pwd)

def loginCaptcha(keyTime):
    url = f'https://www.yiban.cn/captcha/index?{keyTime.split(".")[0]}'
    with opener.open(url) as res:
        data = res.read()
        with open(f'{keyTime}.png','wb') as f:
            f.write(data)
            f.flush()
            f.close()

def login_page(login_dict):
    login_data = parse.urlencode(login_dict).encode('utf-8')
    login_url = 'https://www.yiban.cn/login/doLoginAjax'
    req = request.Request(login_url,data=login_data,method='POST')
    with opener.open(req) as res:
        content = res.read().decode("utf-8")
        try:
            data = json.loads(content)
            print(data)
            for item in cookie:
                print(f'{item.name}={item.value}')
        except:
            return content
    return None
        # print(res.status)
        # print(res.info())
        # print(res.read().decode())
        # print(res.headers['Content-Type'])

def login(account,password,data=None):
    data_keys,data_keys_time = login_pr(data)
    loginCaptcha(data_keys_time)
    if data is not None:
        captcha = input('请输入验证码：')
    else:
        captcha = None
    login_dict = {
        'account': account,
        'password': rsaEncrypt(password,data_keys),
        'captcha': captcha,
        'keysTime': data_keys_time,
        # 'is_rember': 1
    }
    content = login_page(login_dict)
    if content is not None:
        login(account,password,content)
    url = 'https://www.yiban.cn/ajax/my/getLogin'
    req = request.Request(url,method='POST')
    with opener.open(req) as res:
        tmp = json.loads(res.read().decode('utf-8'))
        print(tmp['data']['isLogin'])