# Generated by Django 4.2.7 on 2023-12-03 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FancyPet', '0029_message_title_message_wxid'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='PetSpaceID',
            field=models.CharField(default='0', max_length=255),
        ),
    ]