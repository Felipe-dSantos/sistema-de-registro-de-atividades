from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.urls import reverse
from multiupload.fields import MultiFileField
# Signals
from django.db.models import signals
from django.template.defaultfilters import slugify


class Local(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class Atividade(models.Model):
    tema = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    descricao = models.TextField()
    local = models.ForeignKey(Local, on_delete=models.CASCADE)
    quantidade_ptc = models.IntegerField()
    data_inicio = models.DateField('Data de inicio', blank=True)
    data_encerramento = models.DateField('Data de encerramento')
    duracao = models.CharField(max_length=20)
    arquivos = models.FileField(upload_to='arquivos/')
    # calcula o intervalo entre a data de inicio e data de encerramento de uma atividade

    def duracao(self):
        duracao = self.data_encerramento - self.data_inicio
        return duracao.days

    def __str__(self):
        return f"{self.tema} , Local: {self.local} Data de inicio: {self.data_inicio} - Data de encerramento: {self.data_encerramento}"

    def get_arquivos(self):
        return self.arquivo.all()

    def get_arquivos(self):
        return self.arquivos.name  # Retorna o nome do arquivo

    def get_absolute_url(self):
        return reverse('exibir-relatorio', args=[str(self.id)])



# class CustomUser(AbstractUser):
#     cpf = models.CharField(max_length=14, unique=True)
#     USERNAME_FIELD = 'cpf'
#     user_permissions = models.ManyToManyField(
#         Permission,
#         verbose_name=('permissions'),
#         blank=True,
#         related_name='custom_user_set',
#     )
#     groups = models.ManyToManyField(
#         Group,
#         verbose_name=('groups'),
#         blank=True,
#         related_name='custom_user_set',
#         help_text=(
#             'The groups this user belongs to. A user will get all permissions '
#             'granted to each of their groups.'
#         ),
#     )

#     def __str__(self):
#         return self.username