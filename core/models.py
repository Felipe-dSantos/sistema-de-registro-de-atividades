from django.db import models
from datetime import date
from django.contrib.auth.models import User

#Signals
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
    arquivos = models.FileField(upload_to='arquivos/')
    
    # calcula o intervalo entre a data de inicio e data de encerramento de uma atividade
    def duracao(self):
        duracao = self.data_encerramento - self.data_inicio
        return duracao.days 
    

    def __str__(self):
        return f"{self.tema} , Local: {self.local} Data de inicio: {self.data_inicio} - Data de encerramento: {self.data_encerramento}"

    
class PDFModel(models.Model):
    pdf_file = models.FileField(upload_to='pdfs/')