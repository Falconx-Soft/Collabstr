# Generated by Django 3.2 on 2022-04-06 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20220407_0123'),
    ]

    operations = [
        migrations.AddField(
            model_name='joininfluencer',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]