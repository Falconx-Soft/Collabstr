# Generated by Django 3.2 on 2022-04-15 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0023_brandorinfluencer_joinbrand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joinbrand',
            name='brand_email',
            field=models.CharField(max_length=300),
        ),
    ]