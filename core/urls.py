from django.contrib import admin
from django.urls import path, include
from .views import home, lista_atividades

urlpatterns = [
    path('', home, name='core_home'),
    path('atividades/', lista_atividades, name='core_lista_atividades'),
]
