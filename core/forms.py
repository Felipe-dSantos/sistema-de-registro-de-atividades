from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Arquivo, Atividade, CustomUsuario
from django import forms
from .models import Atividade
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class CustomUsuarioCreateForm(UserCreationForm):
    # cpf = forms.CharField(label='CPF')
    class Meta:
        model = CustomUsuario
        fields = ('username','first_name', 'last_name')
        labels = {'username': 'CPF',}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Altere o help_text do campo de senha
        self.fields['username'].help_text = 'Digite um CPF valido.'
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.cpf = self.cleaned_data["username"]
        if commit:
            user.save()
        return user
    

class CustomUsuarioChangeForm(UserChangeForm):
    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name')

class AtividadeForm(forms.ModelForm):

    class Meta:
        model = Atividade
        fields = ['descricao', 'local']
        widgets = {
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),  # Defina o número de linhas aqui
            'local': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Selecione o local'})
        }

   
class ArquivoForm(forms.ModelForm):
    class Meta:
        model = Arquivo
        fields = ('arquivo', )

ArquivoFormSet = forms.inlineformset_factory(Atividade, Arquivo, form=ArquivoForm, extra=1)
