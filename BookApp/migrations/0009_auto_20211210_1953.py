# Generated by Django 3.2.6 on 2021-12-10 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookApp', '0008_auto_20211210_1650'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='PublicationDate',
            new_name='PublicationYear',
        ),
        migrations.AddField(
            model_name='book',
            name='Upload_Date',
            field=models.DateField(auto_now=True),
        ),
    ]
