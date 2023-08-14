from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import LocalList, AtividadeList
from .views import (
    exibir_relatorio,
    LocalCreate,
    AtividadeCreate,
    LocalUpdate,
    AtividadeUpdate,
    LocalDelete,
    AtividadeDelete,
)

urlpatterns = [
    #url de login e logout
    path('login/', auth_views.LoginView.as_view(
        template_name='core/usuarios/login.html'
    ), name="login"),
     path('logout/', auth_views.LogoutView.as_view() , name='logout'),
    
    path('relatorio/', exibir_relatorio, name='core_exibir_relatorio'),
    path('cadastro-atividade/', AtividadeCreate.as_view(), name='cadastro-atividade'),
    path('cadastro-local/', LocalCreate.as_view(), name='cadastro-local'),
    #update views
    path('editar/local/<int:pk>', LocalUpdate.as_view(), name='editar-local'),
    path('editar/atividade/<int:pk>', AtividadeUpdate.as_view(), name='editar-atividade'),
    #delete views
    path('excluir/local/<int:pk>', LocalDelete.as_view(), name='excluir-local'),
    path('excluir/atividade/<int:pk>', AtividadeDelete.as_view(), name='excluir-atividade'),
    #list views
    path('listar/locais/', LocalList.as_view(), name='listar-local'),
    path('listar/atividades/', AtividadeList.as_view() , name='listar-atividade'),
    
]
