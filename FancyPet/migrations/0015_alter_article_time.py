# Generated by Django 4.2.7 on 2023-11-15 10:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('FancyPet', '0014_article_share'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]