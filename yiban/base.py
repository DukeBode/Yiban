from urllib import request, parse, error
from time import strftime,localtime,time
from os import listdir,getcwd,remove
from os.path import isfile
import sqlite3
import json
import ssl
import re

class Net:
    ssl._create_default_https_context = ssl._create_unverified_context
    
    @classmethod
    def param(cls,url):
        '''
        @description:
            获取 GET 链接中的参数 
        @param 
            url: GET 链接
        @return: 
        '''
        param=re.finditer(r'[^/]+/\d+',url)
        data=dict()
        for item in param:
            content=item.group().split('/')
            data[content[0]]=content[1]
        return data
    
    @classmethod
    def params_by_GET(cls,url):
        result = parse.urlparse(url)
        return parse.parse_qs(result.query,True)

    @classmethod
    def POST_json(cls,url,data):
        '''
        @description: 
            POST 方法获取 json 数据
        @param
            url: POST 地址
            data: POST 数据
        @return: 
        '''
        try:
            params = parse.urlencode(data).encode("utf-8")
            response = request.urlopen(url,data=params)
            return json.loads(response.read().decode("utf-8"))
        except error.URLError:
            print("系统已退出，请确认网络连接正常！！！")
            return {}

    @classmethod
    # GET 方法封装
    def GET_json(cls,url,data):
        string = f'{url}?{parse.urlencode(data)}'
        response = request.urlopen(string)
        return json.loads(response.read())
    
    # post 获取数据
    @classmethod
    def postUrl(cls,url,data):
        try:
            return cls.POST_json(url,data)['data']
        except KeyError:
            print('数据异常！！！')
        exit()

class File:
    # 格式化文件名
    @classmethod
    def format_name(cls,name):
        symbols=tuple(r'\/:*?"<>|')
        for symbol in symbols:
            name = name.replace(symbol,'')
        return name
    
    @classmethod
    def clean(cls,*format):
        '''
        @description: 
            删除指定后缀的文件
        @param
            format: 后缀名
        @return: 
        '''
        for file in listdir(getcwd()):
            if file[file.rfind('.')+1:] in format:
                remove(file)
                print(f'已删除文件 {file}')

    # 保存文件内容
    @classmethod
    def save(cls,title,content):
        with open(f"{cls.format_name(title)}.html", "w") as f:
            f.write(content)
    
    # excel格式存储
    # data 二维数据
    @classmethod
    def save_excel(cls,filename,data):
        from openpyxl import Workbook
        if isfile(filename):
            remove(filename)
        wb = Workbook()
        ws = wb.active
        for item in data:
            print(item)
            ws.append(item)
        wb.save(filename)

    # 读取文件内容
    @classmethod
    def read(cls,title):
        with open(title, 'r') as f:
            return f.readlines()

# 数据库
class Database:
    def __init__(self,filename='yiban',recreate=True):
        t=strftime('%d',localtime(time()))
        self.db_name=f"{filename}{t}.db"
        if isfile(self.db_name) and recreate==True:
            remove(self.db_name)
        self.item={}
    
    # 执行 SQL
    def __sql(self,db_name,sqls):
        content=[]
        db = sqlite3.connect(db_name)
        c = db.cursor()
        for sql in sqls:
            try:
                content = c.execute(sql).fetchall()
            except:
                continue
        db.commit()
        db.close()
        return content
    
    # 创建表
    def create(self,table,item):
        self.__sql(self.db_name,[f'''create table {table}{item}'''])
        self.item[table]=item
    
    # 插入数据
    def insert(self,table,data):
        str=[]
        for val in data:
            str.append(f'''INSERT INTO {table} {self.item[table]} VALUES {val}''')
        self.__sql(self.db_name,str)

    # 数据查询
    def select(self,data):
        return self.__sql(self.db_name,[f'''SELECT {data}'''])