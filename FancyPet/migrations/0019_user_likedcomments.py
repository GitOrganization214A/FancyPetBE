# Generated by Django 4.2.7 on 2023-11-19 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FancyPet', '0018_alter_petspace_month_alter_petspace_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='likedComments',
            field=models.JSONField(blank=True, null=True),
        ),
    ]