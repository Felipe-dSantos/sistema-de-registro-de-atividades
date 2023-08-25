from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from .forms import CustomUserCreateForm, CustomUserChangeForm
# from .models import CustomUser
from .models import Atividade, Local

# @admin.register(CustomUser)
# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreateForm
#     form = CustomUserChangeForm
#     model = CustomUser
    
#     list_display = ( 'first_name', 'last_name', 'email', 'password', 'is_staff')
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Informações Pessoais', {'fields': ('first_name', 'last_name')}),
#         ('Permições', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permission')})
        
#     )


class ListaAtividades(admin.ModelAdmin):
    list_display = ('tema', 'usuario', 'local', 'data_inicio', 'data_encerramento', 'duracao', 'status')


# Register your models here.
admin.site.register(Atividade, ListaAtividades) 
admin.site.register(Local) 