import requests
import sys
import re
import datetime
import openpyxl

def excel(filename,data):
    wb = openpyxl.Workbook()
    ws = wb.active
    for item in data:
        ws.append(item)
    wb.save(filename)


def show(url,post):
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
        return web.json()['data']

if __name__=='__main__':
    param=re.finditer('[^/]+/[0-9]+',sys.argv[-1])
    data=dict()
    for item in param:
        content=item.group().split('/')
        data[content[0]]=content[1]
    del data['group_id']
    showAjax = "http://www.yiban.cn/forum/article/showAjax"
    data['origin']=0
    print(data)
    data['size']=show(showAjax,data)['article']['replyCount']
    del data['origin']
    listAjax = "http://www.yiban.cn/forum/reply/listAjax"
    data['page']=data['order']=1
    replys=show(listAjax,data)['list']
    data=list()
    try:
        data.append(tuple(replys['0'].keys()))
        for line in replys:
            M=replys[line]
            M['user']=M['user']['name']
            M['list']=""
            data.append(tuple(M.values()))
    except Exception as error:
        for item in data:
            print(item)
        t=datetime.datetime.now().strftime("%H%M%S")
        excel(f"reply{t}.xlsx",data)
        exit()