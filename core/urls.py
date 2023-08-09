from django.contrib import admin
from django.urls import path
from .views import (
    home,
    lista_atividades,
    exibir_relatorio,
    nova_atividade, 

)

urlpatterns = [
    path('', home, name='core_home'),
    path('atividades/', lista_atividades, name='core_lista_atividades'),
    path('nova_atividade/', nova_atividade, name='core_nova_atividade'),
    path('relatorio/', exibir_relatorio, name='core_exibir_relatorio'),
]
