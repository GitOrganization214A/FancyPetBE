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
    path('api/v1/likeArticle/', views.likeArticle, name='likeArticle'),
    path('api/v1/likeComment/', views.likeComment, name='likeComment'),
    path('api/v1/viewArticle/', views.viewArticle, name='viewArticle'),
    path('api/v1/viewCommentsHot/', views.viewCommentsHot, name='viewCommentsHot'),
    path('api/v1/viewCommentsTime/',
         views.viewCommentsTime, name='viewCommentsTime'),
    path('api/v1/postComment/', views.postComment, name='postComment'),
    path('api/v1/newPetSpace/', views.newPetSpace, name='newPetSpace'),
    path('api/v1/viewPetSpace/', views.viewPetSpace, name='viewPetSpace'),
    path('api/v1/deleteArticle/', views.deleteArticle, name='deleteArticle'),
    path('api/v1/deleteComment/', views.deleteComment, name='deleteComment'),
    path('api/v1/QRcode/', views.QRcode, name='QRcode'),
    path('api/v1/adoptPet/', views.adoptPet, name='adoptPet'),
    path('api/v1/postAdopt/', views.postAdopt, name='postAdopt'),
    path('api/v1/lovePet/', views.lovePet, name='lovePet'),
    path('api/v1/postLove/', views.postLove, name='postLove'),
    path('api/v1/applyAdopt/', views.applyAdopt, name='applyAdopt'),
    path('api/v1/applyLove/', views.applyLove, name='applyLove'),
    path('api/v1/deleteActivity/', views.deleteActivity, name='deleteActivity'),
    path('api/v1/viewUserInfo/', views.viewUserInfo, name='viewUserInfo'),
    path('api/v1/deletePetSpace/', views.deletePetSpace, name='deletePetSpace'),
    path('api/v1/partyPet/', views.partyPet, name='partyPet'),
    path('api/v1/postParty/', views.postParty, name='postParty'),
    path('api/v1/applyParty/', views.applyParty, name='applyParty'),
    path('api/v1/newPhoto/', views.newPhoto, name='newPhoto'),
    path('api/v1/deletePhoto/', views.deletePhoto, name='deletePhoto'),
    path('api/v1/follow/', views.follow, name='follow'),
    path('api/v1/showMessages/', views.showMessages, name='showMessages'),
    path('api/v1/deleteMessage/', views.deleteMessage, name='deleteMessage'),
    path('api/v1/followArticles/', views.followArticles, name='followArticles'),
    path('api/v1/addHealthRecord/', views.addHealthRecord, name='addHealthRecord'),
    path('api/v1/showHealthRecord/',
         views.showHealthRecord, name='showHealthRecord'),
    path('api/v1/searchArticlesHot/',
         views.searchArticlesHot, name='searchArticlesHot'),
    path('api/v1/searchArticlesTime/',
         views.searchArticlesTime, name='searchArticlesTime'),
    path('api/v1/changePetInfo/', views.changePetInfo, name='changePetInfo'),
    path('api/v1/changePetAvatar/', views.changePetAvatar, name='changePetAvatar'),
    path('api/v1/petVideos/', views.petVideos, name='petVideos'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
