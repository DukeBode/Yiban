import sys
from time import strftime,localtime,time
from yiban import *
import config

# 话题评论
def replys():
    article = Article()
    article.replys(EXCEL=config.xlsx)

# 话题内容
def content():
    article= Article()
    print(article.content['article']['content'])

# 获取微社区表头
def heads():
    school = Forum(config.channel_id,config.puid,config.group_id,recreate=False)
    head=school.head
    for line in head:
        print(line,':')
        print('    ',head[line])

# 获取微社区数据
def articles():
    school = Forum(config.channel_id,config.puid,config.group_id)
    school.getArticles(sys.argv[-1],size=config.size)

# SQL 查询
def sql():
    school = Forum(config.channel_id,config.puid,config.group_id,recreate=False)
    now = strftime('%H-%M-%S',localtime(time()))
    nth = 0
    while True:
        try:
            nth += 1
            val = input(f'{now} SQL {nth}> ')
            i = 0
        except KeyboardInterrupt:
            print('\n结束查询,程序退出。')
            exit()
        data = school.sql(val,f'-{now}-{nth}',config.sql_xlsx)
        for line in data:   
            i+=1
            print(i,end='')
            for item in line:
                print('$',item,end='')
            print()

# SQL 查询示例
def demo():
    print('''
    24小时之前十月发帖
        * FROM articles where createtime like "10-%" ORDER BY clicks*1 DESC
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
# 清理非程序文件
def clean():Yiban.clean('xlsx')

def count():
    school = Forum(config.channel_id,config.puid,config.group_id,recreate=False)
    values = config.count_item
    data=[('归属方','发帖数量')]
    for item in values:
        num = 0
        for val in values[item]:
            if config.content:
                sql = f'count(*) FROM articles WHERE title LIKE "%{val}%" OR content LIKE "%{val}%"'
            else:
                sql = f'count(*) from articles where title like "%{val}%"'
            num += school.sql(sql)[0][0]
        data.append((item,num))
    if data is not []:
        Yiban.excel(strftime('count-%H-%M-%S.xlsx',localtime(time())),data)

# 帮助字典
help = {
    'replys':replys,
    'content':content,
    'heads':heads,
    'articles':articles,
    'sql':sql,
    'count':count,
    'demo':demo,
    'clean':clean
}

if __name__=='__main__':
    val = sys.argv
    val = val[1] if len(val)>1 else ''
    if val in help:
        data = help.get(val)
        data()
    else:
        print('参数',val,'不存在！！！')
        print('可用参数：',tuple(help.keys()))