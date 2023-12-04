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
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def showMessages(request):
    try:
        openid = request.GET.get('openid')
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
            return JsonResponse({'status': 'Error', 'message': '无权限'})
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


def init(request):
    # count = Count.objects.get(CountID="1")
    # for user in User.objects.all():
    #     user.UserID = str(count.UserNum)
    #     count.UserNum += 1
    #     user.save()
    # count.save()
    for article in Article.objects.all():
        user = User.objects.get(openid=article.openid)
        article.UserID = user.UserID
        article.save()
    return JsonResponse({'status': 'success'})

# def init(request):
#     Count.objects.all().delete()
#     Count.objects.create(
#         CountID="1",
#         ArticleNum=1,
#         PetSpaceNum=1,
#         CommentNum=1,
#         ActivityNum=1,
#     )
#     count = Count.objects.get(CountID="1")

#     PetSpace.objects.all().delete()

#     Activity.objects.all().delete()
#     # Activity.objects.create(
#     #     openid="ob66w612B_fnXnoIqnIGPvfy6HxY",
#     #     type="adopt",
#     #     ActivityID=str(count.ActivityNum),
#     #     PetSpaceID="1",
#     #     title="求好心人领养一只猫猫",
#     #     content="1111111111111111111111",
#     # )
#     # count.ActivityNum += 1
#     # Activity.objects.create(
#     #     openid="ob66w612B_fnXnoIqnIGPfvy6HxY",
#     #     type="adopt",
#     #     ActivityID=str(count.ActivityNum),
#     #     PetSpaceID="2",
#     #     title="求好心人领养一只狗狗",
#     #     content="2222222222222222222222222",
#     # )
#     # count.ActivityNum += 1
#     # count.save()

#     # 删除数据库中所有的Article对象
#     Article.objects.all().delete()

#     # 给数据库中添加一个Article对象
#     count = Count.objects.get(CountID="1")
#     Article.objects.create(
#         openid="ob66w612B_fnXnoIqnIGPvfy6HxY",
#         ArticleID=str(count.ArticleNum),
#         title="家人们谁懂啊",
#         content="今天遇到九只好可爱的猫猫，一整个爱住了",
#         images=json.dumps([
#             {'url': 'http://43.143.139.4:8000/media/article/background.jpg'},
#             {'url': 'http://43.143.139.4:8000/media/article/background.jpg'},
#             {'url': 'http://43.143.139.4:8000/media/article/background.jpg'},
#             {'url': 'http://43.143.139.4:8000/media/article/background.jpg'},
#             {'url': 'http://43.143.139.4:8000/media/article/background.jpg'},
#             {'url': 'http://43.143.139.4:8000/media/article/background.jpg'},
#             {'url': 'http://43.143.139.4:8000/media/article/background.jpg'},
#             {'url': 'http://43.143.139.4:8000/media/article/background.jpg'},
#             {'url': 'http://43.143.139.4:8000/media/article/background.jpg'},
#         ]),
#         time="2020-01-01",
#         like=1,
#         comment=2,
#         read=3,
#         share=4,
#     )
#     count.ArticleNum += 1

#     Article.objects.create(
#         openid="ob66w612B_fnXnoIqnIGPvfy6HxY",
#         ArticleID=str(count.ArticleNum),
#         title="家人们我懂我懂",
#         content="像你这样的小猫咪，生来就是要被妈妈吃掉的",
#         images=json.dumps([
#             {'url': 'http://43.143.139.4:8000/media/article/background.jpg'},
#         ]),
#         time="2020-01-01",
#         like=1,
#         comment=2,
#         read=3,
#         share=4,
#     )
#     count.ArticleNum += 1
#     count.save()

#     # 删除数据库中所有的Comment对象
#     Comment.objects.all().delete()
#     count = Count.objects.get(CountID="1")
#     Comment.objects.create(
#         openid="ob66w63IHeVqG35o6rtQWdUtx6-0",
#         ArticleID="1",
#         CommentID=str(count.CommentNum),
#         content="羡慕猫猫",
#         like=0,
#     )
#     count.CommentNum += 1
#     Comment.objects.create(
#         openid="ob66w67W7KbxFUShl2c3Q-Z4Pi5Y",
#         ArticleID="1",
#         CommentID=str(count.CommentNum),
#         content="一直都想养可爱的小猫猫",
#         like=0,
#     )
#     count.CommentNum += 1
#     count.save()

#     return JsonResponse({'status': 'success'})
