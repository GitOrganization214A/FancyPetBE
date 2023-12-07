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
        images=json.dumps([]),
    )
    count.PetSpaceNum += 1
    count.save()

    with open(path, 'wb') as f:
        f.write(avatar)

    return JsonResponse({'status': 'success'})


def viewPetSpace(request):
    try:
        PetSpaceID = request.GET.get('PetSpaceID')
        petSpace = PetSpace.objects.get(PetSpaceID=PetSpaceID)

        data = {
            'name': petSpace.name,
            'avatar': petSpace.avatar,
            'breed': petSpace.breed,
            'year': petSpace.year,
            'month': petSpace.month,
            'gender': petSpace.gender,
            'images': json.loads(petSpace.images),
        }
        print(data)
        return JsonResponse(data)

    except ObjectDoesNotExist:
        return JsonResponse({'status': 'No such PetSpace'})

    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


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


def deletePetSpace(request):
    try:
        PetSpaceID = request.GET.get('PetSpaceID')
        PetSpace.objects.get(PetSpaceID=PetSpaceID).delete()
        return JsonResponse({'status': 'success'})

    except ObjectDoesNotExist:
        return JsonResponse({'status': 'No such PetSpace'})

    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})


@csrf_exempt
def newPhoto(request):
    try:
        PetSpaceID = request.POST.get('PetSpaceID')
        image = request.FILES.get('image', None)
        file = image.read()

        petSpace = PetSpace.objects.get(PetSpaceID=PetSpaceID)
        images = json.loads(petSpace.images)

        petSpace.imageNum += 1
        ext = os.path.splitext(image.name)[1]
        path = 'media/PetSpace/' + \
            PetSpaceID+'_'+str(petSpace.imageNum)+ext
        images.append(host_name+path)
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
        PetSpaceID = request.GET.get('PetSpaceID')
        index = request.GET.get('index')

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
        if petSpace.openid != openid:
            return JsonResponse({'status': 'Error', 'message': 'No permission'})

        healthRecord = json.loads(
            petSpace.healthRecord) if petSpace.healthRecord else []
        healthRecord.append({'date': date, 'content': content, 'type': type})
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
        if petSpace.openid != openid:
            return JsonResponse({'status': 'Error', 'message': 'No permission'})

        healthRecord = json.loads(
            petSpace.healthRecord) if petSpace.healthRecord else []
        # 列表倒序
        healthRecord.reverse()
        return JsonResponse(healthRecord, safe=False)

    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})
