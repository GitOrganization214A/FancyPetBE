from django.shortcuts import render
from django.http import JsonResponse
from .models import User, Article, PetSpace, Count, Comment
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import os

host_name = 'http://43.143.139.4:8000/'


def postComment(request):
    ArticleID = request.GET.get('ArticleID')
    openid = request.GET.get('openid')
    content = request.GET.get('content')
    article = Article.objects.get(ArticleID=ArticleID)
    if article:
        article.comment += 1
        article.save()
        user = User.objects.get(openid=openid)
        info = getUserInfo(openid)
        data = {
            'openid': openid,
            'ArticleID': ArticleID,
            'nickname': info['nickname'],
            'avatar': info['avatar'],
            'content': content,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'status': 'No such article'})


@csrf_exempt
def newPetSpace(request):
    print(request.POST)
    avatar = request.FILES.get('avatar', None).read()
    openid = request.POST.get('openid')
    name = request.POST.get('name')
    breed = request.POST.get('breed')
    year = request.POST.get('year')
    month = request.POST.get('month')
    gender = request.POST.get('gender')

    count = Count.objects.get(CountID="1")
    path = 'media/PetSpace/'+str(count.PetSpaceNum)+'.jpg'
    PetSpace.objects.create(
        openid=openid,
        PetSpaceID=str(count.PetSpaceNum),
        name=name,
        avatar=host_name+path,
        breed=breed,
        year=year,
        month=month,
        gender=gender,
    )
    count.PetSpaceNum += 1
    count.save()

    with open(path, 'wb') as f:
        f.write(avatar)

    return JsonResponse({'status': 'success'})


def viewArticle(request):
    ArticleID = request.GET.get('ArticleID')
    openid = request.GET.get('openid')
    article = Article.objects.get(ArticleID=ArticleID)

    if article:
        article.read += 1
        article.save()

        user = User.objects.get(openid=openid)
        likedArticles = json.loads(
            user.likedArticles) if user.likedArticles else []

        # 找到帖子的评论
        comments = []
        commentList = Comment.objects.filter(ArticleID=ArticleID)
        for comment in commentList:
            info = getUserInfo(comment.openid)
            comments.append({
                'openid': comment.openid,
                'ArticleID': comment.ArticleID,
                'CommentID': comment.CommentID,
                'nickname': info['nickname'],
                'avatar': info['avatar'],
                'content': comment.content,
                'time': comment.time.strftime("%Y-%m-%d %H:%M:%S"),
                'like': comment.like,
            })

        info = getUserInfo(article.openid)
        data = {
            'openid': article.openid,
            'ArticleID': article.ArticleID,
            'nickname': info['nickname'],
            'avatar': info['avatar'],
            'title': article.title,
            'content': article.content,
            'images': json.loads(article.images),
            'time': article.time.strftime("%Y-%m-%d %H:%M:%S"),
            'like': article.like,
            'comment': article.comment,
            'read': article.read,
            'share': article.share,
            'liked': article.ArticleID in likedArticles,
            'comments': comments,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'status': 'No such article'})


def like(request):
    ArticleID = request.GET.get('ArticleID')
    operartion = request.GET.get('operation')
    openid = request.GET.get('openid')
    user = User.objects.get(openid=openid)
    likedArticles = json.loads(
        user.likedArticles) if user.likedArticles else []
    print(operartion)
    article = Article.objects.get(ArticleID=ArticleID)
    if article:
        if operartion == 'like':
            article.like += 1
            likedArticles.append(ArticleID)
        elif operartion == 'cancel' and ArticleID in likedArticles:
            article.like -= 1
            likedArticles.remove(ArticleID)
        article.save()
        user.likedArticles = json.dumps(likedArticles)
        user.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'No such article'})


@csrf_exempt
def postArticle(request):
    print("get:", request.GET)
    print("post:", request.POST)
    if request.method == 'GET':
        count = Count.objects.get(CountID="1")
        images = []

        openid = request.GET.get('openid')
        title = request.GET.get('title')
        content = request.GET.get('content')
        Article.objects.create(
            openid=openid,
            ArticleID=str(count.ArticleNum),
            title=title,
            content=content,
            images=json.dumps(images),
        )
        count.ArticleNum += 1
        count.save()
        return JsonResponse({'ArticleID': str(count.ArticleNum-1)})
    else:
        ArticleID = request.POST.get('ArticleID')
        article = Article.objects.get(ArticleID=ArticleID)
        images = json.loads(article.images)
        img_num = len(images)
        #
        image = request.FILES.get('image', None).read()
        if image:
            path = 'media/article/' + \
                str(ArticleID)+'_'+str(img_num+1)+'.jpg'
            with open(path, 'wb') as f:
                f.write(image)
            images.append(host_name+path)
        article.images = json.dumps(images)
        article.save()
        return JsonResponse({'ArticleID': ArticleID})


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
    with open('media/user/'+openid+'.jpg', 'wb') as f:
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
    openid = request.GET.get('openid')
    print(openid)
    user = User.objects.get(openid=openid)
    likedArticles = json.loads(
        user.likedArticles) if user.likedArticles else []
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
            'share': article.share,
            'liked': article.ArticleID in likedArticles,
        })
    print(data)
    return JsonResponse(data, safe=False)


def init(request):
    Count.objects.all().delete()
    Count.objects.create(
        CountID="1",
        ArticleNum=1,
        PetSpaceNum=1,
        CommentNum=1,
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
        read=3,
        share=4,
    )
    count.ArticleNum += 1
    count.CommentNum += 2
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
        read=3,
        share=4,
    )
    count.ArticleNum += 1
    count.save()

    # 删除数据库中所有的Comment对象
    Comment.objects.all().delete()
    count = Count.objects.get(CountID="1")
    Comment.objects.create(
        openid="ob66w63IHeVqG35o6rtQWdUtx6-0",
        ArticleID="1",
        CommentID=str(count.CommentNum),
        content="I am Fancy",
        like=0,
    )
    count.CommentNum += 1
    Comment.objects.create(
        openid="ob66w67W7KbxFUShl2c3Q-Z4Pi5Y",
        ArticleID="1",
        CommentID=str(count.CommentNum),
        content="I like Fancy",
        like=0,
    )
    count.CommentNum += 1
    count.save()

    return JsonResponse({'status': 'success'})
