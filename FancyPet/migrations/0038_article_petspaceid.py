# Generated by Django 4.2.7 on 2023-12-09 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FancyPet', '0037_user_newmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='PetSpaceID',
            field=models.CharField(default='0', max_length=255),
        ),
    ]