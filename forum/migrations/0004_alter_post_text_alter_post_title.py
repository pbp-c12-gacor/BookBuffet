# Generated by Django 4.2.6 on 2023-10-29 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_remove_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(max_length=50),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.TextField(max_length=25),
        ),
    ]