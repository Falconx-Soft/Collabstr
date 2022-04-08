# Generated by Django 3.2 on 2022-04-06 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20220406_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='joininfluencer',
            name='instagram_followers',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='joininfluencer',
            name='instagram_username',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='joininfluencer',
            name='tiktok_followers',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='joininfluencer',
            name='tiktok_username',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='joininfluencer',
            name='twitch_username',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='joininfluencer',
            name='twitter_followers',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='joininfluencer',
            name='twitter_username',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='joininfluencer',
            name='website',
            field=models.URLField(default=''),
        ),
        migrations.AddField(
            model_name='joininfluencer',
            name='youtube_url',
            field=models.URLField(default=''),
        ),
    ]