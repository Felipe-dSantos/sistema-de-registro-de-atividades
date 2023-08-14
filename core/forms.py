from django.forms import ModelForm
from .models import Atividade
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm


# class CustomUserCreateForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ('first_name', 'last_name')
#         label = {'username': 'E-mail'}
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         user.cpf = self.cleaned_data["username"]
        
#         if commit:
#             user.save()
#         return user
    
# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = CustomUser
#         fields = ('first_name', 'last_name')
        
class AtividadeForm(ModelForm):
    class Meta:
        model = Atividade
        fields = '__all__'

