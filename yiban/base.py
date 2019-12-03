from urllib import request, parse, error
from time import strftime,localtime,time
from os import listdir,getcwd,remove
import sqlite3
import json
import ssl

class Net:
    ssl._create_default_https_context = ssl._create_unverified_context

    @classmethod
    # POST 方法封装
    def POST_json(cls,url,data):
        params = parse.urlencode(data).encode("utf-8")
        response = request.urlopen(url,data=params)
        return json.loads(response.read().decode("utf-8"))

    @classmethod
    # GET 方法封装
    def GET_json(cls,url,data):
        string = f'{url}?{parse.urlencode(data)}'
        response = request.urlopen(string)
        return json.loads(response.read())

class File:
    # 格式化文件名
    @classmethod
    def filename(cls,name):
        symbols=tuple(r'\/:*?"<>|')
        for symbol in symbols:
            name = name.replace(symbol,'')
        return name
    
    # 删除文件，参数名为后缀名
    @classmethod
    def clean(cls,*format):
        for file in listdir(getcwd()):
            if file[file.rfind('.')+1:] in format:
                remove(file)
                print(f'已删除文件 {file}')

    # 保存文件内容
    @classmethod
    def filesave(cls,title,content):
        with open(f"{cls.filename(title)}.html", "w") as f:
            f.write(content)

    # 读取文件内容
    @classmethod
    def fileread(cls,title):
        with open(title, 'r') as f:
            return f.readlines()

# 数据库
class Database:
    def __init__(self,filename='yiban',recreate=True):
        t=strftime('%d',localtime(time()))
        self.db_name=f"{filename}{t}.db"
        from os.path import isfile
        if isfile(self.db_name) and recreate==True:
            remove(self.db_name)
        del isfile
        self.item={}
    
    # 执行 SQL
    def __sql(self,db_name,sqls):
        content=[]
        db = sqlite3.connect(db_name)
        c = db.cursor()
        for sql in sqls:
            content = c.execute(sql).fetchall()
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