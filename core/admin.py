from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.forms import AtividadeForm
from .models import Arquivo, Atividade, Local




class ListaAtividades(admin.ModelAdmin):
    form = AtividadeForm
    list_display = ('id', 'tema', 'usuario', 'descricao', 'local', 'quantidade_ptc', 'data_inicio', 'data_encerramento', 'duracao')

class ArquivoInline(admin.TabularInline):
    model = Arquivo
    extra = 2
    
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ('id', 'tema', 'usuario', 'descricao', 'local', 'quantidade_ptc', 'data_inicio', 'data_encerramento', 'duracao')
    inlines = [
        ArquivoInline
    ]

# Register your models here.
admin.site.register(Atividade, AtividadeAdmin) 
admin.site.register(Local) 
