# Generated by Django 4.2.3 on 2023-12-17 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atividade',
            name='quantidade_ptc',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='atividade',
            name='tema',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='local',
            name='nome',
            field=models.CharField(max_length=50),
        ),
    ]