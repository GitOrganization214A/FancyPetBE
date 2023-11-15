"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from FancyPet import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/login/', views.login, name='login'),
    path('api/v1/changeInfo/', views.changeInfo, name='changeInfo'),
    path('api/v1/changeAvatar/', views.changeAvatar, name='changeAvatar'),
    path('api/v1/HotArticles/', views.HotArticles, name='HotArticles'),
    path('api/v1/init/', views.init, name='init'),
    path('api/v1/PetSpaces/', views.PetSpaces, name='PetSpaces'),
    path('api/v1/postArticle/', views.postArticle, name='postArticle'),
    path('api/v1/like/', views.like, name='like'),
    path('api/v1/viewArticle/', views.viewArticle, name='viewArticle'),
    path('api/v1/postComment/', views.postComment, name='postComment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
