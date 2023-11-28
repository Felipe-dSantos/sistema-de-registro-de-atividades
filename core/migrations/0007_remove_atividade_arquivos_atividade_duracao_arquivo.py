# Generated by Django 4.2.3 on 2023-11-24 04:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_atividade_duracao_delete_atividadearquivo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atividade',
            name='arquivos',
        ),
        migrations.AddField(
            model_name='atividade',
            name='duracao',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Arquivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='arquivos/')),
                ('atividade', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.atividade')),
            ],
        ),
    ]
