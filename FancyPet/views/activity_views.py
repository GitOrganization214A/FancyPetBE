from django.shortcuts import render
from django.http import JsonResponse
from FancyPet.models import User, Article, PetSpace, Count, Comment, Activity, Message
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .user_views import getUserInfo
import requests
import json
import os

host_name = 'http://43.143.139.4:8000/'


def getPetInfo(PetSpaceID):
    try:
        pet = PetSpace.objects.get(PetSpaceID=PetSpaceID)
        data = {
            'avatar': pet.avatar,
            'name': pet.name,
            'breed': pet.breed,
        }
        return data
    except Exception as e:
        return {'status': 'Error', 'message': str(e)}


def adoptPet(request):
    try:
        openid = request.GET.get('openid')
        activities = Activity.objects.filter(type="adopt")
        data = []
        for activity in activities:
            user = User.objects.get(openid=activity.openid)
            data.append({
                'UserID': user.UserID,
                'ActivityID': activity.ActivityID,
                'PetSpaceID': activity.PetSpaceID,
                'nickname': user.nickname,
                'avatar': user.avatar,
                'content': activity.content,
                'self': activity.openid == openid,
                'pet': getPetInfo(activity.PetSpaceID),
            })
        print(data)
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def postAdopt(request):
    try:
        openid = request.GET.get('openid')
        PetSpaceID = request.GET.get('PetSpaceID')
        content = request.GET.get('content')
        count = Count.objects.get(CountID="1")
        Activity.objects.create(
            openid=openid,
            ActivityID=str(count.ActivityNum),
            PetSpaceID=PetSpaceID,
            title='',
            content=content,
            type="adopt",
        )
        count.ActivityNum += 1
        count.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def applyAdopt(request):
    try:
        openid = request.GET.get('openid')
        content = request.GET.get('content')
        ActivityID = request.GET.get('ActivityID')
        wxid = request.GET.get('wxid')

        activity = Activity.objects.get(ActivityID=ActivityID)
        user = User.objects.get(openid=openid)

        count = Count.objects.get(CountID="1")
        Message.objects.create(
            openid=activity.openid,
            wxid=wxid,
            UserID=user.UserID,
            PetSpaceID1=activity.PetSpaceID,
            MessageID=str(count.MessageNum),
            type="adopt",
            title='',
            content=content,
        )
        count.MessageNum += 1
        count.save()
        user2 = User.objects.get(openid=activity.openid)
        user2.newMessage += 1
        user2.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def lovePet(request):
    try:
        openid = request.GET.get('openid')
        activities = Activity.objects.filter(type="love")
        data = []
        for activity in activities:
            user = User.objects.get(openid=activity.openid)
            data.append({
                'UserID': user.UserID,
                'ActivityID': activity.ActivityID,
                'PetSpaceID': activity.PetSpaceID,
                'nickname': user.nickname,
                'avatar': user.avatar,
                'content': activity.content,
                'self': activity.openid == openid,
                'pet': getPetInfo(activity.PetSpaceID),
            })
        print(data)
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def postLove(request):
    try:
        openid = request.GET.get('openid')
        PetSpaceID = request.GET.get('PetSpaceID')
        content = request.GET.get('content')
        count = Count.objects.get(CountID="1")
        Activity.objects.create(
            openid=openid,
            ActivityID=str(count.ActivityNum),
            PetSpaceID=PetSpaceID,
            title='',
            content=content,
            type="love",
        )
        count.ActivityNum += 1
        count.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def applyLove(request):
    try:
        openid = request.GET.get('openid')
        wxid = request.GET.get('wxid')
        content = request.GET.get('content')
        ActivityID = request.GET.get('ActivityID')
        PetSpaceID = request.GET.get('PetSpaceID')

        activity = Activity.objects.get(ActivityID=ActivityID)

        user = User.objects.get(openid=openid)

        count = Count.objects.get(CountID="1")
        Message.objects.create(
            openid=activity.openid,
            wxid=wxid,
            UserID=user.UserID,
            PetSpaceID1=activity.PetSpaceID,
            PetSpaceID2=PetSpaceID,
            MessageID=str(count.MessageNum),
            type="love",
            title='',
            content=content,
        )
        count.MessageNum += 1
        count.save()
        user2 = User.objects.get(openid=activity.openid)
        user2.newMessage += 1
        user2.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


@csrf_exempt
def postParty(request):
    print(request.POST)
    print(request.FILES)
    try:
        openid = request.POST.get('openid')
        content = request.POST.get('content')
        time = request.POST.get('date')
        address = request.POST.get('address')
        title = request.POST.get('title')
        image = request.FILES.get('image').read()
        count = Count.objects.get(CountID="1")
        path = 'media/activity/'+str(count.ActivityNum)+'.jpg'
        with open(path, 'wb') as f:
            f.write(image)
        Activity.objects.create(
            openid=openid,
            ActivityID=str(count.ActivityNum),
            PetSpaceID="0",
            title=title,
            content=content,
            type="party",
            time=time,
            address=address,
            img=host_name+path,
        )
        count.ActivityNum += 1
        count.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'Error', 'message': str(e)})


def partyPet(request):
    try:
        openid = request.GET.get('openid')
        activities = Activity.objects.filter(type="party")
        data = []
        for activity in activities:
            user = User.objects.get(openid=activity.openid)
            data.append({
                'UserID': user.UserID,
                'ActivityID': activity.ActivityID,
                'nickname': user.nickname,
                'avatar': user.avatar,
                'time': activity.time,
                'address': activity.address,
                'title': activity.title,
                'content': activity.content,
                'img': activity.img,
                'self': activity.openid == openid,
            })
        print(data)
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def applyParty(request):
    try:
        openid = request.GET.get('openid')
        # content = request.GET.get('content')
        ActivityID = request.GET.get('ActivityID')

        activity = Activity.objects.get(ActivityID=ActivityID)
        user = User.objects.get(openid=openid)

        count = Count.objects.get(CountID="1")
        Message.objects.create(
            openid=activity.openid,
            wxid='',
            UserID=user.UserID,
            MessageID=str(count.MessageNum),
            ActivityID=ActivityID,
            type="party",
            title='',
            content='',
        )
        count.MessageNum += 1
        count.save()
        user2 = User.objects.get(openid=activity.openid)
        user2.newMessage += 1
        user2.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def deleteActivity(request):
    try:
        ActivityID = request.GET.get('ActivityID')
        activity = Activity.objects.get(ActivityID=ActivityID)
        activity.delete()
        massages = Message.objects.filter(ActivityID=ActivityID)
        if massages:
            for massage in massages:
                massage.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def petVideos(request):
    try:
        openid = request.GET.get('openid')
        me = User.objects.get(openid=openid)
        likedArticles = json.loads(
            me.likedArticles) if me.likedArticles else []

        data = []
        for article in Article.objects.all():
            images = json.loads(article.images) if article.images else []
            for image in images:
                if image['url'].endswith('.mp4'):
                    user = User.objects.get(openid=article.openid)
                    data.append({
                        'ArticleID': article.ArticleID,
                        'UserID': user.UserID,
                        'nickname': user.nickname,
                        'avatar': user.avatar,
                        'title': article.title,
                        'content': article.content,
                        'video': image,
                        'time': article.time,
                        'like': article.like,
                        'liked': article.ArticleID in likedArticles,
                        'self': article.openid == openid,
                    })
        return JsonResponse(data, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'Error', 'message': str(e)})


def QRcode(request):
    try:
        # 请求获取 access_token
        appid = "wx17396561c08eee6a"
        secret = "1553b8c2bdf47f280ffeb61c989e0f50"
        token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}"

        response = requests.post(token_url)
        data = response.json()
        access_token = data.get('access_token')

        curscene = request.GET.get('curscene')

        wxacode_url = f"https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token={access_token}"

        response = requests.post(wxacode_url, json={'scene': curscene})
        with open('media/PetSpace/1_QRcode.jpg', 'wb') as f:
            f.write(response.content)

        return JsonResponse({'status': 'success'})

    except Exception as e:
        return JsonResponse({'error': str(e)})
