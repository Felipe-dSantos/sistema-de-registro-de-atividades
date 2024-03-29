from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.filters import SimpleListFilter
from calendar import month_name
from core.forms import AtividadeForm
from .models import Arquivo, Atividade, Local
from django.db.models import Q
from django.contrib.auth.admin import UserAdmin

from core.forms import CustomUsuarioCreateForm, CustomUsuarioChangeForm
from .models import CustomUsuario


@admin.register(CustomUsuario)
class CustomUsuarioAdmin(UserAdmin):
    add_form = CustomUsuarioCreateForm
    form = CustomUsuarioChangeForm
    model = CustomUsuario
    list_display = ('id', 'cpf' , 'first_name', 'last_name', 'get_groups_display',  'is_staff')
    fieldsets = (
        (None, {'fields': ('cpf',  'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions' )}),
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
        
    )
    def get_groups_display(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    
    get_groups_display.short_description = 'Grupos'


class MesFilter(SimpleListFilter):
    title = 'Mês'
    parameter_name = 'mes'

    def lookups(self, request, model_admin):
        
        meses_pt_br = [
            ('1', 'Janeiro'),
            ('2', 'Fevereiro'),
            ('3', 'Março'),
            ('4', 'Abril'),
            ('5', 'Maio'),
            ('6', 'Junho'),
            ('7', 'Julho'),
            ('8', 'Agosto'),
            ('9', 'Setembro'),
            ('10', 'Outubro'),
            ('11', 'Novembro'),
            ('12', 'Dezembro'),
        ]
        return meses_pt_br

    def queryset(self, request, queryset):
       if self.value():
            mes_selecionado = int(self.value())
            return queryset.filter(
                Q(data_inicio__month=mes_selecionado) | Q(data_encerramento__month=mes_selecionado)
            )
class ArquivoInline(admin.TabularInline):
    model = Arquivo
    extra = 3
    
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ('id', 'tema', 'get_full_name', 'descricao', 'local', 'quantidade_ptc', 'data_inicio', 'data_encerramento', 'duracao')
    list_filter = ('local', MesFilter)
    inlines = [ArquivoInline]

    def get_full_name(self, obj):
        return obj.usuario.get_full_name()

    get_full_name.short_description = 'Nome do responsável'
    



# Register your models here.
admin.site.register(Atividade, AtividadeAdmin) 
admin.site.register(Local) 

