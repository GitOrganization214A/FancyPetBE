# Generated by Django 4.2.7 on 2023-12-27 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FancyPet', '0051_remove_article_combined_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='combined_score',
            field=models.FloatField(default=0),
        ),
    ]
