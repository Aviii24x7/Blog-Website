# Generated by Django 4.1.7 on 2023-04-25 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aviBlog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image_name',
            field=models.ImageField(upload_to='posts'),
        ),
    ]