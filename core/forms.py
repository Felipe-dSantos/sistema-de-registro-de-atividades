from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms.widgets import DateInput # need to import

from .models import Atividade

from django import forms
from .models import Atividade

class UsuarioForm(UserCreationForm):
    email = forms.EmailField(max_length=100)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def clean_email(self):
        e = self.changed_data['email']
        if User.objects.filter(email=e).exists():
            raise ValidationError("o email {} já está em uso.".format(e))
        return e

# class DateInput(forms.DateInput):
#     input_type = 'date'

class AtividadeForm(forms.ModelForm):
    class Meta:
        model = Atividade
        fields = '__all__'
        
        # widgets = {
        #     'data_inicio': DateInput(attrs={'type': 'date'}),
        #     'data_encerramento': DateInput(attrs={'type': 'date'}),
        # }