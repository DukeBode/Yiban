
from urllib import request
from http import cookiejar
import ssl
        
class User:
    
    # 登录状态
    @property
    def status(self):
        url = self.www('ajax/my/getLogin')
        req = request.Request(url,method='POST')
        import json
        tmp = json.loads(content)
        print(tmp['data']['isLogin'])
