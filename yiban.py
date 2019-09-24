import sys,os,re
from time import strftime,localtime,time
import openpyxl,sqlite3
import requests

class Yiban:

    # excel格式存储
    # data 二维数据
    @classmethod
    def excel(cls,filename,data):
        wb = openpyxl.Workbook()
        ws = wb.active
        for item in data:
            print(item)
            ws.append(item)
            wb.save(filename)

    # post 获取数据
    @classmethod
    def postUrl(cls,url,post):
        try:
            web = requests.post(url, data=post)
            state = web.status_code
        except Exception as error:
            print("系统已退出，请确认网络连接正常！！！")
            exit()
        else:
            if state!=200:
                print("数据异常！！！")
                exit()
            return web

    # 获取链接中的参数
    # url 默认为最后一个参数
    @classmethod
    def param(cls,url=sys.argv[-1]):
        param=re.finditer('[^/]+/[0-9]+',url)
        data=dict()
        for item in param:
            content=item.group().split('/')
            data[content[0]]=content[1]
        return data
    
# 数据库
class Database:
    def __init__(self,filename='yiban'):
        t=strftime('%d%H%M%S',localtime(time()))
        # t=datetime.datetime.now().strftime("%H%M%S")
        self.db_name=f"{filename}{t}.db"
        if os.path.isfile(self.db_name):os.remove(self.db_name)
        self.item={}
    
    def __sql(self,db_name,sql):
        content=[]
        db = sqlite3.connect(db_name)
        c = db.cursor()
        content = c.execute(sql).fetchall()
        db.commit()
        db.close()
        return content
    
    # 创建表
    def create(self,table,item):
        self.__sql(self.db_name,f'''create table {table}{item}''')
        self.item[table]=item
    
    # 插入数据
    def insert(self,table,data):
        self.__sql(self.db_name,f'''INSERT INTO {table} {self.item[table]} VALUES {data}''')

    # 数据查询
    def select(self,data):
        return self.__sql(self.db_name,f'''SELECT {data}''')

# 微社区
class Forum:
    def __init__(self,puid=5189448,DATABASE=True):
        self.post = dict(channel_id=55461, group_id=0, my=0, need_notice=0, 
        orderby='updateTime', page=1, puid=puid, Sections_id=-1)
        # 创建数据库
        self.db = Database() if DATABASE else None
        # 初始化 heads 数据
        self.__head()

    @property
    def __tmp(self):
        data=Yiban.postUrl('https://www.yiban.cn/forum/article/listAjax', self.post)
        return data.json()['data']['list']
    
    def __create(self,title,dict):
        if self.db:
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
    
    # 发帖日期比较
    def compareDay(self,update,start):
        year = strftime('%Y-',localtime(time()))
        # 月份比较
        if year + update[:3]==start[:8] or update[:8]==start[:8]:
            # 日期比较
            return int(update[3:5]) < int(start[8:])
        return False
    
    def __insert(self,title,value):
        value = str(tuple(value))
        value = value.replace('None','\'None\'')
        value = value.replace('True','\'True\'')
        value = value.replace('False','\'False\'')
        if self.db:self.db.insert(title,value)
        print(value)
    
    def getArticles(self,firstDay=strftime('%Y-%m-%d',localtime(time())),size=20):
        while True:
            self.post['size'] = size
            data = self.__tmp
            for item in data:
                for key in self.heads:
                    if key=='data':continue
                    elif self.heads[key]=='list':
                        for val in item[key]:
                            self.__insert(key,[item['id'],val])
                        item[key] = 'DBlist'
                    else:
                        if self.sql(f'''id FROM author WHERE id="{item[key]['id']}"''')==[]:
                        # f'id FROM author WHERE id="{item[key]['id']}"')==[]:
                            self.__insert(key,item[key].values())
                        item[key] = 'DBdict'
                self.__insert("articles",item.values())
            if self.compareDay(data[-1]['updateTime'],firstDay):
                break
            self.post['page']+=1
            self.post['lastId'] = data[-1]['aid']
    
    def sql(self,key):
        try:
            return self.db.select(key)
        except:
            print('输入错误！！！')
            return []

    # 关键词统计
    # * FROM articles WHERE title LIKE "%易流技术%" OR content LIKE "%易流技术%" ORDER BY clicks*1 DESC
    # 点击量排行
    # * FROM articles ORDER BY clicks*1 DESC LIMIT 100
    # 评论量排行
    # * FROM articles ORDER BY replyCount+0 DESC LIMIT 100
    # 点赞量排行
    # * FROM articles ORDER BY upCount*1 DESC LIMIT 100
    # 个人发帖情况
    # user_id,author.name,COUNT(user_id),SUM(clicks),SUM(upCount),SUM(replyCount) FROM articles,author WHERE author.id=user_id GROUP BY user_id ORDER BY COUNT(user_id) DESC

    # 用户发帖
    # * FROM articles WHERE user_id="29171346" ORDER BY clicks*1 DESC
    # 作者信息查询
    # DISTINCT * FROM author WHERE id="29171346"
    # 帖子图片
    # * from IMAGES WHERE ID="90723390"

# 话题
class Article:
    def __init__(self,data=Yiban.param()):
        self.post=data
    
    # 内容
    @property
    def content(self):
        data=self.post
        del data['group_id']
        data['origin']=0
        msg=Yiban.postUrl("http://www.yiban.cn/forum/article/showAjax",data)
        return msg.json()['data']
    
    # 评论
    def replys(self,EXCEL=False):
        data=self.post
        data['page']=data['order']=1
        data['size']=self.content['article']['replyCount']
        msg=Yiban.postUrl("http://www.yiban.cn/forum/reply/listAjax",data)
        replys=msg.json()['data']['list']
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
    lut = Forum(5189448)
    lut.getArticles()
    os.system("cls")
    print('''
    # 关键词统计
        * FROM articles WHERE title LIKE "%易流技术%" OR content LIKE "%易流技术%" ORDER BY clicks*1 DESC
    # 点击量排行
        * FROM articles ORDER BY clicks*1 DESC LIMIT 100
    # 评论量排行
        * FROM articles ORDER BY replyCount+0 DESC LIMIT 100
    # 点赞量排行
        * FROM articles ORDER BY upCount*1 DESC LIMIT 100
    # 个人发帖情况
        user_id,author.name,COUNT(user_id),SUM(clicks),SUM(upCount),SUM(replyCount) FROM articles,author WHERE author.id=user_id GROUP BY user_id ORDER BY COUNT(user_id) DESC

    # 用户发帖
        * FROM articles WHERE user_id="29171346" ORDER BY clicks*1 DESC
    # 作者信息查询
        DISTINCT * FROM author WHERE id="29171346"
    # 帖子图片
        * from IMAGES WHERE ID="90723390"
    ''')
    while True:
        i=1
        val=input("sql> ")
        for line in lut.sql(val):
            print(i,end='')
            for item in line:
                print('$',item,end='')

    # article= Article()
    # article.content
    # article.replys(EXCEL=True)
    # article.replys()

    # 日期出界需人工校验
    # 多关键词 dict.setdefault