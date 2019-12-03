import sys,os,re
from time import strftime,localtime,time
from urllib import request, parse, error
import openpyxl, sqlite3, json
# import ssl

class Yiban:
    # # 格式化文件名
    # @classmethod
    # def filename(cls,name):
    #     symbols=tuple('\/:*?"<>|')
    #     for symbol in symbols:
    #         name = name.replace(symbol,'')
    #     return name
    
    # # 删除文件，参数名为后缀名
    # @classmethod
    # def clean(cls,*format):
    #     for file in os.listdir(os.getcwd()):
    #         if file[file.rfind('.')+1:] in format:
    #             os.remove(file)
    #             print(f'已删除文件 {file}')

    # excel格式存储
    # data 二维数据
    @classmethod
    def excel(cls,filename,data):
        if os.path.isfile(filename):
            os.remove(filename)
        wb = openpyxl.Workbook()
        ws = wb.active
        for item in data:
            print(item)
            ws.append(item)
        wb.save(filename)

    # # 保存文件内容
    # @classmethod
    # def filesave(cls,title,content):
    #     with open(f"{cls.filename(title)}.html", "w") as f:
    #         f.write(content)

    # # 读取文件内容
    # @classmethod
    # def fileread(cls,title):
    #     with open(title, 'r') as f:
    #         return f.readlines()

    # ssl._create_default_https_context = ssl._create_unverified_context

    # post 获取数据
    @classmethod
    def postUrl(cls,url,data):
        try:
            params = parse.urlencode(data).encode("utf-8")
            response = request.urlopen(url,data=params)
            content = json.loads(response.read().decode("utf-8"))
            return content['data']
        except error.URLError:
            print("系统已退出，请确认网络连接正常！！！")
        except KeyError:
            print('数据异常！！！')
        exit()
            

    # 获取链接中的参数
    @classmethod
    def param(cls,url):
        param=re.finditer('[^/]+/\d+',url)
        data=dict()
        for item in param:
            content=item.group().split('/')
            data[content[0]]=content[1]
        return data
    
# # 数据库
# class Database:
#     def __init__(self,filename='yiban',recreate=True):
#         t=strftime('%d',localtime(time()))
#         self.db_name=f"{filename}{t}.db"
#         if os.path.isfile(self.db_name) and recreate==True:
#             os.remove(self.db_name)
#         self.item={}
    
#     # 执行 SQL
#     def __sql(self,db_name,sqls):
#         content=[]
#         db = sqlite3.connect(db_name)
#         c = db.cursor()
#         for sql in sqls:
#             content = c.execute(sql).fetchall()
#         db.commit()
#         db.close()
#         return content
    
#     # 创建表
#     def create(self,table,item):
#         self.__sql(self.db_name,[f'''create table {table}{item}'''])
#         self.item[table]=item
    
#     # 插入数据
#     def insert(self,table,data):
#         str=[]
#         for val in data:
#             str.append(f'''INSERT INTO {table} {self.item[table]} VALUES {val}''')
#         self.__sql(self.db_name,str)

#     # 数据查询
#     def select(self,data):
#         return self.__sql(self.db_name,[f'''SELECT {data}'''])

# 微社区
class Forum:
    def __init__(self,forum,DATABASE=True,recreate=True):
        self.config(forum)     
        self.canWrite = False
        self.db = None
        if DATABASE:
            self.canWrite=recreate
            # 创建数据库
            self.db = Database(recreate=recreate)
        # 初始化 heads 数据
        self.__head()
    
    # 初始化配置
    def config(self,forum):
        post_data=Yiban.param(forum)
        if 'group_id' not in post_data:
            if 'id' in post_data:
                post_data['puid']=post_data['id']
                del post_data['id']
            post_data['group_id']=0
        data = Yiban.postUrl('http://www.yiban.cn/forum/api/getListAjax',post_data)
        post_data['channel_id'] = data['channel_id']
        self.post = dict(
            channel_id=post_data['channel_id'], 
            group_id=post_data['group_id'], 
            my=0, 
            need_notice=0, 
            orderby='updateTime', 
            page=1, 
            puid=post_data['puid'], 
            Sections_id=-1
        )

    @property
    def __tmp(self):
        data=Yiban.postUrl('https://www.yiban.cn/forum/article/listAjax', self.post)
        return data['list']
    
    def __create(self,title,dict):
        if self.db and self.canWrite:
            self.db.create(title,str(tuple(dict)).replace('\'','').replace('-',''))

    # 建立二级 head
    def __head(self):
        self.heads={}
        self.post['page'] = self.post['size'] = 1
        data = self.__tmp[0]
        for title in data:
            value=data[title]
            if isinstance(value,(str,int,float,bool)):
                continue
            elif isinstance(value,(tuple,list)):
                self.heads[title] = 'list'
                self.__create(title,['id',title])
            elif isinstance(value,dict):
                self.heads[title] = tuple(value)
                self.__create(title,value)
        self.heads['data'] = tuple(data)
        self.__create("articles",data)
    
    # SQL 查询
    def sql(self,key,nth=None,EXCEL=False):
        try:
            data = self.db.select(key)
            if not EXCEL:return data
            Yiban.excel(f"Forum-data{nth}.xlsx",data)
        except:
            print('输入错误！！！')
        return []

    # 发帖日期比较
    def compareDay(self,update,start):
        year = strftime('%Y-',localtime(time()))
        update = year+update[:5] if update[2]=='-' else update[:10]
        print(update)
        return update < start

    # 字符串去布尔值
    def replace(self,val):
        return re.sub(r'([a-zA-Z]+),','\'\\1\',',str(tuple(val)))

    # 插入数据封装
    def __insert(self,sqls):
        for sql in sqls:
            if self.db and self.canWrite:
                self.db.insert(sql,set(sqls[sql]))
    
    # 获取帖子内容
    def getArticles(self,firstDay=strftime('%Y-%m-%d',localtime(time())),size=20):
        print(firstDay)
        while True:
            self.post['size'] = size
            data = self.__tmp
            sqls={}
            for item in data:
                for key in self.heads:
                    if key=='data':continue
                    elif self.heads[key]=='list':
                        # 存储子数组
                        for val in item[key]:
                            sqls.setdefault(key, [])
                            sqls[key].append(self.replace([item['id'],val]))
                        item[key] = 'DBlist'
                    else:
                        # 存储子字典
                        if self.sql(f'''id FROM author WHERE id="{item[key]['id']}"''')==[]:
                            sqls.setdefault(key, [])
                            sqls[key].append(self.replace(item[key].values()))
                        item[key] = 'DBdict'
                # 存储字典
                sqls.setdefault('articles', [])
                sqls['articles'].append(self.replace(item.values()))
            self.__insert(sqls)
            if self.compareDay(data[-1]['updateTime'],firstDay):
                break
            self.post['page'] += 1
            self.post['lastId'] = data[-1]['aid']

# 话题
class Article:
    def __init__(self,data=sys.argv[-1]):
        self.post=Yiban.param(data)
        if len(self.post) == 0:
            raise AttributeError    
    
    # 内容
    @property
    def content(self):
        data=self.post
        data['origin']=0
        if 'groupid' in data:del data['group_id']
        return Yiban.postUrl("http://www.yiban.cn/forum/article/showAjax",data)
    
    # 评论
    def replys(self,EXCEL=False):
        data=self.post
        data['page']=data['order']=1
        data['size']=self.content['article']['replyCount']
        msg=Yiban.postUrl("http://www.yiban.cn/forum/reply/listAjax",data)
        replys=msg['list']
        data=list()
        try:
            data.append(tuple(replys['0'].keys()))
            for line in replys:
                M=replys[line]
                M['user']=M['user']['name']
                M['list']=""
                data.append(tuple(M.values()))
        except Exception as error:
            if EXCEL:
                t=strftime('%H%M%S',localtime(time()))
                Yiban.excel(f"reply{t}.xlsx",data)
            else:
                for item in data:print(item)
            exit()


if __name__=='__main__':
    print('请使用edata')
    exit()
