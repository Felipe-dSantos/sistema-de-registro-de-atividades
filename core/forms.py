from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms.widgets import DateInput # need to import
from multiupload.fields import MultiFileField

from .models import Arquivo, Atividade
from django import forms
from .models import Atividade

class UsuarioForm(UserCreationForm):
    email = forms.EmailField(max_length=100)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def clean_email(self):
        e = self.cleaned_data['email']
        if User.objects.filter(email=e).exists():
            raise ValidationError("o email {} já está em uso.".format(e))
        return e

class AtividadeForm(forms.ModelForm):

    class Meta:
        model = Atividade
        fields = '__all__'

class ArquivoForm(forms.ModelForm):
    class Meta:
        model = Arquivo
        fields = ('arquivo', )

ArquivoFormSet = forms.inlineformset_factory(Atividade, Arquivo, form=ArquivoForm, extra=1)
