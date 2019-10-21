from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponse
from django.contrib import auth
from .openapi import Yiban
from .models import User

def back(request):
    # print(User.objects.filter(userid='hell').exists())
    # print(request.session.keys())
    # request.COOKIES['hello']=123
    # print(request.COOKIES)
    # print(request.GET.keys()) 
    response = HttpResponse('正在维护 <a class="nav-link" href="/">返回首页</a>')
    if 'code' in request.GET:
        oauth=Oauth()
        data = oauth.get_access_token(request.GET["code"])
        if 'userid' in data:
            user = User.objects.get_or_create(userid=data['userid'])[0]
            user.access_token = data['access_token']
            user.expires = data['expires']
            data = Yiban.get_user(data['access_token'])
            if data['status']=='success':
                data = data['info']
                user.username = data['yb_username']
                user.usernick = data['yb_usernick']
                user.sex = data['yb_sex']
                user.userhead = data['yb_userhead']
                user.schoolid = data['yb_schoolid']
                user.schoolname = data['yb_schoolname']
                response = HttpResponse(f'''
                    网薪：{data['yb_money']}
                    经验值：{data['yb_exp']}
                    <a class="nav-link" href="/">返回首页</a><br>
                ''')
            user.save()
            
            # user = auth.authenticate(userid=data['userid'])
            auth.login(request,user)
            # request.session['access_token']=p['access_token']
            # request.session['userid']=p['userid']
            # print(Yiban.letter(data['access_token'],data['access_token']))
            # print(Yiban.recommend_friend(data['access_token'],5))
            # print(Yiban.check_friend(data['access_token'],10690513))
            # print(Yiban.news(data['access_token']))
            # print(Yiban.sport_steps(data['access_token'],30))
        
        # response.set_cookie("code",request.GET["code"])
            
    return response
    # return render(request, 'oauth/back.html')

def index(request):
    print(request.user)
    return render(request, 'yiban/index.html')

def demo(request):
    print(request.META['HTTP_USER_AGENT'])
    return render(request, 'yiban/demo.html', {
        'username':request.user
    })

def login(request):
    return redirect(Yiban.login())

def logout(request):
    auth.logout(request)
    return redirect('/')
