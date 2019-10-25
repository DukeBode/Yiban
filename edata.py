import sys,config
from yiban import *

# 话题评论
def replys():Article().replys(EXCEL=config.xlsx)

# 话题内容
def content():
    article = Article().content['article']
    id,title = article['id'],article['title']
    Yiban.filesave(f'{id}{title}',article['content'])
    print(f'请在当前目录，点击 {id}{title}.html 文件阅读内容。')

# 获取微社区表头
def heads():
    head = Forum(config.forum,recreate=False).sql('sql from sqlite_master')
    for line in head:
        print(line[0].replace('CREATE TABLE ','\n表：').replace('(','\n列：('))

# 获取微社区数据
def articles():Forum(config.forum).getArticles(sys.argv[-1],size=config.size)

# SQL 查询
def sql():
    school = Forum(config.forum,recreate=False)
    now = school.sql("time('now', 'localtime')")[0][0].replace(':','-')
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
    查询所有发帖及作者信息
        articles.*,author.* from articles,author where articles.user_id=author.id  
    24小时之前十月发帖
        * FROM articles where createtime GLOB "10-*" ORDER BY clicks*1 DESC
    # 关键词统计
        * FROM articles WHERE title GLOB "*易流技术*" OR content GLOB "*易流技术*" ORDER BY clicks*1 DESC
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
def clean():Yiban.clean(*config.del_file)

def count():
    school = Forum(config.forum,recreate=False)
    values = config.count_item
    data=[('归属方','发帖数量')]
    for item in values:
        num = 0
        for val in values[item]:
            if config.content:
                sql = f'count(*) FROM articles WHERE title GLOB "*{val}*" OR content GLOB "*{val}*"'
            else:
                sql = f'count(*) from articles where title GLOB "*{val}*"'
            num += school.sql(sql)[0][0]
        data.append((item,num))
    if data is not []:
        now = school.sql("time('now', 'localtime')")[0][0].replace(':','-')
        Yiban.excel(f'count-{now}.xlsx',data)

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
    param = sys.argv
    param = param[1] if len(param)>1 else ''
    try:
        help.get(param.lower())()
    except TypeError:
        print('参数',param,'不存在！！！')
        print('可用参数：',tuple(help.keys()))
        