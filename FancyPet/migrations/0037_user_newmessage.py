# Generated by Django 4.2.7 on 2023-12-05 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FancyPet', '0036_petspace_healthrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='newMessage',
            field=models.IntegerField(default=0),
        ),
    ]
