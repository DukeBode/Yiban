from urllib import request, parse
from django.conf.settings import YIBAN_CONFIG as config
import json

class Yiban:
    @classmethod
    # POST 方法封装
    def POST(cls,url,data):
        params = parse.urlencode(data).encode("utf-8")
        response = request.urlopen(url,data=params)
        return json.loads(response.read().decode("utf-8"))

    @classmethod
    # GET 方法封装
    def GET(cls,url,data):
        string = f'{url}?{parse.urlencode(data)}'
        response = request.urlopen(string)
        return json.loads(response.read())

    @classmethod
    # GET重定向授权页面
    def login(cls):
        url = 'https://openapi.yiban.cn/oauth/authorize'
        params = parse.urlencode({
            'client_id': config.client_id,
            'redirect_uri': config.redirect_uri,
            'state': config.state
        })
        return f'{url}?{params}'

#

    @classmethod
    # 获取当前用户基本信息。
    def get_user(cls,access_token):
        return cls.GET(
            'https://openapi.yiban.cn/user/me',{
                'access_token': access_token,
        })

# 好友关系接口

    @classmethod
    # 获取当前用户好友列表。
    def get_user_friend(cls, access_token, page, count):
        return cls.GET(
            'https://openapi.yiban.cn/friend/me_list',{
                'access_token': access_token,
                'page': page,
                'count': count,
        })
    
    @classmethod
    # 当前用户与指定用户是否为好友关系。
    def check_friend(cls, access_token, yb_friend_uid):
        return cls.GET(
            'https://openapi.yiban.cn/friend/check',{
                'access_token': access_token,
                'yb_friend_uid': yb_friend_uid,
        })

    @classmethod
    # 获取推荐好友列表。
    def recommend_friend(cls, access_token, count):
        return cls.GET(
            'https://openapi.yiban.cn/friend/recommend',{
                'access_token': access_token,
                'count':count,
        })
    
    @classmethod
    # 发送好友申请。
    def apply_friend(cls, access_token, to_yb_uid, content='好友申请'):
        return cls.POST(
            'https://openapi.yiban.cn/friend/apply',{
                'access_token': access_token,
                'to_yb_uid': to_yb_uid,
                'content': content,
        })

    @classmethod
    # 删除指定好友。
    def remove_friend(cls,access_token, yb_friend_uid):
        return cls.GET(
            'https://openapi.yiban.cn/friend/remove',{
                'access_token': access_token,
                'yb_friend_uid': yb_friend_uid,
        })

# 消息接口

    @classmethod
    # 向指定用户发送易班站内信应用提醒。
    def letter(cls,access_token,to_yb_uid,content='hello',template='system'):
        url = 'https://openapi.yiban.cn/msg/letter'
        params = {
            'access_token': access_token,
            'to_yb_uid': to_yb_uid,
            'content': content,
            # 'template': template,
        }
        return cls.POST(url,params)

# 资讯服务接口

    @classmethod
    # 获取易班推荐资讯。
    def news(cls,access_token, page=1, count=15):
        # count 最大 30
        return cls.GET(
            'https://openapi.yiban.cn/news/yb_push',{
                'access_token': access_token,
                'page': page,
                'count': count,
        })

# 扩展接口

    @classmethod
    # 获取易班app运动计步数据。
    def sport_steps(cls, access_token, days=7):
        # days 最大 90
        return cls.GET(
            'https://openapi.yiban.cn/extend/sport_steps',{
                'access_token': access_token,
                'days': days,
        })

class Oauth:
    def __init__(self):
        self.client_id = config.client_id
        self.client_secret = config.client_secret
        self.redirect_uri = config.redirect_uri
        self.state = config.state
        self.dev_uid = config.dev_uid

    # 获取已授权用户的access_token。
    def get_access_token(self, code):
        return Yiban.POST(
            'https://openapi.yiban.cn/oauth/access_token',{
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'code': code,
                'redirect_uri': self.redirect_uri,
            })
    
    # 校验用户是否授权，如已授权状态expire_in值为0，则该授权凭证已过期，需要重新授权。
    def check_token_info(self, access_token, yb_uid):
        url = 'https://openapi.yiban.cn/oauth/token_info'
        params = {
            'client_id': self.client_id,
            'access_token':access_token,
            'yb_uid':yb_uid,
        }
        return Yiban.POST(url,params)
    
    # 开发者主动取消指定用户的授权。
    def revoke_token(self, access_token):
        url = 'https://openapi.yiban.cn/oauth/revoke_token'
        params = {
            'client_id': self.client_id,
            'access_token':access_token,
        }
        return Yiban.POST(url,params)
    
    # 重置开发者在其所创建应用中的有效授权。
    def reset_token(self, access_token):
        url = 'https://openapi.yiban.cn/oauth/reset_token'
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'dev_uid': self.dev_uid
        }
        return Yiban.POST(url,params)
       
