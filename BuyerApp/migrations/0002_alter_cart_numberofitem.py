# Generated by Django 3.2.6 on 2021-12-04 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BuyerApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='NumberOfItem',
            field=models.IntegerField(),
        ),
    ]