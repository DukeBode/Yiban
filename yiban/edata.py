from yiban.data import Forum,Article
from yiban.base import File
from asyncio import run,sleep,create_task,gather
from random import random
from sys import argv

import importlib.util as imp
if imp.find_spec('config') is None:
    print('请配置config文件')
    exit()
del imp
import config

# 异步函数装饰器
def asyncio(function):
    if function.__name__ not in argv:
        return IndexError
    run(function())
    exit()

# 话题评论
def replys():Article().replys(EXCEL=config.xlsx)

# 话题内容
def content():
    article = Article().content['article']
    id,title = article['id'],article['title']
    File.save(f'{id}{title}',article['content'])
    print(f'请在当前目录，点击 {id}{title}.html 文件阅读内容。')

# 话题阅读
async def click(num,url):
    web=Article(url)
    for index in range(num):
        article = web.content['article']
        await sleep(config.delay_max*random())
        print(f"{index+1}：{article['title']}已阅读：{article['clicks']}次")

# 话题阅读
@asyncio
async def clicks():
    tasks=[]
    try:
        num = int(argv[2])
        tasks.append(create_task(click(num,argv[3])))
        await gather(*tasks, return_exceptions=False)
    except AttributeError:
        tasks=[]
        data = File.read(argv[3])
        for url in data:
            task = create_task(click(num,url))
            tasks.append(task)
        await gather(*tasks, return_exceptions=True)
    except IndexError:
        print('请确认参数完整')
    except ValueError:
        print('请输入阅读数量')

# 获取微社区表头
def heads():
    head = Forum(config.forum,recreate=False).sql('sql from sqlite_master')
    for line in head:
        print(line[0].replace('CREATE TABLE ','\n表：').replace('(','\n列：('))

# 获取微社区数据
def articles():Forum(config.forum).getArticles(argv[-1],size=config.size)

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
def clean():File.clean(*config.del_file)

# 数量统计
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
        File.save_excel(f'count-{now}.xlsx',data)

# def help(function,**argv):
#     item=helps.add_parser(function.__name__,help=argv['help'])
#     arguments = argv['arguments'] if 'arguments' in argv else None
#     for val in arguments:item.add_argument(val,help=arguments[val])
#     item.set_defaults(func=function)

if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='edata.py',description='Yiban Forum Data')
    helps = parser.add_subparsers(title='可选操作值',help='选择操作使用 -h 获取帮助') 

    help = helps.add_parser('clicks',help='阅读指定话题')
    help.add_argument('阅读次数',help='计划要阅读的次数')
    help.add_argument('话题链接',help='单篇话题链接或存储话题链接的文本文档地址')
    help.set_defaults(func=clicks)
    help = helps.add_parser('replys',help='统计话题评论')
    help.add_argument('话题链接',help='易班话题的链接')
    help.set_defaults(func=replys)
    help = helps.add_parser('content',help='获取话题内容')
    help.add_argument('话题链接',help='易班话题的链接')
    help.set_defaults(func=content)
    help = helps.add_parser('heads',help='查看微社区数据表表头').set_defaults(func=heads)
    help = helps.add_parser('articles',help='获取微社区数据')
    help.add_argument('时间',help='开始时间，格式 年-月-日')
    help.set_defaults(func=articles)
    help = helps.add_parser('count',help='统计各归属方发帖数量').set_defaults(func=count)
    help = helps.add_parser('demo',help='常用查询语句示例').set_defaults(func=demo)
    help = helps.add_parser('sql',help='使用 SQL 语句查询发帖情况').set_defaults(func=sql)
    help = helps.add_parser('clean',help=f'清理{config.del_file}文件').set_defaults(func=clean)
    args = parser.parse_args()
    if 'func' not in args:
        print('请输入值！！！')
        exit()
    args.func()
