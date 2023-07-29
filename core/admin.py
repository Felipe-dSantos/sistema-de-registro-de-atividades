from django.contrib import admin
from .models import Professor, Atividade, Local


class ListaAtividades(admin.ModelAdmin):
    list_display = ('tema', 'nome_responsavel', 'local', 'data_inicio', 'data_encerramento', 'duracao', 'status')


# Register your models here.
admin.site.register(Professor) 
admin.site.register(Atividade, ListaAtividades) 
admin.site.register(Local) 