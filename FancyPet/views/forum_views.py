from django.shortcuts import render
from django.http import JsonResponse
from FancyPet.models import User, Article, PetSpace, Count, Comment, Activity
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .user_views import getUserInfo
from django.db.models import Q
import requests
import json
import os

host_name = 'http://43.143.139.4:8000/'


def getComments(openid, ArticleID):
    user = User.objects.get(openid=openid)
    likedComments = json.loads(
        user.likedComments) if user.likedComments else []
    # 找到帖子的评论
    comments = []
    commentList = Comment.objects.filter(ArticleID=ArticleID)
    for comment in commentList:
        user = User.objects.get(openid=comment.openid)
        comments.append({
            'UserID': user.UserID,
            'ArticleID': comment.ArticleID,
            'CommentID': comment.CommentID,
            'nickname': user.nickname,
            'avatar': user.avatar,
            'content': comment.content,
            'time': comment.time.strftime("%Y-%m-%d %H:%M:%S"),
            'like': comment.like,
            'liked': comment.CommentID in likedComments,
            'self': comment.openid == openid,
        })
    return comments


def searchArticles(openid, keyword):
    articles = Article.objects.filter(
        Q(title__contains=keyword) | Q(content__contains=keyword))
    user = User.objects.get(openid=openid)
    likedArticles = json.loads(
        user.likedArticles) if user.likedArticles else []
    data = []
    for article in articles:
        # 将每个Article对象转换成字典
        user = User.objects.get(openid=article.openid)
        data.append({
            'UserID': article.UserID,
            'ArticleID': article.ArticleID,
            'nickname': user.nickname,
            'avatar': user.avatar,
            'title': article.title,
            'content': article.content,
            'PetSpaceID': article.PetSpaceID,
            'images': json.loads(article.images),
            'time': article.time,
            'like': article.like,
            'comment': article.comment,
            'read': article.read,
            'share': article.share,
            'liked': article.ArticleID in likedArticles,
            'self': article.openid == openid,
        })
    return data


def deleteArticle(request):
    try:
        ArticleID = request.GET.get('ArticleID')
        article = Article.objects.get(ArticleID=ArticleID)
        user = User.objects.get(openid=article.openid)
        user.atcnum -= 1
        user.save()
        article.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def deleteComment(request):
    try:
        CommentID = request.GET.get('CommentID')
        comment = Comment.objects.get(CommentID=CommentID)
        article = Article.objects.get(ArticleID=comment.ArticleID)
        article.comment -= 1
        article.save()
        comment.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def deletePetSpace(request):
    try:
        PetSpaceID = request.GET.get('PetSpaceID')
        petSpace = PetSpace.objects.get(PetSpaceID=PetSpaceID)
        petSpace.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def postComment(request):
    ArticleID = request.GET.get('ArticleID')
    openid = request.GET.get('openid')
    content = request.GET.get('content')
    article = Article.objects.get(ArticleID=ArticleID)
    if article:
        article.comment += 1
        article.save()

        count = Count.objects.get(CountID="1")
        Comment.objects.create(
            openid=openid,
            ArticleID=ArticleID,
            CommentID=str(count.CommentNum),
            content=content,
        )
        count.CommentNum += 1
        count.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'No such article'})


def viewArticle(request):
    try:
        ArticleID = request.GET.get('ArticleID')
        openid = request.GET.get('openid')
        article = Article.objects.get(ArticleID=ArticleID)

        article.read += 1
        article.save()

        user = User.objects.get(openid=openid)
        likedArticles = json.loads(
            user.likedArticles) if user.likedArticles else []
        likedComments = json.loads(
            user.likedComments) if user.likedComments else []

        user = User.objects.get(openid=article.openid)
        data = {
            'UserID': article.UserID,
            'ArticleID': article.ArticleID,
            'nickname': user.nickname,
            'avatar': user.avatar,
            'title': article.title,
            'content': article.content,
            'images': json.loads(article.images),
            'time': article.time.strftime("%Y-%m-%d %H:%M:%S"),
            'like': article.like,
            'comment': article.comment,
            'read': article.read,
            'share': article.share,
            'liked': article.ArticleID in likedArticles,
            'self': article.openid == openid,
        }
        return JsonResponse(data)

    except ObjectDoesNotExist:
        return JsonResponse({'status': 'No such article'})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def viewCommentsHot(request):
    try:
        openid = request.GET.get('openid')
        ArticleID = request.GET.get('ArticleID')
        comments = getComments(openid, ArticleID)
        # comments 按点赞数排序
        comments.sort(key=lambda x: x['like'], reverse=True)
        return JsonResponse(comments, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def viewCommentsTime(request):
    try:
        openid = request.GET.get('openid')
        ArticleID = request.GET.get('ArticleID')
        comments = getComments(openid, ArticleID)
        # comments 按时间排序
        comments.sort(key=lambda x: x['time'], reverse=True)
        return JsonResponse(comments, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def likeArticle(request):
    try:
        ArticleID = request.GET.get('ArticleID')
        operartion = request.GET.get('operation')
        openid = request.GET.get('openid')
        user = User.objects.get(openid=openid)
        likedArticles = json.loads(
            user.likedArticles) if user.likedArticles else []
        print(operartion)
        article = Article.objects.get(ArticleID=ArticleID)
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
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def likeComment(request):
    try:
        CommentID = request.GET.get('CommentID')
        operartion = request.GET.get('operation')
        openid = request.GET.get('openid')
        user = User.objects.get(openid=openid)
        likedComments = json.loads(
            user.likedComments) if user.likedComments else []
        print(operartion)
        print(CommentID)
        comment = Comment.objects.get(CommentID=CommentID)
        if operartion == 'like':
            comment.like += 1
            likedComments.append(CommentID)
        elif operartion == 'cancel' and CommentID in likedComments:
            comment.like -= 1
            likedComments.remove(CommentID)
        comment.save()
        user.likedComments = json.dumps(likedComments)
        user.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


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
        PetSpaceID = request.GET.get('PetSpaceID', 0)
        user = User.objects.get(openid=openid)
        Article.objects.create(
            openid=openid,
            UserID=user.UserID,
            ArticleID=str(count.ArticleNum),
            title=title,
            content=content,
            images=json.dumps(images),
        )
        count.ArticleNum += 1
        count.save()
        user = User.objects.get(openid=openid)
        user.atcnum += 1
        user.save()
        return JsonResponse({'ArticleID': str(count.ArticleNum-1)})
    else:
        ArticleID = request.POST.get('ArticleID')
        article = Article.objects.get(ArticleID=ArticleID)
        images = json.loads(article.images)
        img_num = len(images)

        image = request.FILES.get('image', None)
        if image:
            file = image.read()
            ext = os.path.splitext(image.name)[1]
            path = 'media/article/' + \
                str(ArticleID)+'_'+str(img_num+1)+ext
            with open(path, 'wb') as f:
                f.write(file)
            images.append({'url': host_name+path})
        article.images = json.dumps(images)
        article.save()
        return JsonResponse({'ArticleID': ArticleID})


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
        user = User.objects.get(openid=article.openid)
        data.append({
            'UserID': article.UserID,
            'ArticleID': article.ArticleID,
            'nickname': user.nickname,
            'avatar': user.avatar,
            'title': article.title,
            'content': article.content,
            'PetSpaceID': article.PetSpaceID,
            'images': json.loads(article.images),
            'time': article.time,
            'like': article.like,
            'comment': article.comment,
            'read': article.read,
            'share': article.share,
            'liked': article.ArticleID in likedArticles,
        })
    data.sort(key=lambda x: x['like'], reverse=True)
    print(data)
    return JsonResponse(data, safe=False)


def viewUserInfo(request):
    try:
        openid = request.GET.get('openid')
        UserID = request.GET.get('UserID')
        user = User.objects.get(UserID=UserID)
        articles = Article.objects.filter(openid=user.openid)
        likedArticles = json.loads(
            user.likedArticles) if user.likedArticles else []
        # 将每个Article对象转换成字典
        articles = [{
            'ArticleID': article.ArticleID,
            'UserID': article.UserID,
            'title': article.title,
            'content': article.content,
            'images': json.loads(article.images),
            'PetSpaceID': article.PetSpaceID,
            'time': article.time.strftime("%Y-%m-%d %H:%M:%S"),
            'like': article.like,
            'comment': article.comment,
            'read': article.read,
            'share': article.share,
            'liked': article.ArticleID in likedArticles,
            'self': openid == article.openid,
        } for article in articles]

        me = User.objects.get(openid=openid)
        followUsers = json.loads(
            me.followUsers) if me.followUsers else []
        print(followUsers)
        data = {
            'UserID': user.UserID,
            'nickname': user.nickname,
            'avatar': user.avatar,
            'follow': user.follow,
            'atcnum': user.atcnum,
            'fans': user.fans,
            'self': openid == user.openid,
            'followed': UserID in followUsers,
            'articles': articles,
        }
        return JsonResponse(data, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'Error', 'message': str(e)})


def follow(request):
    try:
        openid = request.GET.get('openid')
        UserID = request.GET.get('UserID')
        operation = request.GET.get('operation')
        user1 = User.objects.get(openid=openid)
        user2 = User.objects.get(UserID=UserID)

        followUsers = json.loads(
            user1.followUsers) if user1.followUsers else []
        if operation == 'follow':
            if UserID in followUsers:
                return JsonResponse({'status': 'Error', 'message': 'Already followed'})
            user1.follow += 1
            user2.fans += 1
            followUsers.append(UserID)
        elif operation == 'cancel':
            if UserID not in followUsers:
                return JsonResponse({'status': 'Error', 'message': 'Not followed'})
            user1.follow -= 1
            user2.fans -= 1
            followUsers.remove(UserID)
        user1.followUsers = json.dumps(followUsers)
        user1.save()
        user2.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'Error', 'message': str(e)})


def followArticles(request):
    try:
        openid = request.GET.get('openid')
        user = User.objects.get(openid=openid)
        followUsers = json.loads(
            user.followUsers) if user.followUsers else []
        likedArticles = json.loads(
            user.likedArticles) if user.likedArticles else []

        # 获取数据库中所有的Article对象
        articles = Article.objects.filter(UserID__in=followUsers)
        data = []
        for article in articles:
            # 将每个Article对象转换成字典
            user = User.objects.get(openid=article.openid)
            data.append({
                'UserID': article.UserID,
                'ArticleID': article.ArticleID,
                'nickname': user.nickname,
                'avatar': user.avatar,
                'title': article.title,
                'content': article.content,
                'PetSpaceID': article.PetSpaceID,
                'images': json.loads(article.images),
                'time': article.time,
                'like': article.like,
                'comment': article.comment,
                'read': article.read,
                'share': article.share,
                'liked': article.ArticleID in likedArticles,
                'self': False,
            })
        return JsonResponse(data, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'Error', 'message': str(e)})


def searchArticlesHot(request):
    try:
        openid = request.GET.get('openid')
        keyword = request.GET.get('keyword')
        articles = searchArticles(openid, keyword)
        # articles 按点赞数排序
        articles.sort(key=lambda x: x['like'], reverse=True)
        data = {
            'num': len(articles),
            'articles': articles,
        }
        return JsonResponse(data, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'Error', 'message': str(e)})


def searchArticlesTime(request):
    try:
        openid = request.GET.get('openid')
        keyword = request.GET.get('keyword')
        articles = searchArticles(openid, keyword)
        # articles 按时间排序
        articles.sort(key=lambda x: x['time'], reverse=True)
        data = {
            'num': len(articles),
            'articles': articles,
        }
        return JsonResponse(data, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'Error', 'message': str(e)})


def shareArticle(request):
    try:
        ArticleID = request.GET.get('ArticleID')
        article = Article.objects.get(ArticleID=ArticleID)
        article.share += 1
        article.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'Error', 'message': str(e)})
