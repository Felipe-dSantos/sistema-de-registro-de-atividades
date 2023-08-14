from django.db import models
from datetime import date
# from django.contrib.auth.models import BaseUserManager, AbstractUser
# from django.contrib.auth.models import User, UserManager

# Create Models
# class UserManager(BaseUserManager):
#     use_in_migrations = True
    
    # def normalize_cpf(cpf):
    #     # # Remove quaisquer caracteres não numéricos do CPF
    #     # cpf = ''.join(filter(str.isdigit, cpf))
    
    #     # # Garante que o CPF tenha 11 dígitos
    #     # cpf = cpf.zfill(11)
    
    #     # return cpf
#     def _create_user(self, email, password, **extra_fields):
        
#         email = self.normalize_email(email)
#         user = self.model(email=email, username=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
    
#     def create_user(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(email, password, **extra_fields)
    
#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_staff', True)
        
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser precisa ter is_superuser=True')
        
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser precisa ter is_staff=True')
        
#         return self._create_user(email, password, **extra_fields)
        
# class CustomUser(AbstractUser):
#     email = models.EmailField('E-mail', unique=True)
    
#     is_staff = models.BooleanField('Membro da equipe', default=True)
    
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']
    
#     def __str__(self):
#         return self.cpf
    
#     objects = UserManager()
    
class Local(models.Model):
    nome = models.CharField(max_length=255)
    def __str__(self):
        return self.nome
    
    
class Atividade(models.Model):
    tema = models.CharField(max_length=255)
    nome_responsavel = models.CharField(max_length=255)
    descricao = models.TextField()
    local = models.ForeignKey(Local, on_delete=models.CASCADE)
    quantidade_ptc = models.IntegerField()
    data_inicio = models.DateField(max_length=10)
    data_encerramento = models.DateField(max_length=10)
    # arquivo = models.FileField(upload_to='arquivos/')
    
    # calcula o intervalo entre a data de inicio e data de encerramento de uma atividade
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
