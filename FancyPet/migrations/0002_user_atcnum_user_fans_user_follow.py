# Generated by Django 4.2.7 on 2023-11-08 02:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("FancyPet", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="atcnum",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="user",
            name="fans",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="user",
            name="follow",
            field=models.IntegerField(default=0),
        ),
    ]
