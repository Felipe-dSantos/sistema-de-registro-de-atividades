# Generated by Django 4.2.3 on 2023-09-28 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_atividade_duracao_alter_arquivo_arquivo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arquivo',
            name='arquivo',
            field=models.FileField(upload_to='arquivos/'),
        ),
    ]
