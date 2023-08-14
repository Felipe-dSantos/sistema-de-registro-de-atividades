from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Local, Atividade
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
 

# Create views.

def exibir_relatorio(request):
    atividades = Atividade.objects.all()
    data = {'atividades': atividades}
    return render(request, 'core/exibir_relatorio.html', data)

################### CREATE #########################


class LocalCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Local
    fields = ['nome']
    template_name = 'core/registros/form.html'
    success_url = reverse_lazy('listar-local')


class AtividadeCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Atividade
    fields = ['tema', 'nome_responsavel', 'descricao', 'local',
              'quantidade_ptc', 'data_inicio', 'data_encerramento']
    template_name = 'core/registros/form.html'
    success_url = reverse_lazy('listar-atividade')

################### UPDATE #########################


class LocalUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Local
    fields = ['nome']
    template_name = 'core/registros/form.html'
    success_url = reverse_lazy('listar-local')


class AtividadeUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Atividade
    fields = ['tema', 'nome_responsavel', 'descricao', 'local',
              'quantidade_ptc', 'data_inicio', 'data_encerramento']
    template_name = 'core/registros/form.html'
    success_url = reverse_lazy('listar-atividade')

################### Delete #########################


class LocalDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Local
    template_name = 'core/registros/form_excluir.html'
    success_url = reverse_lazy('listar-local')


class AtividadeDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Atividade
    template_name = 'core/registros/form_excluir.html'
    success_url = reverse_lazy('listar-atividade')

    ################### Read #########################


class LocalList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Local
    template_name = 'core/listas/Local.html'


class AtividadeList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Atividade
    template_name = 'core/listas/Atividade.html'
