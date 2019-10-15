# Django Demo

- 添加 app

```sh
git clone -b Django-OAuth https://github.com/DukeBode/Yiban.git yiban
```
- 配置文件

setting.py

```py
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