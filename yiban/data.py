from .base import Net,Database,File
from time import strftime,localtime,time
import re,sys

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
        post_data=Net.param(forum)
        if 'group_id' not in post_data:
            if 'id' in post_data:
                post_data['puid']=post_data['id']
                del post_data['id']
            post_data['group_id']=0
        data = Net.postUrl('http://www.yiban.cn/forum/api/getListAjax',post_data)
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
        data=Net.postUrl('https://www.yiban.cn/forum/article/listAjax', self.post)
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
            File.save_excel(f"Forum-data{nth}.xlsx",data)
        except:
            print('输入错误！！！')
        return []

    def compareDay(self,update,start):
        '''
        @description:
            发帖日期比较 
        @param 
            update: 更新日期
            start: 开始日期
        @return: 
        '''
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
    '''
    @description: 
        易班微社区话题
    '''
    def __init__(self,article_url=sys.argv[-1]):
        self.post=Net.param(article_url)
        if len(self.post) == 0:
            raise AttributeError    
    
    # 内容
    @property
    def content(self):
        try:
            url = URL.LOGIN_CAPTCHA
        except:
            url = 'http://www.yiban.cn/forum/article/showAjax'
        data=self.post
        data['origin']=0
        if 'groupid' in data:del data['group_id']
        return Net.postUrl(url,data)
    
    # 评论
    def replys(self,EXCEL=False):
        try:
            url = URL.LOGIN_CAPTCHA
        except:
            url = 'http://www.yiban.cn/forum/reply/listAjax'
        data=self.post
        data['page']=data['order']=1
        data['size']=self.content['article']['replyCount']
        msg=Net.postUrl(url,data)
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
                File.save_excel(f"reply{t}.xlsx",data)
            else:
                for item in data:print(item)
            exit()

class Reply:
    pass