from django.forms import ModelForm
from .models import Atividade 

class AtividadeForm(ModelForm):
    class Meta:
        model = Atividade
        fields = '__all__'
        