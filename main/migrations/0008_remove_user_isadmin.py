# Generated by Django 4.2.6 on 2023-10-27 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_remove_user_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='isAdmin',
        ),
    ]