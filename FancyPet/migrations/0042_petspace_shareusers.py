# Generated by Django 4.2.7 on 2023-12-20 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FancyPet', '0041_petspace_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='petspace',
            name='shareUsers',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
