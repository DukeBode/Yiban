# Django Demo

- 添加 app

```sh
git clone -b Django-OAuth https://github.com/DukeBode/Yiban.git yiban
```
- 配置文件

setting.py

```py
# 指定应用开发者的易班用户id
dev_uid = '8465441'
# 应用 appID
client_id = '029d1d60cfee89f1'
# 应用 appsecret
client_secret = '6c7fb7e0e357db28cc1e17057437d575'
# 应用回调地址
redirect_uri = 'http://yiban.dukestudio.site/oauth/back'
# 防跨站伪造参数
state = 'state'

AUTH_USER_MODEL = 'yiban.User'

INSTALLED_APPS = [
    ...,
    'yiban',
]
```

urls.py

```py
from django.urls import include, path

from yiban.views import demo

urlpatterns = [
    path('oauth/', include('yiban.urls')),
    path('admin/', admin.site.urls),
    path('',demo),
]
```    

- 迁移数据，启动测试
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```