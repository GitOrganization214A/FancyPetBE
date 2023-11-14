from django.db import models

# Create your models here.


class User(models.Model):
    openid = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255)
    avatar = models.CharField(max_length=255)
    follow = models.IntegerField(default=0)
    atcnum = models.IntegerField(default=0)
    fans = models.IntegerField(default=0)
    likedArticles = models.JSONField(
        blank=True,
        null=True
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


class PetSpace(models.Model):
    openid = models.CharField(max_length=255)
    PetSpaceID = models.CharField(max_length=255, default='0')
    name = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    avatar = models.CharField(max_length=255)
    images = models.JSONField(
        blank=True,
        null=True
    )


class Count(models.Model):
    CountID = models.CharField(max_length=255)
    ArticleNum = models.IntegerField(default=0)
    PetSpaceNum = models.IntegerField(default=0)
