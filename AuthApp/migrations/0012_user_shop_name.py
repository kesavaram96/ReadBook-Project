# Generated by Django 3.2.6 on 2021-11-27 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthApp', '0011_alter_user_phone_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='shop_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
