# Generated by Django 4.2.7 on 2023-11-14 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FancyPet', '0012_article_comments_count_commentnum'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openid', models.CharField(max_length=255)),
                ('ArticleID', models.CharField(max_length=255)),
                ('CommentID', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('like', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='article',
            name='comments',
        ),
        migrations.AlterField(
            model_name='count',
            name='ArticleNum',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='count',
            name='CommentNum',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='count',
            name='PetSpaceNum',
            field=models.IntegerField(default=1),
        ),
    ]