from urllib import request, parse
# import requests
# import time
# from xml.etree import ElementTree as ET

class MediaPlatform:
    pass
#     def __init__(self, host):
#         self.BASE_URL = 'http://mp.yiban.cn/'
#         self.payload = dict(
#             grant_type='client_credentials',
#             appid=host['AppId'],
#             secret=host['AppSceret'],
#         )
#         self.__end_time = 0
#         self.data = {}

#     @property
#     def access_token(self):
#         if self.__end_time <= time.time():
#             req = requests.post(
#                 url=f'{self.BASE_URL}cgibin/oauth/token', data=self.payload)
#             self.data = req.json()
#             print(self.data)
#             try:
#                 self.__end_time = time.time() + int(self.data['expires_in'])
#             except KeyError:
#                 return ''
#         return self.data['access_token']

#     def group_create(self):
#         # http: // mp.yiban.cn / cgibin / groups / create?access_token = ACCESS_TOKEN
#         pass

#     @property
#     def group_list(self):
#         req = requests.get(url=self.BASE_URL + f'cgibin/groups/get?access_token={self.access_token}')
#         return req.json()

#     # 用户所在分组
#     def group_search(self, openid):
#         req = requests.post(url=f'{self.BASE_URL}cgibin/groups/getid?access_token={self.access_token}', data={
#             'openid': openid,
#         })
#         return req.json()

#     def group_update(self):
#         # http: // mp.yiban.cn / cgibin / groups / update?access_token = ACCESS_TOKEN
#         pass

#     def group_move(self):
#         # http: // mp.yiban.cn / cgibin / groups / members / update?access_token = ACCESS_TOKEN
#         pass

#     def user_info(self, openid, lang='zh_CN'):
#         req = requests.get(url=f'{self.BASE_URL}cgibin/user/info', params={
#             'access_token': self.access_token,
#             'openid': openid,
#             'lang': lang,
#         })
#         return req.json()

#     def user_list(self, next_openid=''):
#         # data = '&next_openid={next_openid}'
#         req = requests.get(url=f'{self.BASE_URL}cgibin/user/get?access_token={self.access_token}')
#         return req.json()

#     @property
#     def menu(self):
#         req = requests.get(url=f'{self.BASE_URL}cgibin/menu/get?access_token={self.access_token}')
#         return req.json()

#     # 自定义菜单
#     @menu.setter
#     def menu(self, data):
#         if data:
#             # {'errcode': 43002, 'errmsg': '需要POST请求'}
#             req = requests.post(url=f'{self.BASE_URL}cgibin/menu/create?access_token={self.access_token}', data=data)
#         else:
#             req = requests.get(url=f'{self.BASE_URL}cgibin/menu/delete?access_token={self.access_token}')
#         print(req.json())