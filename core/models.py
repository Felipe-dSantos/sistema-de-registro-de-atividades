from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def normalize_cpf(self, cpf):
        # Remove caracteres especiais
        cpf = ''.join(filter(str.isdigit, str(cpf)))

        # Verifica se o CPF possui 11 dígitos
        if len(cpf) != 11:
            raise ValueError('CPF deve conter 11 dígitos após a normalização')

        return cpf

    def _create_user(self, cpf, password, **extra_fields):
        if not cpf:
            raise ValueError('O cpf é obrigatório')

        cpf = self.normalize_cpf(cpf)
        user = self.model(cpf=cpf, username=cpf, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, cpf, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(cpf, password, **extra_fields)

    def create_superuser(self, cpf, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True')
        return self._create_user(cpf, password, **extra_fields)


class CustomUsuario(AbstractUser):
    cpf = models.CharField(max_length=14,
                           verbose_name=_('CPF'),
                           unique=True
                           )
    is_staff = models.BooleanField('Membro da equipe',
                                   default=False)

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['first_name', 'last_name', ]

    def __str__(self):
        return self.cpf
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    objects = UsuarioManager()


class Local(models.Model):
    nome = models.CharField(max_length=50)
    def __str__(self):
        return self.nome


class Atividade(models.Model):
    tema = models.CharField(max_length=50)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                on_delete=models.CASCADE
                                )
    descricao = models.TextField()
    local = models.ForeignKey(Local, on_delete=models.CASCADE)
    quantidade_ptc = models.PositiveIntegerField()
    data_inicio = models.DateField('Data de inicio')
    data_encerramento = models.DateField('Data de encerramento')
    duracao = models.CharField(max_length=20)
    data_registro = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.tema
    
    def get_usuario_nome_completo(self):
        return self.usuario.get_full_name() if self.usuario else "Usuário sem nome"

    def get_absolute_url(self):
        return reverse('exibir-relatorio', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if not self.id:
            self.data_registro = timezone.now()
        super(Atividade, self).save(*args, **kwargs)


class Arquivo(models.Model):
    arquivo = models.FileField(upload_to='arquivos/')
    Atividade = models.ForeignKey(
        Atividade, related_name='arquivo', 
        on_delete=models.CASCADE
        )

    def __str__(self):
        return self.arquivo.name

    def is_doc(self):
        return self.arquivo.name.lower().endswith('.doc') or self.arquivo.name.lower().endswith('.docx')

    def is_pdf(self):
        return self.arquivo.name.lower().endswith('.pdf')

    def is_image(self):
        return self.arquivo.name.lower().endswith('.png') or self.arquivo.name.lower().endswith('.jpg') or self.arquivo.name.lower().endswith('.jpeg') or self.arquivo.name.lower().endswith('.gif') or self.arquivo.name.lower().endswith('.bmp')
