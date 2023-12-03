from django.db import models
from django.utils import timezone
import json
import pytz
# Create your models here.


class User(models.Model):
    openid = models.CharField(max_length=255)
    UserID = models.CharField(max_length=255, default='0')
    nickname = models.CharField(max_length=255)
    avatar = models.CharField(max_length=255)
    follow = models.IntegerField(default=0)
    atcnum = models.IntegerField(default=0)
    fans = models.IntegerField(default=0)
    likedArticles = models.JSONField(
        blank=True,
        null=True
    )
    likedComments = models.JSONField(
        blank=True,
        null=True
    )
    followUsers = models.JSONField(
        blank=True,
        null=True,
        default=list
    )


class Article(models.Model):
    openid = models.CharField(max_length=255)
    ArticleID = models.CharField(max_length=255, default='0')
    title = models.CharField(max_length=255)
    content = models.TextField()
    images = models.JSONField(
        blank=True,
        null=True
    )
    time = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)
    comment = models.IntegerField(default=0)
    read = models.IntegerField(default=0)
    share = models.IntegerField(default=0)


class PetSpace(models.Model):
    openid = models.CharField(max_length=255)
    PetSpaceID = models.CharField(max_length=255, default='0')
    name = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    avatar = models.CharField(max_length=255)
    year = models.CharField(max_length=255, default='')
    month = models.CharField(max_length=255, default='')
    gender = models.CharField(max_length=255, default='')
    imageNum = models.IntegerField(default=0)
    images = models.JSONField(
        blank=True,
        null=True
    )


class Comment(models.Model):
    openid = models.CharField(max_length=255)
    ArticleID = models.CharField(max_length=255)
    CommentID = models.CharField(max_length=255)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)


class Activity(models.Model):
    openid = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    ActivityID = models.CharField(max_length=255, default='0')
    PetSpaceID = models.CharField(max_length=255, default='0')
    title = models.CharField(max_length=255)
    content = models.TextField()
    time = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=255, default='')
    img = models.CharField(max_length=255, default='')


class Message(models.Model):
    openid = models.CharField(max_length=255)
    wxid = models.CharField(max_length=255, default='')
    UserID = models.CharField(max_length=255, default='0')
    PetSpaceID = models.CharField(max_length=255, default='0')
    title = models.CharField(max_length=255, default='')
    MessageID = models.CharField(max_length=255, default='0')
    type = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)


class Count(models.Model):
    CountID = models.CharField(max_length=255)
    UserNum = models.IntegerField(default=1)
    ArticleNum = models.IntegerField(default=1)
    PetSpaceNum = models.IntegerField(default=1)
    CommentNum = models.IntegerField(default=1)
    ActivityNum = models.IntegerField(default=1)
    MessageNum = models.IntegerField(default=1)
