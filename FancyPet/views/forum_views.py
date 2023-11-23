from django.shortcuts import render
from django.http import JsonResponse
from FancyPet.models import User, Article, PetSpace, Count, Comment, Activity
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .user_views import getUserInfo
import requests
import json
import os

host_name = 'http://43.143.139.4:8000/'


def deleteArticle(request):
    try:
        ArticleID = request.GET.get('ArticleID')
        article = Article.objects.get(ArticleID=ArticleID)
        article.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def deleteComment(request):
    try:
        CommentID = request.GET.get('CommentID')
        comment = Comment.objects.get(CommentID=CommentID)
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
                'self': comment.openid == openid,
            })
        return JsonResponse({'status': 'success', 'comments': comments})
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
                'self': comment.openid == openid,
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
            'self': article.openid == openid,
            'comments': comments,
        }
        return JsonResponse(data)

    except ObjectDoesNotExist:
        return JsonResponse({'status': 'No such article'})
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
        # 获取文件后缀名
        image = request.FILES.get('image', None)
        if image:
            file = image.read()
            ext = os.path.splitext(image.name)[1]
            print(ext)
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
