import os
import json
import requests
import sqlite3
# from openpyxl import Workbook
# from openpyxl.utils import get_column_letter


class MicroCommunity:
    def __init__(self):
        self.article_url = 'http://www.yiban.cn/forum/article/listAjax'
        self.post = dict(channel_id=55461, group_id=0, my=0, need_notice=0, orderby='updateTime', page=1, puid=5189448,
                         Sections_id=-1, size=200)
        self.del_content = ['Channel_id', 'User_id', 'isNotice', 'isLocked', 'isWeb', 'replyTime', 'updateTime',
                            'status', 'UserGroup_id', 'oldArtId', 'oldAreaId', 'content', 'files_count',
                            'Sections_name', 'aid', 'images', 'editPermission', 'delPermission', 'sections_title'
                            ]
        self.num = 1
        self.file = 'MicroCommunity'
        self.item = tuple(self.delete(self.content()[0]))

    def content(self):
        url = requests.post(self.article_url, data=self.post)
        state = url.status_code
        if state == 200:
            url_content = url.json()  # web_content = url.text.encode('utf-8').decode('unicode_escape')
            # content = url_content['data']['list']
            return url_content['data']['list']

    def delete(self, item):
        for key in self.del_content:
            del item[key]
        return item


    def save(self, time='02',table='table0'):
        item = str(self.item).replace('\'', '')
        db_name = self.file+'.db'
        if os.path.isfile(db_name):
            os.remove(db_name)
        db = sqlite3.connect(db_name)
        c = db.cursor()
        c.execute(f'''create table {table}{item}''')
        state = 1
        while state:
            for line in self.content():
                # print(line['createTime'])
                # print(line)
                if line['updateTime'][:3] == time+'-':
                    # \or line_content['createTime'][5:7] == time:
                    state = 0
                    break
                line_content = self.delete(line)
                line_content['author'] = line_content['author']['name']
                data = str(tuple(line_content.values()))
                c.execute(f'INSERT INTO {table} {item} VALUES {data}')
                print(data)
            self.post['page'] += 1
        db.commit()
        db.close()

    def json_save(self, content, file_name='json'):
        file = open(f'{file_name}.json', mode='w', encoding='utf-8')
        json.dump(content, file, indent=4)
        file.close()

    def top(self, key, num, table='table0'):
        data = []
        db = sqlite3.connect(self.file + '.db')
        c = db.cursor()
        content = c.execute(f'SELECT * FROM {table}')
        row = self.item[key]
        for line in content:
            number = len(data)
            if number > num:
                data = data[:num]
            data.append(dict(zip(self.item, line)))
            while number > 1:
                number -= 1
                if int(data[number-1][row]) < int(data[number][row]):
                    data[number-1], data[number] = data[number], data[number-1]
        self.json_save(data, file_name=row)
        for show in data:
            print(show)
            # print(show.values())
            # print(show['title']+'\t'+show['createTime']+'\t'+show['clicks']+'\t'+show['url'])
        db.commit()
        db.close()

    def top_name(self, table='table0'):
        # 从数据库获取数据
        db = sqlite3.connect(self.file + '.db')
        c = db.cursor()
        content = c.execute(f'SELECT * FROM {table}')
        dict = {}
        for line in content:
            dict.setdefault(line[7], 0)
            dict[line[7]] += 1
        list = sorted(dict.items(), key=lambda x: x[1], reverse=True)
        k = 0
        for item in list:
            k += 1
            print(k, end='\t')
            print(item[0], end='\t')
            print(dict[item[0]])
        db.commit()
        db.close()

    # 点击排行
    def top_clicks(self, num=5): self.top(4, num)

    def top_average_clicks(self, table='table0'):
        # 从数据库获取数据
        db = sqlite3.connect(self.file + '.db')
        c = db.cursor()
        content = c.execute(f'SELECT * FROM {table}')
        dict = {}
        clicks={}
        for line in content:
            dict.setdefault(line[7], 0)
            dict[line[7]] += 1
            clicks.setdefault(line[7], 0)
            clicks[line[7]] += int(line[4])
        for item in dict:
            dict[item] = clicks[item]/dict[item]
        list = sorted(dict.items(), key=lambda x: x[1], reverse=True)
        k = 0
        for item in list:
            k += 1
            print(k, end='\t')
            print(item[0], end='\t')
            print(int(dict[item[0]]))
        db.commit()
        db.close()

    # 回复排行
    def top_reply_count(self, num=5): self.top(2, num)

    # 点赞排行榜
    def top_up_count(self, num=5): self.top(5, num)

    # def xlsx(self, content):
    #     content_book = Workbook()
    #     content_sheet = content_book.active
    #     i = 1
    #     for line in range(len(content)):
    #         line_content = content[line]
    #     for item in line_content:
    #         key = get_column_letter(i) + str(line + 1)
    #         content_sheet[key] = line_content[item]
    #         i += 1
    #     content_book.save('abcd.xlsx')


def show():
    print('输入统计时间段：')


if __name__ == '__main__':
    lut = MicroCommunity()
    # lut.save()

    # lut.top_clicks(100)
    # lut.top_reply_count()
    # lut.top_up_count()
    # lut.top_name()
    # lut.top_average_clicks()
