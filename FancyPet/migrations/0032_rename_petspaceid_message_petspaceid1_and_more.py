# Generated by Django 4.2.7 on 2023-12-04 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FancyPet', '0031_message_userid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='PetSpaceID',
            new_name='PetSpaceID1',
        ),
        migrations.AddField(
            model_name='message',
            name='PetSpaceID2',
            field=models.CharField(default='0', max_length=255),
        ),
    ]