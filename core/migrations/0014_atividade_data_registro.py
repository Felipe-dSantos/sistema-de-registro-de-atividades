# Generated by Django 4.2.3 on 2023-12-01 03:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_delete_testdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='atividade',
            name='data_registro',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]