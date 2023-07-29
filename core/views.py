from django.shortcuts import render
from .models import Atividade


# Create your views here.
def home(request):
    context = {'mensagem': 'Ola mundo'}
    return render(request, 'core/index.html', context)

def lista_atividades(request):
    atividades = Atividade.objects.all()
    return render(request, 'core/lista_atividades.html', {'atividades': atividades})