from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Arquivo, Atividade, CustomUsuario
from django import forms
from .models import Atividade
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class CustomUsuarioCreateForm(UserCreationForm):
    # first_name = forms.CharField(label='Primeiro nome*')
    # last_name = forms.CharField(label='Sobrenome*')

    class Meta:
        model = CustomUsuario
        fields = ('username','first_name', 'last_name')
        labels = {'username': 'CPF',}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Altere o help_text do campo de senha
        self.fields['username'].help_text = ''
    #     self.fields['first_name'].label = 'Primeiro nome*'
    #     self.fields['last_name'].label = 'Sobrenome*'
        
    # def clean(self):
    #     cleaned_data = super().clean()
    #     first_name = cleaned_data.get('first_name')
    #     last_name = cleaned_data.get('last_name')

    #     if not first_name:
    #         self.add_error('first_name', 'Este campo é obrigatório.')
    #     if not last_name:
    #         self.add_error('last_name', 'Este campo é obrigatório.')

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
