# Generated by Django 3.2.6 on 2022-07-19 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_alter_orders_crated_at'),
        ('chat', '0003_auto_20220530_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='privatechatroom',
            name='order',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='user.orders'),
        ),
    ]
