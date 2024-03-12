from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import ChangePasswordView, CustomLoginView, Home, LocalList, AtividadeList, AtividadeGeralList

from core import  views as v
from . import views
from .views import (
     LocalCreate,
     AtividadeCreate,
     LocalUpdate,
     AtividadeUpdate,
     LocalDelete,
     AtividadeDelete,
     CustomLoginRedirectView,
     UsuarioCreate,
     
)
  # urls
urlpatterns = [
    # url de login e logout
    path('login/', CustomLoginView.as_view(
        template_name='core/usuarios/login.html'
    ), name="login"),
    path('custom_login_redirect/', CustomLoginRedirectView.as_view(),
         name='custom_login_redirect'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registrar/', UsuarioCreate.as_view(), name='registrar-usuario'),
    path('home/', Home.as_view(), name= 'home'),
    # create 
    path('cadastro-atividade/', AtividadeCreate.as_view(),
         name='cadastro-atividade'),
    path('cadastro-local/', LocalCreate.as_view(), name='cadastro-local'),
    # update 
    path('editar/local/<int:pk>', LocalUpdate.as_view(), name='editar-local'),
    path('editar/atividade/<int:pk>',
         AtividadeUpdate.as_view(), name='editar-atividade'),
    # delete 
    path('excluir/local/<int:pk>', LocalDelete.as_view(), name='excluir-local'),
    path('excluir/atividade/<int:pk>',
         AtividadeDelete.as_view(), name='excluir-atividade'),
    # list 
    path('listar/locais/', LocalList.as_view(), name='listar-local'),
    path('listar/atividades/', AtividadeList.as_view(), name='listar-atividade'),
    path('listar/atividadesGerais/', AtividadeGeralList.as_view(),
         name='listar-atividade-geral'),

    path('export-pdf/', views.export_pdf, name='export-pdf'),
    path('relatorio/<int:pk>/gerar_pdf/',
         views.gerar_pdf_relatorio, name='gerar-pdf-relatorio'),
    path('relatorio/<int:pk>/', views.exibir_relatorio, name='exibir-relatorio'),

    path('alterar-senha/', ChangePasswordView.as_view(), name='alterar_senha'),

    path('password_reset/', v.MyPasswordReset.as_view(), name='password_reset'),  # noqa E501
    path('password_reset/done/', v.MyPasswordResetDone.as_view(), name='password_reset_done'),  # noqa E501
    path('reset/<uidb64>/<token>/', v.MyPasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', v.MyPasswordResetComplete.as_view(), name='password_reset_complete'),

]
