# Generated by Django 4.2.6 on 2023-10-27 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_delete_extendeduser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='status',
        ),
    ]
