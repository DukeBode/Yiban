'''
@Author: your name
@Date: 2020-04-28 14:57:08
@LastEditTime: 2020-05-08 18:30:54
@LastEditors: your name
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

def login_pr(content=False):
    '''
    @description: 
        获取 RSA 公钥，和时间
    @param
        content: 登录页内容
    @return: 
    '''
    login_re = re.compile('''(?sm)data-keys='([\s\S]*?)'.*'(.*?)'>''')
    if not content:
        content = cli.login()
    return login_re.search(content).groups()

def loginCaptcha(keyTime):
    data = cli.captcha(keyTime)
    with open(f'{keyTime}.png','wb') as f:
        f.write(data)
        f.flush()
        f.close()

def login_page(login_dict):
    content = cli.doLoginAjax(login_dict)
    try:
        data = json.loads(content)
        print(data)
        # for item in cookie:
        #     print(f'{item.name}={item.value}')
    except:
        return content
    return None

def login(account,password,data=None):
    data_keys,data_keys_time = login_pr(data)
    loginCaptcha(data_keys_time)
    if data is not None:
        captcha = input('请输入验证码：')
    else:
        captcha = None
    login_dict = {
        'account': account,
        'password': cli.rsaEncrypt(password,data_keys),
        'captcha': captcha,
        'keysTime': data_keys_time,
        # 'is_rember': 1
    }
    content = login_page(login_dict)
    if content is not None:
        print(1)
        login(account,password,content)
    
    

def checkin():
    url = cli.www('ajax/checkin/checkin')
    tmp = cli.json(url)
    from bs4 import BeautifulSoup
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
    # cli.getCaptcha('1588867188.14')
    # content = cli.getLogin()
    # tmp = json.loads(content)
    # print(tmp['data']['isLogin'])
    # print(checkin())
    from ruamel.yaml import YAML

    config=None
    with open('config.yml','r',encoding="utf-8") as f:
        config =YAML(typ='safe').load(f.read())
        login(config['account'],config['password'])
    # page=config['page_dir']