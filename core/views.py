from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Local, Atividade
from django.urls import reverse_lazy


# Create views.
def home(request):
    data = {'mensagem': 'inicio'}
    return render(request, 'core/index.html', data)


def lista_atividades(request):
    atividades = Atividade.objects.all()
    # form = AtividadeForm()
    data = {'atividades': atividades}
    #  data = {'atividades': atividades , 'form': form}
    return render(request, 'core/lista_atividades.html', data)

# def nova_atividade(request):
#     form = AtividadeForm(request.POST or None)
#     if form.is_valid():
#         form.save()
    # return redirect('core_lista_atividades')


def exibir_relatorio(request):
    atividades = Atividade.objects.all()
    data = {'atividades': atividades}
    return render(request, 'core/exibir_relatorio.html', data)

################### CREATE #########################


class LocalCreate(CreateView):
    model = Local
    fields = ['nome']
    template_name = 'core/registros/form.html'
    success_url = reverse_lazy('listar-local')


class AtividadeCreate(CreateView):
    model = Atividade
    fields = ['tema', 'nome_responsavel', 'descricao', 'local',
              'quantidade_ptc', 'data_inicio', 'data_encerramento']
    template_name = 'core/registros/form.html'
    success_url = reverse_lazy('listar-atividade')

################### UPDATE #########################


class LocalUpdate(UpdateView):
    model = Local
    fields = ['nome']
    template_name = 'core/registros/form.html'
    success_url = reverse_lazy('listar-local')


class AtividadeUpdate(UpdateView):
    model = Atividade
    fields = ['tema', 'nome_responsavel', 'descricao', 'local',
              'quantidade_ptc', 'data_inicio', 'data_encerramento']
    template_name = 'core/registros/form.html'
    success_url = reverse_lazy('listar-atividade')

################### Delete #########################


class LocalDelete(DeleteView):
    model = Local
    template_name = 'core/registros/form_excluir.html'
    success_url = reverse_lazy('listar-local')


class AtividadeDelete(DeleteView):
    model = Atividade
    template_name = 'core/registros/form_excluir.html'
    success_url = reverse_lazy('listar-atividade')

    ################### Read #########################


class LocalList(ListView):
    model = Local
    template_name = 'core/listas/Local.html'


class AtividadeList(ListView):
    model = Atividade
    template_name = 'core/listas/Atividade.html'
