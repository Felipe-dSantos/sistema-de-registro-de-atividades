from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Atividade,Local
from .forms import AtividadeForm

# Create your views here.
def home(request):
    context = {'mensagem': 'Ola mundo'}
    return render(request, 'core/index.html', context)


def lista_atividades(request):
    atividades = Atividade.objects.all()
    form = AtividadeForm()
    data = {'atividades': atividades , 'form': form}
    return render(request, 'core/lista_atividades.html',data)


def nova_atividade(request):
    form = AtividadeForm(request.POST or None)
    if form.is_valid():
        form.save()
    return redirect('core_lista_atividades')
    


    # return response 
def exibir_relatorio(request):
    # Obter as atividades do banco de dados (por exemplo, todas as atividades)
    atividades = Atividade.objects.all()


    # Enviar as atividades para o template como contexto
    context = {'atividades': atividades}
    return render(request, 'core/exibir_relatorio.html', context)