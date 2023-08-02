from django.shortcuts import render, redirect
from .models import Atividade
from .forms import AtividadeForm

# Create your views here.
def home(request):
    data = {'mensagem': 'inicio'}
    return render(request, 'core/index.html', data)


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
    

def exibir_relatorio(request):
    atividades = Atividade.objects.all()
    data = {'atividades': atividades}
    return render(request, 'core/exibir_relatorio.html', data)