# Generated by Django 3.2 on 2022-05-13 00:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='submit_requirements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=2000)),
                ('requiremerts', models.CharField(max_length=2000)),
                ('need', models.CharField(max_length=2000)),
                ('apply', models.CharField(max_length=500)),
                ('product_cost', models.IntegerField()),
                ('additional_info', models.CharField(max_length=2000)),
                ('re_use', models.BooleanField()),
                ('name_of_answer', models.CharField(max_length=500)),
                ('influencer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.joininfluencer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
