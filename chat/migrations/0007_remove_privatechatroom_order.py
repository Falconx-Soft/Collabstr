# Generated by Django 3.2.6 on 2022-07-26 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_privatechatroom_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='privatechatroom',
            name='order',
        ),
    ]
