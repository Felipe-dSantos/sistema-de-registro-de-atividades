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


# class UsuarioForm(UserCreationForm):
#     email = forms.EmailField(max_length=100)
    
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
#     def clean_email(self):
#         e = self.cleaned_data['email']
#         if User.objects.filter(email=e).exists():
#             raise ValidationError("o email {} já está em uso.".format(e))
#         return e

class AtividadeForm(forms.ModelForm):

    class Meta:
        model = Atividade
        fields = ['descricao']
        widgets = {
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 5})  # Defina o número de linhas aqui
        }

   
class ArquivoForm(forms.ModelForm):
    class Meta:
        model = Arquivo
        fields = ('arquivo', )

ArquivoFormSet = forms.inlineformset_factory(Atividade, Arquivo, form=ArquivoForm, extra=1)
