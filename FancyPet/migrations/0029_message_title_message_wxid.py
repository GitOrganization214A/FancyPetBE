# Generated by Django 4.2.7 on 2023-12-02 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FancyPet', '0028_message_count_messagenum'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='title',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='message',
            name='wxid',
            field=models.CharField(default='', max_length=255),
        ),
    ]