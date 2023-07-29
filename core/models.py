from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import math
from datetime import timedelta, date

class Professor(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14)
    data_nascimento = models.DateField(max_length=10)
    
    def __str__(self):
        return f"{self.nome} , CPF: {self.cpf}, Data de Nascimento: {self.data_nascimento}"

class Local(models.Model):
    nome = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nome
    
class Atividade(models.Model):
    tema = models.CharField(max_length=255)
    nome_responsavel = models.CharField(max_length=255)
    descricao = models.TextField()
    quantidade_ptc = models.IntegerField()
    data_inicio = models.DateField(max_length=10)
    data_encerramento = models.DateField(max_length=10)
    imagem = models.ImageField()
    local = models.ForeignKey(Local, on_delete=models.CASCADE)
    
    # calcula o intervalo entre a data de inicio e data de encerramento de uma ativida
    def duracao(self):
        duracao = self.data_encerramento - self.data_inicio
        return duracao.days
    
    def status(self):
        today = date.today()
        if self.data_encerramento < today:
            return 'Encerrada'
        else:
            return 'Em andamento'

    def __str__(self):
        return f"{self.tema} , Responsavel:{self.nome_responsavel}, Local: {self.local} Data de inicio: {self.data_inicio} - Data de encerramento: {self.data_encerramento}"