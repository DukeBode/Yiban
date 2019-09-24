# 统计易班微社区数据
import os
import requests
import sqlite3

class MicroCommunity:
    def __init__(self):
        self.article_url = 'https://www.yiban.cn/forum/article/listAjax'
        self.post = dict(channel_id=55461, group_id=0, my=0, need_notice=0, orderby='updateTime', page=1, puid=5189448,
                         Sections_id=-1, size=1)
        self.del_content = ['Channel_id', 'User_id', 'isNotice', 'isWeb', 'replyTime', 'updateTime',
                             'UserGroup_id', 'oldArtId', 'oldAreaId', 'content', 'files_count',
                            'Sections_name', 'aid', 'images', 'editPermission', 'delPermission', 'sections_title'
                            ]
        #, 'isLocked''status',
        self.c_name = ['新韵能源','魅力材料','明德机电','菁华土木','尚学电信','慎微软件','风华能动','炫彩生命','精进理学','计通新闻','计通学院','青春法学','励志外院','韶华经管','至美设计','多彩石化','石小易']
        self.num = 1
        self.file = 'MicroCommunity'
        self.item = tuple(self.delete(self.content()[0]))
    
    # 获取话题列表
    def content(self,SHOW=False):
        try:
            web = requests.post(self.article_url, data=self.post)
            state = web.status_code
        except Exception as error:
            print("系统已退出，请确认网络连接正常！！！")
            exit()
        else:
            if state!=200:
                print("数据异常！！！")
                exit()
            content = web.json() 
            if SHOW:print(content['data']['list'][0].keys())
            return content['data']['list']

    def delete(self, item):
        for key in self.del_content:
            del item[key]
        return item

    def save(self, time='02',table='table0'):
        item = str(self.item).replace('\'', '')
        db_name = self.file+'.db'
        if os.path.isfile(db_name):os.remove(db_name)
        db = sqlite3.connect(db_name)
        c = db.cursor()
        c.execute(f'''create table {table}{item}''')
        self.post['size']=200
        state = 1
        while state:
            for line in self.content():
                self.post['lastId']=line['aid']
                if line['updateTime'][:3] == time+'-' or line['updateTime'][5:7] == time:
                    state = 0
                    break
                # print(line['createTime'])
                line_content = self.delete(line)
                line_content['author'] = line_content['author']['name']
                # print(line_content.keys())
                data = str(tuple(line_content.values()))
                c.execute(f'INSERT INTO {table} {item} VALUES {data}')
                print(data)
            self.post['page'] += 1
        db.commit()
        db.close()

    # 标题关键词计数
    def count(self, table='table0',keyw='红柳易讯',mouth='04',group=True):
        if group:
            print("id,标题,,评论，更新日期，点击量，点赞量，未屏蔽，，作者，链接")
            print("'id', 'title', 'isLocked', 'replyCount', 'createTime', \
            'clicks', 'upCount', 'status', 'Sections_id', 'hotScore', 'kid', 'author', 'url'")
        db = sqlite3.connect(self.file + '.db')
        c = db.cursor()
        content = c.execute(f'SELECT * FROM {table} WHERE title LIKE "%{keyw}%"')
        dict = {}
        k=0
        for line in content:
            if line[4][:2] == mouth or line[4][5:7]==mouth:
                if line[7]=='1':
                    dict.setdefault(keyw, 0)#字典初始化
                    dict[keyw] += 1
                else:k=k+1
            if group:print(line)
        db.commit()
        db.close()
        return dict    

    # 排行
    def top(self, key, num, table='table0'):
        data = []
        db = sqlite3.connect(self.file + '.db')
        c = db.cursor()
        content = c.execute(f'SELECT id,title,createTime,{key},url FROM {table}')
        for line in content:
            data.append(line)
            number = len(data)
            while number > 1:
                number -= 1
                if int(data[number-1][3]) < int(data[number][3]):
                    data[number-1], data[number] = data[number], data[number-1]
            if number > num:data = data[:num]
        k=0
        num+=1
        for show in data:
            k+=1
            if k<num:print(f'{k}${show[0]}${show[1]}${show[2]}${show[3]}${show[4]}')
            else:break
        db.commit()
        db.close()

    def top_name(self, num=1000,table='table0'):
        # 从数据库获取数据
        db = sqlite3.connect(self.file + '.db')
        c = db.cursor()
        content = c.execute(f'''SELECT author,COUNT(author),SUM(clicks),SUM(upCount),SUM(replyCount) 
        FROM {table} GROUP BY author ORDER BY COUNT(author) DESC''')
        k = 0
        print(f'序号\t姓名\t发帖量\t点击量\t点赞量\t评论量')
        for line in content:
            k += 1
            if k>num:break
            print(f'{k}${line[0]}${line[1]}${int(line[2])}${int(line[3])}${int(line[4])}')
        db.commit()
        db.close()
        
    # 点击排行
    def top_clicks(self, num=5): self.top('clicks', num)
    # 回复排行
    def top_reply_count(self, num=5): self.top('replyCount', num)
    # 点赞排行榜
    def top_up_count(self, num=5): self.top('upCount', num)
    # 关键字统计
    def c_count(self,mouth0='04'):
        c_dict={}
        k=0
        for line in self.c_name:
            item=self.count(keyw=line, mouth=mouth0,group=False)
            c_dict[line]=item[line] if item else 0
        for c_line in c_dict.keys():
            k=k+1
            print(f'{k}${c_line}${c_dict[c_line]}')

if __name__ == '__main__':
    lut = MicroCommunity()
    # 月份减一，只首次运行
    # lut.save('04')
    # 点击量排行
    # lut.top_clicks(100)
    # 本月，关键词统计帖子
    # lut.count(keyw='易流技术')
    # 院发帖数量统计
    # lut.c_count(mouth0='05')
    # 回复
    # lut.top_reply_count(num=100)
    # 点赞
    # lut.top_up_count(num=100)
    # 个人发帖情况
    # lut.top_name(num=200)