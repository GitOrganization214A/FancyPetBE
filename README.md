##Django后端项目



####响应请求
1. 在urls.py文件中定义路由，将URL映射到对应的视图函数。
2. 在views.py文件中定义视图函数，处理前端请求并返回响应。
```
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello_world, name='hello_world'),
]

# views.py
from django.http import JsonResponse

def hello_world(request):
    return JsonResponse({"message": "Hello, world!"})
```

####数据库修改
每次修改数据库配置需要执行迁移
```
python3 manage.py makemigrations
python3 manage.py migrate
```