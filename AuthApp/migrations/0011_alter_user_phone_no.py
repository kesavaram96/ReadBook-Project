# Generated by Django 3.2.6 on 2021-11-25 15:21

from django.db import migrations
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthApp', '0010_auto_20211016_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_no',
            field=phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31, null=True, unique=True),
        ),
    ]