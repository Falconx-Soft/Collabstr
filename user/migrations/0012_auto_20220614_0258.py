# Generated by Django 3.2.6 on 2022-06-13 21:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_previousexprience_previousexprienceimages'),
    ]

    operations = [
        migrations.RenameField(
            model_name='previousexprience',
            old_name='influencer_username',
            new_name='influencer',
        ),
        migrations.RenameField(
            model_name='previousexprienceimages',
            old_name='influencer_username',
            new_name='influencer',
        ),
    ]