from django.shortcuts import render
from django.http import JsonResponse
from .models import User, Article
import requests


def changeInfo(request):
    openid = request.GET.get('openid')
    nickname = request.GET.get('nickname')
    avatar = request.GET.get('avatar')

    user = User.objects.filter(openid=openid)
    if user:
        user = user[0]
        user.nickname = nickname
        user.avatar = avatar
        user.save()
    else:
        user = User.objects.create(
            openid=openid, nickname=nickname, avatar=avatar)
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
            openid=openid, nickname="nickname", avatar=None)
        data = {
            'openid': openid,
            'nickname': None,
            'avatar': None,
            'follow': 0,
            'atcnum': 0,
            'fans': 0,
        }

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
            'nickname': info['nickname'],
            'avatar': info['avatar'],
            'title': article.title,
            'content': article.content,
            'image': article.image,
            'time': article.time,
            'like': article.like,
            'comment': article.comment,
            'read': article.read,
        })
    print(data)
    return JsonResponse(data, safe=False)


def init(request):
    # 删除数据库中所有的Article对象
    Article.objects.all().delete()
    # 给数据库中添加一个Article对象
    Article.objects.create(
        openid="o5f8E5Y6Qb4YbV3tY1kDy8Rj5Z3s",
        title="标题",
        content="内容",
        image="https://www.baidu.com/img/bd_logo1.png",
        time="2020-01-01",
        like=0,
        comment=0,
        read=0
    )
    return
