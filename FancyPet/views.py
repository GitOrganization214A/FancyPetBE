from django.shortcuts import render
from django.http import JsonResponse
from .models import User, Article, PetSpace, Count
from django.views.decorators.csrf import csrf_exempt

import requests
import json
import os

host_name = 'http://43.143.139.4:8000/'


def PetSpaces(request):
    print(request)
    openid = request.GET.get('openid')
    print(openid)
    # 获取数据库中所有的PetSpace对象
    petspaces = PetSpace.objects.filter(openid=openid)
    data = []
    for petspace in petspaces:
        # 将每个PetSpace对象转换成字典
        data.append({
            'openid': petspace.openid,
            'PetSpaceID': petspace.PetSpaceID,
            'name': petspace.name,
            'breed': petspace.breed,
            'avatar': petspace.avatar,
        })
    print(data)
    return JsonResponse(data, safe=False)


@csrf_exempt
def changeAvatar(request):
    print(request)
    files = request.FILES
    content = files.get('avatar', None).read()
    openid = request.POST.get('openid')
    print(openid)
    with open('media/user/'+openid+'.png', 'wb') as f:
        f.write(content)
    user = User.objects.filter(openid=openid)
    if user:
        user = user[0]
        user.avatar = host_name+'media/user/'+openid+'.png'
        user.save()
    return JsonResponse({'status': 'success'})


def changeInfo(request):
    openid = request.GET.get('openid')
    nickname = request.GET.get('nickname')

    user = User.objects.filter(openid=openid)
    if user:
        user = user[0]
        user.nickname = nickname
        user.save()
    else:
        user = User.objects.create(
            openid=openid, nickname=nickname)
    return JsonResponse({'status': 'success'})


def login(request):
    code = request.GET.get('code')  # 从请求中获取code
    # 获取session_key和openid
    url = "https://api.weixin.qq.com/sns/jscode2session"  # 微信服务器的URL

    params = {
        "appid": "wx17396561c08eee6a",  # 你的微信AppID
        "secret": "1553b8c2bdf47f280ffeb61c989e0f50",  # 你的微信AppSecret
        "js_code": code,
        "grant_type": "authorization_code"
    }

    response = requests.get(url, params=params)  # 发送请求
    data = response.json()  # 解析响应

    # session_key = data.get('session_key')
    openid = data.get('openid')
    user = User.objects.filter(openid=openid)
    if user:
        user = user[0]
        data = {
            'openid': openid,
            # 设置nickname为空
            'nickname': user.nickname,
            'avatar': user.avatar,
            'follow': user.follow,
            'atcnum': user.atcnum,
            'fans': user.fans,
        }
    else:
        user = User.objects.create(
            openid=openid, nickname="nickname", avatar=host_name+'media/user/logo.png')
        data = {
            'openid': openid,
            'nickname': None,
            'avatar': host_name+'media/user/logo.png',
            'follow': 0,
            'atcnum': 0,
            'fans': 0,
        }
    print(data)
    return JsonResponse(data)  # 返回响应


def getUserInfo(openid):
    user = User.objects.filter(openid=openid)
    if user:
        user = user[0]
        data = {
            'openid': openid,
            # 设置nickname为空
            'nickname': user.nickname,
            'avatar': user.avatar,
        }
    else:
        data = {
            'openid': openid,
            'nickname': None,
            'avatar': None,
        }
    return data


def HotArticles(request):
    # 获取数据库中所有的Article对象
    articles = Article.objects.all()
    data = []
    for article in articles:
        # 将每个Article对象转换成字典
        info = getUserInfo(article.openid)
        data.append({
            'openid': article.openid,
            'ArticleID': article.ArticleID,
            'nickname': info['nickname'],
            'avatar': info['avatar'],
            'title': article.title,
            'content': article.content,
            'images': json.loads(article.images),
            'time': article.time,
            'like': article.like,
            'comment': article.comment,
            'read': article.read,
        })
    print(data)
    return JsonResponse(data, safe=False)


def init(request):
    Count.objects.all().delete()
    Count.objects.create(
        CountID="1",
        ArticleNum=0,
        PetSpaceNum=0,
    )
    count = Count.objects.get(CountID="1")

    PetSpace.objects.all().delete()
    PetSpace.objects.create(
        openid="ob66w67W7KbxFUShl2c3Q-Z4Pi5Y",
        PetSpaceID=str(count.PetSpaceNum),
        name="溪小明儿",
        breed="英吉利斗牛犬",
        avatar=host_name+'media/user/logo.png',
    )
    count.PetSpaceNum += 1
    PetSpace.objects.create(
        openid="ob66w67W7KbxFUShl2c3Q-Z4Pi5Y",
        PetSpaceID=str(count.PetSpaceNum),
        name="fancy",
        breed="英短",
        avatar=host_name+'media/user/logo.png',
    )
    print(count.PetSpaceNum)
    count.PetSpaceNum += 1
    count.save()

    # 删除数据库中所有的Article对象
    Article.objects.all().delete()

    # 给数据库中添加一个Article对象
    count = Count.objects.get(CountID="1")
    Article.objects.create(
        openid="ob66w612B_fnXnoIqnIGPvfy6HxY",
        ArticleID=str(count.ArticleNum),
        title="标题",
        content="内容",
        images=json.dumps([
            'http://43.143.139.4:8000/media/article/background.jpg',
            'http://43.143.139.4:8000/media/article/background.jpg',
            'http://43.143.139.4:8000/media/article/background.jpg',
            'http://43.143.139.4:8000/media/article/background.jpg',
            'http://43.143.139.4:8000/media/article/background.jpg',
            'http://43.143.139.4:8000/media/article/background.jpg',
            'http://43.143.139.4:8000/media/article/background.jpg',
            'http://43.143.139.4:8000/media/article/background.jpg',
            'http://43.143.139.4:8000/media/article/background.jpg',
        ]),
        time="2020-01-01",
        like=1,
        comment=2,
        read=3
    )
    count.ArticleNum += 1
    Article.objects.create(
        openid="ob66w612B_fnXnoIqnIGPvfy6HxY",
        ArticleID=str(count.ArticleNum),
        title="标题2",
        content="内容2",
        images=json.dumps([
            'http://43.143.139.4:8000/media/article/background.jpg',
        ]),
        time="2020-01-01",
        like=1,
        comment=2,
        read=3
    )
    count.ArticleNum += 1
    count.save()
    return JsonResponse({'status': 'success'})
