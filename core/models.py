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
    # calcula o intervalo entre a data de inicio e data de encerramento de uma atividade


    def __str__(self):
        return f"{self.tema} , Local: {self.local} Data de inicio: {self.data_inicio} - Data de encerramento: {self.data_encerramento}"

    def get_absolute_url(self):
        return reverse('exibir-relatorio', args=[str(self.id)])



class Arquivo(models.Model):
    arquivo = models.FileField(upload_to='arquivos/')
    Atividade = models.ForeignKey(Atividade, related_name='arquivo', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.arquivo.name 
    
    
    def is_doc(self):
        return self.arquivo.name.lower().endswith('.doc') or self.arquivo.name.lower().endswith('.docx')

    def is_pdf(self):
        return self.arquivo.name.lower().endswith('.pdf')

    def is_image(self):
        return self.arquivo.name.lower().endswith('.png') or self.arquivo.name.lower().endswith('.jpg') or self.arquivo.name.lower().endswith('.jpeg') or self.arquivo.name.lower().endswith('.gif') or self.arquivo.name.lower().endswith('.bmp')
