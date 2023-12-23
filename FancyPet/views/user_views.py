from django.shortcuts import render
from django.http import JsonResponse
from FancyPet.models import User, Article, PetSpace, Count, Comment, Activity, Message
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import requests
import json
import os


host_name = 'http://43.143.139.4:8000/'


@csrf_exempt
def changeAvatar(request):
    print(request.POST)
    print(request.FILES)
    files = request.FILES
    content = files.get('avatar', None).read()
    openid = request.POST.get('openid')
    print(openid)
    with open('media/user/'+openid+'.jpg', 'wb') as f:
        f.write(content)
    user = User.objects.filter(openid=openid)
    if user:
        user = user[0]
        user.avatar = host_name+'media/user/'+openid+'.jpg'
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
            'UserID': user.UserID,
            'nickname': user.nickname,
            'avatar': user.avatar,
            'follow': user.follow,
            'atcnum': user.atcnum,
            'fans': user.fans,
            'newMessage': user.newMessage,
        }
    else:
        count = Count.objects.get(CountID="1")
        user = User.objects.create(
            openid=openid, nickname="nickname", avatar=host_name+'media/user/logo.png', UserID=str(count.UserNum))
        count.UserNum += 1
        count.save()
        data = {
            'openid': openid,
            'UserID': user.UserID,
            'nickname': 'nickname',
            'avatar': host_name+'media/user/logo.png',
            'follow': 0,
            'atcnum': 0,
            'fans': 0,
        }
    print(data)
    return JsonResponse(data)  # 返回响应


def userInfo(request):
    try:
        openid = request.GET.get('openid')
        user = User.objects.get(openid=openid)
        data = {
            'openid': openid,
            'UserID': user.UserID,
            'nickname': user.nickname,
            'avatar': user.avatar,
            'follow': user.follow,
            'atcnum': user.atcnum,
            'fans': user.fans,
            'newMessage': user.newMessage,
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def showMessages(request):
    try:
        openid = request.GET.get('openid')
        me = User.objects.get(openid=openid)
        me.newMessage = 0
        me.save()

        messages = Message.objects.filter(openid=openid)
        data = []
        for message in messages:
            user = User.objects.get(UserID=message.UserID)
            if message.type == "adopt":
                pet = PetSpace.objects.get(PetSpaceID=message.PetSpaceID1)
                data.append({
                    'MessageID': message.MessageID,
                    'wxid': message.wxid,
                    'UserID': message.UserID,
                    'nickname': user.nickname,
                    'PetSpaceID': message.PetSpaceID1,
                    'PetName': pet.name,
                    'content': message.content,
                    'time': message.time.strftime("%Y-%m-%d %H:%M:%S"),
                    'type': message.type,
                })
            elif message.type == "love":
                pet1 = PetSpace.objects.get(PetSpaceID=message.PetSpaceID1)
                pet2 = PetSpace.objects.get(PetSpaceID=message.PetSpaceID2)
                data.append({
                    'MessageID': message.MessageID,
                    'wxid': message.wxid,
                    'UserID': message.UserID,
                    'nickname': user.nickname,
                    'PetSpaceID1': message.PetSpaceID1,
                    'PetSpaceID2': message.PetSpaceID2,
                    'PetName1': pet1.name,
                    'PetName2': pet2.name,
                    'content': message.content,
                    'time': message.time.strftime("%Y-%m-%d %H:%M:%S"),
                    'type': message.type,
                })
            elif message.type == "party":
                print(message.ActivityID)
                activity = Activity.objects.get(ActivityID=message.ActivityID)
                data.append({
                    'MessageID': message.MessageID,
                    'wxid': message.wxid,
                    'UserID': message.UserID,
                    'nickname': user.nickname,
                    'ActivityID': message.ActivityID,
                    'ActivityName': activity.title,
                    'time': message.time.strftime("%Y-%m-%d %H:%M:%S"),
                    'type': message.type,
                })
        print(data)
        return JsonResponse(data, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'Error', 'message': str(e)})


def deleteMessage(request):
    try:
        openid = request.GET.get('openid')
        MessageID = request.GET.get('MessageID')
        message = Message.objects.get(MessageID=MessageID)
        if message.openid == openid:
            message.delete()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'Error', 'message': 'No permission'})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


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


def myFollows(request):
    try:
        openid = request.GET.get('openid')
        me = User.objects.get(openid=openid)
        follows = json.loads(me.followUsers) if me.followUsers else []
        data = []
        for UserID in follows:
            user = User.objects.get(UserID=UserID)
            data.append({
                'UserID': user.UserID,
                'nickname': user.nickname,
                'avatar': user.avatar,
                'followed': True,
            })
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def myFans(request):
    try:
        openid = request.GET.get('openid')
        me = User.objects.get(openid=openid)
        myFollows = json.loads(me.followUsers) if me.followUsers else []
        UserID = me.UserID
        data = []
        for user in User.objects.all():
            follows = json.loads(user.followUsers) if user.followUsers else []
            if UserID in follows:
                data.append({
                    'UserID': user.UserID,
                    'nickname': user.nickname,
                    'avatar': user.avatar,
                    'followed': user.UserID in myFollows,
                })
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def init(request):
    num = 0
    for article in Article.objects.all():
        num += 1
    print(num)
    return JsonResponse({'status': 'success'})
