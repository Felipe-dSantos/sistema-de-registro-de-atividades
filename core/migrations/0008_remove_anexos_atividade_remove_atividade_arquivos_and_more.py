# Generated by Django 4.2.3 on 2023-09-15 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_anexos_delete_pdfmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anexos',
            name='atividade',
        ),
        migrations.RemoveField(
            model_name='atividade',
            name='arquivos',
        ),
        migrations.AddField(
            model_name='anexos',
            name='arquivos',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='arquivos', to='core.atividade'),
            preserve_default=False,
        ),
    ]
