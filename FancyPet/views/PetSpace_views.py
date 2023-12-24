from django.shortcuts import render
from django.http import JsonResponse
from FancyPet.models import User, Article, PetSpace, Count, Comment, Activity
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .forum_views import getArticlesDict
import requests
import json
import os

host_name = 'http://43.143.139.4:8000/'


def permission(openid, PetSpaceID):
    pet = PetSpace.objects.get(PetSpaceID=PetSpaceID)
    shareUsers = json.loads(pet.shareUsers) if pet.shareUsers else []
    if pet.openid != openid and openid not in shareUsers:
        return False
    else:
        return True


@csrf_exempt
def newPetSpace(request):
    print(request.POST)
    avatar = request.FILES.get('avatar', None).read()
    openid = request.POST.get('openid')
    name = request.POST.get('name', '未命名')
    breed = request.POST.get('breed', '未选择')
    year = request.POST.get('year', '0')
    month = request.POST.get('month', '1')
    gender = request.POST.get('gender', '未选择')

    count = Count.objects.get(CountID="1")
    path = 'media/PetSpace/'+str(count.PetSpaceNum)+'.jpg'
    PetSpace.objects.create(
        openid=openid,
        PetSpaceID=str(count.PetSpaceNum),
        public=0,
        name=name,
        avatar=host_name+path,
        breed=breed,
        year=year,
        month=month,
        gender=gender,
        images=json.dumps([]),
    )
    count.PetSpaceNum += 1
    count.save()

    with open(path, 'wb') as f:
        f.write(avatar)

    return JsonResponse({'status': 'success'})


def viewPetSpace(request):
    try:
        openid = request.GET.get('openid', '')
        PetSpaceID = request.GET.get('PetSpaceID')
        petSpace = PetSpace.objects.get(PetSpaceID=PetSpaceID)
        if petSpace.public == 0 and permission(openid, PetSpaceID) == False:
            return JsonResponse({'status': 'Error', 'message': 'No permission'})

        shareUsers = json.loads(
            petSpace.shareUsers) if petSpace.shareUsers else []
        role = ''
        if openid == petSpace.openid:
            role = 'owner'
        elif openid in shareUsers:
            role = 'shareUser'
        else:
            role = 'visitor'
        data = {
            'name': petSpace.name,
            'avatar': petSpace.avatar,
            'breed': petSpace.breed,
            'year': petSpace.year,
            'month': petSpace.month,
            'gender': petSpace.gender,
            'images': json.loads(petSpace.images),
            'role': role,
            'public': petSpace.public == 1,
        }
        print(petSpace.public)
        return JsonResponse(data)

    except ObjectDoesNotExist:
        return JsonResponse({'status': 'No such PetSpace'})

    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def PetSpaces(request):
    openid = request.GET.get('openid')

    petspaces = PetSpace.objects.all()
    data = []
    for petspace in petspaces:
        shareUsers = json.loads(
            petspace.shareUsers) if petspace.shareUsers else []
        if petspace.openid == openid or openid in shareUsers:
            # 将每个PetSpace对象转换成字典
            data.append({
                'PetSpaceID': petspace.PetSpaceID,
                'name': petspace.name,
                'breed': petspace.breed,
                'avatar': petspace.avatar,
            })
    print(data)
    return JsonResponse(data, safe=False)


def deletePetSpace(request):
    try:
        openid = request.GET.get('openid')
        PetSpaceID = request.GET.get('PetSpaceID')
        pet = PetSpace.objects.get(PetSpaceID=PetSpaceID)
        if openid != pet.openid:
            return JsonResponse({'status': 'Error', 'message': 'No permission'})

        pet.delete()
        for activity in Activity.objects.filter(PetSpaceID=PetSpaceID):
            activity.delete()
        for article in Article.objects.filter(PetSpaceID=PetSpaceID):
            article.PetSpaceID = '0'
            article.save()
        for user in User.objects.all():
            bills = json.loads(user.bills) if user.bills else []
            for bill in bills:
                if bill['PetSpaceID'] == PetSpaceID:
                    bill['PetSpaceID'] = '0'
            user.bills = json.dumps(bills)
            user.save()
        return JsonResponse({'status': 'success'})

    except ObjectDoesNotExist:
        return JsonResponse({'status': 'No such PetSpace'})

    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


@csrf_exempt
def newPhoto(request):
    try:
        openid = request.POST.get('openid')
        PetSpaceID = request.POST.get('PetSpaceID')
        image = request.FILES.get('image', None)

        if permission(openid, PetSpaceID) == False:
            return JsonResponse({'status': 'Error', 'message': 'No permission'})
        file = image.read()

        petSpace = PetSpace.objects.get(PetSpaceID=PetSpaceID)
        images = json.loads(petSpace.images)

        petSpace.imageNum += 1
        ext = os.path.splitext(image.name)[1]
        path = 'media/PetSpace/' + \
            PetSpaceID+'_'+str(petSpace.imageNum)+ext
        # 添加到列表的前面
        images.insert(0, host_name+path)
        petSpace.images = json.dumps(images)
        petSpace.save()

        with open(path, 'wb') as f:
            f.write(file)

        return JsonResponse({'status': 'success'})

    except ObjectDoesNotExist:
        return JsonResponse({'status': 'No such PetSpace'})

    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def deletePhoto(request):
    try:
        openid = request.GET.get('openid')
        PetSpaceID = request.GET.get('PetSpaceID')
        index = request.GET.get('index')

        if permission(openid, PetSpaceID) == False:
            return JsonResponse({'status': 'Error', 'message': 'No permission'})

        petSpace = PetSpace.objects.get(PetSpaceID=PetSpaceID)
        images = json.loads(petSpace.images)
        image = images.pop(int(index))
        petSpace.images = json.dumps(images)
        petSpace.save()

        # 删除image的前25个字符，即host_name
        image = image[25:]
        os.remove(image)

        return JsonResponse({'status': 'success'})

    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def addHealthRecord(request):
    try:
        openid = request.GET.get('openid')
        PetSpaceID = request.GET.get('PetSpaceID')
        date = request.GET.get('date')
        content = request.GET.get('content')
        type = request.GET.get('type')

        petSpace = PetSpace.objects.get(PetSpaceID=PetSpaceID)
        if permission(openid, PetSpaceID) == False:
            return JsonResponse({'status': 'Error', 'message': 'No permission'})

        healthRecord = json.loads(
            petSpace.healthRecord) if petSpace.healthRecord else []
        healthRecord.insert(
            0, {'date': date, 'content': content, 'type': type})
        petSpace.healthRecord = json.dumps(healthRecord)
        petSpace.save()

        return JsonResponse({'status': 'success'})

    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def showHealthRecord(request):
    try:
        openid = request.GET.get('openid')
        PetSpaceID = request.GET.get('PetSpaceID')
        petSpace = PetSpace.objects.get(PetSpaceID=PetSpaceID)
        if permission(openid, PetSpaceID) == False:
            return JsonResponse({'status': 'Error', 'message': 'No permission'})

        healthRecord = json.loads(
            petSpace.healthRecord) if petSpace.healthRecord else []

        return JsonResponse(healthRecord, safe=False)

    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def deleteHealthRecord(request):
    try:
        openid = request.GET.get('openid')
        PetSpaceID = request.GET.get('PetSpaceID')
        index = request.GET.get('index')
        petSpace = PetSpace.objects.get(PetSpaceID=PetSpaceID)
        if permission(openid, PetSpaceID) == False:
            return JsonResponse({'status': 'Error', 'message': 'No permission'})

        healthRecord = json.loads(
            petSpace.healthRecord) if petSpace.healthRecord else []
        healthRecord.pop(int(index))
        petSpace.healthRecord = json.dumps(healthRecord)
        petSpace.save()

        return JsonResponse({'status': 'success'})

    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def changePetInfo(request):
    try:
        openid = request.GET.get('openid')
        PetSpaceID = request.GET.get('PetSpaceID')
        name = request.GET.get('name')
        breed = request.GET.get('breed')
        year = request.GET.get('year')
        month = request.GET.get('month')
        gender = request.GET.get('gender')
        pet = PetSpace.objects.get(PetSpaceID=PetSpaceID)
        if permission(openid, PetSpaceID) == False:
            return JsonResponse({'status': 'Error', 'message': 'No permission'})
        pet.name = name
        pet.breed = breed
        pet.year = year
        pet.month = month
        pet.gender = gender
        pet.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


@csrf_exempt
def changePetAvatar(request):
    try:
        openid = request.POST.get('openid')
        PetSpaceID = request.POST.get('PetSpaceID')
        avatar = request.FILES.get('avatar', None).read()
        pet = PetSpace.objects.get(PetSpaceID=PetSpaceID)
        if permission(openid, PetSpaceID) == False:
            return JsonResponse({'status': 'Error', 'message': 'No permission'})
        path = 'media/PetSpace/'+PetSpaceID+'.jpg'
        with open(path, 'wb') as f:
            f.write(avatar)
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def petArticles(request):
    try:
        openid = request.GET.get('openid')
        PetSpaceID = request.GET.get('PetSpaceID')
        articles = Article.objects.filter(PetSpaceID=PetSpaceID)
        data = getArticlesDict(articles, openid)
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def addBill(request):
    try:
        openid = request.GET.get('openid')
        PetSpaceID = request.GET.get('PetSpaceID', 0)
        date = request.GET.get('date')
        content = request.GET.get('content', '')
        type = request.GET.get('type', '')
        money = request.GET.get('money', 0.0)
        user = User.objects.get(openid=openid)
        bills = json.loads(user.bills) if user.bills else []
        bills.insert(0, {'date': date, 'content': content,
                     'type': type, 'money': money, 'PetSpaceID': PetSpaceID})
        user.bills = json.dumps(bills)
        user.save()
        print(bills)

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def showBills(request):
    try:
        openid = request.GET.get('openid')
        user = User.objects.get(openid=openid)
        bills = json.loads(user.bills) if user.bills else []
        cost = 0.0

        for bill in bills:
            print(bill)
            cost += float(bill['money'])
            pet = PetSpace.objects.get(PetSpaceID=bill['PetSpaceID'])
            bill['avatar'] = pet.avatar
            bill['name'] = pet.name

        data = {'bills': bills, 'cost': cost}
        print(data)
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def deleteBill(request):
    try:
        openid = request.GET.get('openid')
        index = request.GET.get('index')
        user = User.objects.get(openid=openid)
        bills = json.loads(user.bills) if user.bills else []
        bills.pop(int(index))
        user.bills = json.dumps(bills)
        user.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def addShareUser(request):
    try:
        openid = request.GET.get('openid')
        PetSpaceID = request.GET.get('PetSpaceID')
        UserID = request.GET.get('UserID')
        pet = PetSpace.objects.get(PetSpaceID=PetSpaceID)
        if openid != pet.openid:
            return JsonResponse({'status': 'Error', 'message': 'No permission'})
        user = User.objects.get(UserID=UserID)
        shareUsers = json.loads(pet.shareUsers) if pet.shareUsers else []
        shareUsers.append(user.openid)
        pet.shareUsers = json.dumps(shareUsers)
        pet.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'Error', 'message': str(e)})


def showShareUsers(request):
    try:
        openid = request.GET.get('openid')
        PetSpaceID = request.GET.get('PetSpaceID')
        pet = PetSpace.objects.get(PetSpaceID=PetSpaceID)
        if permission(openid, PetSpaceID) == False:
            return JsonResponse({'status': 'Error', 'message': 'No permission'})
        shareUsers = json.loads(pet.shareUsers) if pet.shareUsers else []
        print(shareUsers)
        data = []
        for openid in shareUsers:
            user = User.objects.get(openid=openid)
            data.append({
                'UserID': user.UserID,
                'nickname': user.nickname,
                'avatar': user.avatar,
            })
        return JsonResponse(data, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'Error', 'message': str(e)})


def deleteShareUser(request):
    try:
        openid = request.GET.get('openid')
        PetSpaceID = request.GET.get('PetSpaceID')
        UserID = request.GET.get('UserID')
        pet = PetSpace.objects.get(PetSpaceID=PetSpaceID)
        shareUsers = json.loads(pet.shareUsers) if pet.shareUsers else []
        user = User.objects.get(UserID=UserID)
        if permission(openid, PetSpaceID) == False:
            return JsonResponse({'status': 'Error', 'message': 'No permission'})
        if openid != user.openid and openid != pet.openid:
            return JsonResponse({'status': 'Error', 'message': 'No permission'})

        if user.openid in shareUsers:
            shareUsers.remove(user.openid)
            pet.shareUsers = json.dumps(shareUsers)
            pet.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'Error', 'message': 'No such user'})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'Error', 'message': str(e)})


def changeOwner(request):
    try:
        openid = request.GET.get('openid')
        PetSpaceID = request.GET.get('PetSpaceID')
        UserID = request.GET.get('UserID')
        pet = PetSpace.objects.get(PetSpaceID=PetSpaceID)
        if pet.openid != openid:
            return JsonResponse({'status': 'Error', 'message': 'No permission'})
        user = User.objects.get(UserID=UserID)
        shareUsers = json.loads(pet.shareUsers) if pet.shareUsers else []
        if user.openid in shareUsers:
            pet.openid = user.openid
            shareUsers.remove(user.openid)
            shareUsers.append(openid)
            pet.shareUsers = json.dumps(shareUsers)
            pet.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'Error', 'message': 'No such user'})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


def setPublic(request):
    try:
        openid = request.GET.get('openid')
        PetSpaceID = request.GET.get('PetSpaceID')
        operation = request.GET.get('operation')
        if permission(openid, PetSpaceID) == False:
            return JsonResponse({'status': 'Error', 'message': 'No permission'})
        pet = PetSpace.objects.get(PetSpaceID=PetSpaceID)
        if operation == 'public' and pet.public == 0:
            pet.public = 1
            pet.save()
            print(111)
            return JsonResponse({'status': 'success'})
        elif operation == 'private' and pet.public == 1:
            pet.public = 0
            pet.save()
            for activity in Activity.objects.filter(PetSpaceID=PetSpaceID):
                activity.delete()
            for article in Article.objects.filter(PetSpaceID=PetSpaceID):
                article.PetSpaceID = '0'
                article.save()
            return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})
