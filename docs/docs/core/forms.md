# Documentação dos Formulários do Django

## Formulário de Criação de Usuário Personalizado

A classe `CustomUsuarioCreateForm` é um formulário para a criação de novos usuários. Ela herda de `UserCreationForm` e usa o modelo `CustomUsuario`. Os campos `username`, `first_name` e `last_name` são usados para a entrada de dados. O campo `username` é rotulado como 'CPF'. O método `save` foi sobrescrito para definir a senha do usuário e o CPF.

```

class CustomUsuarioCreateForm(UserCreationForm):

    class Meta:
        model = CustomUsuario
        fields = ('username','first_name', 'last_name')
        labels = {'username': 'CPF',}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Altere o help_text do campo de senha
        self.fields['username'].help_text = ''
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.cpf = self.cleaned_data["username"]
        if commit:
            user.save()
        return user
    

```

## Formulário de Alteração de Usuário Personalizado

A classe `CustomUsuarioChangeForm` é um formulário para a alteração de usuários existentes. Ela herda de `UserChangeForm` e usa o modelo `CustomUsuario`. Os campos `first_name` e `last_name` são usados para a entrada de dados.
```

class CustomUsuarioChangeForm(UserChangeForm):
    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name')


```
## Formulário de Atividade

A classe `AtividadeForm` é um formulário para a criação e alteração de atividades. Ela usa o modelo `Atividade` e os campos `descricao` e `local` para a entrada de dados. O campo `descricao` é uma área de texto com 5 linhas e o campo `local` é um campo de seleção.
```
class AtividadeForm(forms.ModelForm):

    class Meta:
        model = Atividade
        fields = ['descricao', 'local']
        widgets = {
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),  # Defina o número de linhas aqui
            'local': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Selecione o local'})
        }


```
## Formulário de Arquivo

A classe `ArquivoForm` é um formulário para a criação e alteração de arquivos. Ela usa o modelo `Arquivo` e o campo `arquivo` para a entrada de dados.
```
   
class ArquivoForm(forms.ModelForm):
    class Meta:
        model = Arquivo
        fields = ('arquivo', )


```
## Formulário de Conjunto de Formulários de Arquivo

`ArquivoFormSet` é um conjunto de formulários para a criação e alteração de múltiplos arquivos associados a uma atividade. Ele usa a função `inlineformset_factory` para criar o conjunto de formulários, com `Atividade` como o modelo principal, `Arquivo` como o modelo secundário e `ArquivoForm` como o formulário base.
```
ArquivoFormSet = forms.inlineformset_factory(Atividade, Arquivo, form=ArquivoForm, extra=1)
```