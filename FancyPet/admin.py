from django.contrib import admin

# Register your models here.
from .models import User, Article, PetSpace, Activity, Video, Message, Comment

admin.site.register(User)
admin.site.register(Article)
admin.site.register(PetSpace)
admin.site.register(Activity)
admin.site.register(Video)
admin.site.register(Message)
admin.site.register(Comment)
