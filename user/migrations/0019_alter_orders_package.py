# Generated by Django 3.2.6 on 2022-07-19 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_alter_orders_crated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='package',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.influencerpackage'),
        ),
    ]
