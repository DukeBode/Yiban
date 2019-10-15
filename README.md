# Django Demo

## 文件说明：

- README.md 本文档
- /venv python 环境
- /Django Demo 工程目录
- requirements.txt 依赖环境
- nginx_default.conf nginx 配置模板


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

## 开发常用操作
- 激活环境，切换至工程目录
```sh
source ./venv/bin/activate && cd Django
```

- 迁移数据
```sh
python manage.py makemigrations && python manage.py migrate
```

- 创建超级用户
```
python manage.py createsuperuser
```

- 使用 5151 端口，测试服务
```
python manage.py runserver 5151
```

- 创建 nginx 配置文件
```
cp nginx_default.conf nginx.conf
```

- 为 nginx 配置设置软连接
```
ln -s /data/yiban/nginx.conf /etc/nginx/conf.d/yiban.conf
```

- 重启 NGINX
```
nginx -s reload
```

- 删除迁移文件及 sqlite 数据
```
rm -r  */migrations/*_initial.py *.sqlite3
```

python manage.py collectstatic

uwsgi -d --ini uwsgi.ini


- 建环境
python3 -m venv ./venv

- 激活环境
source ./venv/bin/activate
deactivate

- 更新 pip
pip install --upgrade pip
pip install django
pip freeze > requirements.txt

- 创建项目
django-admin startproject Django && cd Django

- 创建 yiban
python manage.py startapp yiban




## sqlite

cd /usr/src

wget https://www.sqlite.org/2019/sqlite-autoconf-3290000.tar.gz

tar -xzvf sqlite-autoconf-3290000.tar.gz 

rm sqlite-autoconf-3290000.tar.gz 

cd sqlite-autoconf-3290000

 ./configure -help | grep "prefix"

 ./configure --prefix=/usr/local

 make && make install

 sqlite3 version

 find /usr/ -name sqlite3

 mv /usr/bin/sqlite3 /usr/bin/sqlite3_default

 ln -s /usr/local/bin/sqlite3   /usr/bin/sqlite3

 sqlite3 version

 vi ~/.bashrc

 export LD_LIBRARY_PATH="/usr/local/lib"
 