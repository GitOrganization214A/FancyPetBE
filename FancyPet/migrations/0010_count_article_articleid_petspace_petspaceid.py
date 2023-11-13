# Generated by Django 4.2.7 on 2023-11-12 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FancyPet', '0009_petspace'),
    ]

    operations = [
        migrations.CreateModel(
            name='Count',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CountID', models.CharField(max_length=255)),
                ('ArticleNum', models.IntegerField(default=0)),
                ('PetSpaceNum', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='ArticleID',
            field=models.CharField(default='0', max_length=255),
        ),
        migrations.AddField(
            model_name='petspace',
            name='PetSpaceID',
            field=models.CharField(default='0', max_length=255),
        ),
    ]
