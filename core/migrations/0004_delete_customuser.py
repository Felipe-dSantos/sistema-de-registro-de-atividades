# Generated by Django 4.2.3 on 2023-11-16 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
