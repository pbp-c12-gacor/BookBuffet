# Generated by Django 4.2.6 on 2023-10-27 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(default='U', max_length=1),
        ),
    ]