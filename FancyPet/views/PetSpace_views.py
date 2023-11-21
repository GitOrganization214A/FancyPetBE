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
