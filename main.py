'''
@Author: your name
@Date: 2020-04-28 14:57:08
@LastEditTime: 2020-06-06 13:07:24
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \Yiban\main.py
'''

# yiban_user_token	
# https://www.yiban.cn/ajax/my/getLogin
# ['data']['checkin']
# https://www.yiban.cn/ajax/user/isSchoolPop

headers = ( 'User-Agent' , 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36' )

from http import cookiejar
from urllib import request, parse, error
import json,re
from yiban.client import WWW
cli = WWW()

# opener.addheaders = [headers]

def login_dict(account,password,captcha=None):
    '''
    @description: 
        获取 RSA 公钥，和时间
    @param
        content: 登录页内容
    @return: 
    '''
    login_re = re.compile('''(?sm)data-keys='([\s\S]*?)'.*'(.*?)'>''')
    content = cli.login() if captcha is None else captcha
    data = login_re.search(content)
    data_keys,data_keys_time = data.groups()
    loginCaptcha(data_keys_time)
    captcha = None if captcha is None else input('请输入验证码：')
    return {
        'account': account,
        'password': cli.rsaEncrypt(password,data_keys),
        'captcha': captcha,
        'keysTime': data_keys_time,
        # 'is_rember': 1
    }

def loginCaptcha(keyTime):
    data = cli.captcha(keyTime)
    with open(f'{keyTime}.png','wb') as f:
        f.write(data)
        f.flush()
        f.close()

def login(account,password,data=None):
    content = cli.doLoginAjax(login_dict(account,password,data))
    try:
        data = json.loads(content)
    except:
        login(account,password,content)
    
def checkin():
    '''
    @description: 签到
    @param {type} 
    @return: 
    '''
    url = cli.www('ajax/checkin/checkin')
    tmp = cli.json(url)
    from bs4 import BeautifulSoup
    if tmp['code'] == 202:
        print(tmp['message'])
        return None
    soup = BeautifulSoup(tmp['data']['survey'],'html.parser')
    for a in soup.select('.survey-option'):
        data={
            'optionid[]': a['data-value'],
            'input': None
        }
        break
    url = cli.www('ajax/checkin/answer')
    login_data = parse.urlencode(data).encode('utf-8')
    req = request.Request(url,data=login_data,method='POST')
    return cli.data(req)

if __name__ == "__main__":
    from ruamel.yaml import YAML

    config=None
    with open('config.yml','r',encoding="utf-8") as f: 
        print(cli.getLogin())
        config =YAML(typ='safe').load(f.read())
        login(config['account'],config['password'])
        checkin()
        content = cli.getLogin()
        print(content['data']['isLogin'],content['data']['user'])
    # 删除验证码
    from yiban.base import File
    File.clean('png')
    # page=config['page_dir']