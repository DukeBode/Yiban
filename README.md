# Django Demo

- 添加 app

```sh
git clone -b Django-OAuth https://github.com/DukeBode/Yiban.git yiban
```

setting.py

INSTALLED_APPS = [
    ...,
    'yiban',
]

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

AUTH_USER_MODEL = 'yiban.User'

urls.py

from yiban.views import demo
    path('oauth/', include('yiban.urls')),
    path('admin/', admin.site.urls),
    path('',demo),
    