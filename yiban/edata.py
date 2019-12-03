from yiban.data import Forum,Article
from yiban.base import File
from asyncio import run,sleep,create_task,gather
from random import random
from sys import argv
# from yiban import config

class Config:
    # 微社区的网址
    # forum='易班群主页网址'
    # forum='易班校方主页网址'
    # forum='易班微社区主页网址'
    # forum='http://www.yiban.cn/school/index/id/5000089'
    forum='http://www.yiban.cn/Org/orglistShow/puid/18396296/group_id/411965/type/forum'
    # 每次获取数量
    size=500
    # 批删除的文件后缀
    del_file='xlsx','html','要删除的文件后缀'
    # 启用 Excel 保存评论
    xlsx=True
    # 启用 Excel 保存查询数据
    sql_xlsx=True
    # 需计数关键词,同一归属方的关键词数会叠加
    # 格式 '归属方'：['查找关键词1','查找关键词n',],
    count_item={
        '易班技术部':['易流技术','易流'],
        '易班编辑部':['易流技'],
        '材料学院':['魅力材料'],
        '电信学院':['尚学电信'],
        '法学院':['青春法学'],
        '机电学院':['明德机电'],
        '经管学院':['韶华经管'],
        '计通学院':['计通学院'],
        '理学院':['精进理学'],
        '能动学院':['风华能动'],
        '石化学院':['多彩石化'],
        '设计学院':['至美设计'],
        '生命学院':['炫彩生命'],
        '土木学院':['菁华土木'],
        '外语学院':['励志外院'],
        '新能源学院':['新韵能源'],
        '软件学院':['慎微软件'],
    }
    # 启用内容关键词检索
    content=False
    # 浏览量最大间隔秒数,可为小数
    delay_max=100
    # 保存各归属方数据（未实现）
    # data=True
    # 屏蔽帖（未实现）
    # status=1

# 异步函数装饰器
def asyncio(function):
    if function.__name__ not in argv:
        return IndexError
    run(function())
    exit()

# 话题评论
def replys():Article().replys(EXCEL=Config.xlsx)

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
        await sleep(Config.delay_max*random())
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
    head = Forum(Config.forum,recreate=False).sql('sql from sqlite_master')
    for line in head:
        print(line[0].replace('CREATE TABLE ','\n表：').replace('(','\n列：('))

# 获取微社区数据
def articles():Forum(Config.forum).getArticles(argv[-1],size=Config.size)

# SQL 查询
def sql():
    school = Forum(Config.forum,recreate=False)
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
        data = school.sql(val,f'-{now}-{nth}',Config.sql_xlsx)
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
def clean():File.clean(*Config.del_file)

# 数量统计
def count():
    school = Forum(Config.forum,recreate=False)
    values = Config.count_item
    data=[('归属方','发帖数量')]
    for item in values:
        num = 0
        for val in values[item]:
            if Config.content:
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

    help = helps.add_parser('clicks',help='阅读指定话题').set_defaults(func=clicks)
    help = helps.add_parser('replys',help='统计话题评论').set_defaults(func=replys)
    help = helps.add_parser('content',help='获取话题内容').set_defaults(func=content)
    help = helps.add_parser('heads',help='查看微社区数据表表头').set_defaults(func=heads)
    help = helps.add_parser('articles',help='获取微社区数据')
    help.add_argument('date',help='时间')
    help.set_defaults(func=articles)
    help = helps.add_parser('count',help='统计各归属方发帖数量').set_defaults(func=count)
    help = helps.add_parser('demo',help='常用查询语句示例').set_defaults(func=demo)
    help = helps.add_parser('sql',help='使用 SQL 语句查询发帖情况').set_defaults(func=sql)
    help = helps.add_parser('clean',help=f'清理{Config.del_file}文件').set_defaults(func=clean)
    args = parser.parse_args()
    try:
        args.func()
    except AttributeError:
        print("请输入值")
