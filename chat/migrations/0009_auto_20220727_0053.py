# Generated by Django 3.2.6 on 2022-07-26 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_auto_20220727_0004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='privatechatroom',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='privatechatroom',
            name='influencer',
        ),
    ]