# Generated by Django 3.2.6 on 2022-06-15 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_remove_orders_crated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='crated_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
