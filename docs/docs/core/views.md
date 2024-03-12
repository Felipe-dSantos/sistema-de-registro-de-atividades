# Documentação das Views do Django

## Importações

O código começa com a importação de vários módulos e funções necessárias para o funcionamento das views.

### Módulos Padrão

- `logging`: Usado para registrar eventos que acontecem durante a execução do código.
- `django.contrib.auth.models.User`: O modelo de usuário padrão do Django.
- `.models.Atividade, Arquivo, CustomUsuario`: Modelos personalizados definidos no arquivo `models.py`.
- `django.views.generic.TemplateView`: Uma view baseada em classe para exibir um template.
- `reportlab.*`: Várias funções e classes do ReportLab para a criação de PDFs.
- `django.contrib.auth.views.*`: Várias views para a funcionalidade de redefinição de senha.
- `weasyprint.HTML, CSS`: Classes para a geração de PDFs a partir de HTML e CSS.
- `datetime`: Módulo para trabalhar com datas e horas.

### Módulos do Django

- `django.http.HttpResponse, request`: Classes para lidar com respostas HTTP e solicitações.
- `django.shortcuts.render, get_object_or_404, redirect`: Funções de atalho para renderizar templates, obter um objeto ou 404, e redirecionar para uma nova URL.
- `django.urls.reverse, reverse_lazy`: Funções para reverter URLs a partir de nomes de URL.
- `django.contrib.auth.models.Group`: O modelo de grupo padrão do Django para lidar com permissões.
- `django.template.loader.render_to_string`: Função para renderizar um template em uma string.
- `django.core.files.File`: Classe para lidar com arquivos.
- `django.views.decorators.csrf.csrf_exempt`: Decorador para isentar uma view da proteção CSRF.

### Módulos de Terceiros

- `weasyprint`: Biblioteca para a geração de PDFs a partir de HTML e CSS.
- `braces.views.GroupRequiredMixin`: Mixin para exigir que um usuário pertença a um grupo específico para acessar uma view.

### Importações Locais

- `.models.Local, Atividade`: Modelos personalizados definidos no arquivo `models.py`.

## Registro e Autenticação de Usuários

### Registro de Usuários

A classe `UsuarioCreate` é uma view baseada em classe para o registro de novos usuários. Ela usa o `CustomUsuarioCreateForm` para a entrada de dados e redireciona para a página de login após um registro bem-sucedido. Se o formulário for válido, o novo usuário é adicionado ao grupo "Docente".
```
class UsuarioCreate(CreateView):
    template_name = 'core/usuarios/form.html'
    form_class = CustomUsuarioCreateForm
    success_url = reverse_lazy('login')
    success_message = 'Usuário cadastrado com Sucesso!'

    def form_valid(self, form):

        grupo = get_object_or_404(Group, name="Docente")
        url = super().form_valid(form)
        self.object.groups.add(grupo)
        self.object.save()
        messages.success(self.request, self.success_message)

        return url

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Cadastro de Usuário"
        context['botao'] = "Cadastrar"
        return context
```
### Redefinição de Senha

As classes `MyPasswordReset` e `MyPasswordResetDone` são views baseadas em classe para a funcionalidade de redefinição de senha. Elas usam templates personalizados para a exibição.

```
class MyPasswordReset(PasswordResetView):
    template_name = 'core/usuarios/password_reset_form.html'
    ...

class MyPasswordResetDone(PasswordResetDoneView):
   
    template_name = 'core/usuarios/password_reset_done.html'
    ...
```

### Confirmação de Redefinição de Senha

A classe `MyPasswordResetConfirm` é uma view baseada em classe para a funcionalidade de confirmação de redefinição de senha. Ela usa o template `core/usuarios/password_reset_confirm.html`. Quando o formulário é válido, a senha do usuário é atualizada e uma mensagem de sucesso é exibida.
```
class MyPasswordResetConfirm(PasswordResetConfirmView):
    
    template_name = 'core/usuarios/password_reset_confirm.html'

    def form_valid(self, form):
        self.user.is_active = True
        self.user.save()
        messages.success(self.request, 'Sua senha foi atualizada com sucesso!')
        return super(MyPasswordResetConfirm, self).form_valid(form)
```
### Conclusão da Redefinição de Senha

A classe `MyPasswordResetComplete` é uma view baseada em classe que é exibida quando a redefinição de senha é concluída com sucesso. Ela usa o template `core/usuarios/password_reset_complete.html`.
```
class MyPasswordResetComplete(PasswordResetCompleteView):
   
    template_name = 'core/usuarios/password_reset_complete.html'
    ...

```
### Alteração de Senha

A classe `ChangePasswordView` é uma view baseada em classe para a funcionalidade de alteração de senha. Ela usa o `PasswordChangeForm` para a entrada de dados e redireciona para a página de listagem de atividades após uma alteração de senha bem-sucedida. Se o formulário for válido, a senha do usuário é atualizada e uma mensagem de sucesso é exibida.
```
class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = 'core/usuarios/change_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('listar-atividade')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, 'Sua senha foi atualizada com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Alterar Senha"
        context['botao'] = "Alterar minha Senha"
        context['url'] = reverse('listar-atividade')
        context['breadcrumb'] = [
            {'title': 'Inicio', 'url': '/home/'},
            {'title': 'alterar senha', 'url': '/alterar_senha/'},

        ]
        return context
```
### Redirecionamento Personalizado de Login

A classe `CustomLoginRedirectView` é uma view baseada em classe que redireciona os usuários após o login com base no grupo ao qual pertencem.

- Se o usuário pertencer ao grupo "Tecnico", ele será redirecionado para a página 'listar-atividade-geral'.
- Se o usuário pertencer ao grupo "Docente", ele será redirecionado para a página 'home'.
- Se o usuário não pertencer a nenhum desses grupos, ele será redirecionado para a página 'home' por padrão.
```
class CustomLoginRedirectView(View):
    def get(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Tecnico').exists():

            return redirect('listar-atividade-geral')
        elif request.user.groups.filter(name='Docente').exists():

            return redirect('home')
        else:
            return redirect('home')

```

## Página Inicial

A classe `Home` é uma view baseada em classe para exibir a página inicial. Ela usa o template `core/home/home.html`.
```

class Home(TemplateView):
    template_name = 'core/home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'title': 'Inicio', 'url': '/home/'},
        ]
        return context

```
## CRUD de Locais

### Criação de Local

A classe `LocalCreate` é uma view baseada em classe para a criação de novos locais. Ela usa o modelo `Local` e o campo `nome` para a entrada de dados. A view redireciona para a página de listagem de locais após a criação bem-sucedida de um local. A view requer que o usuário esteja logado e seja um membro do grupo "Administrador".
```
class LocalCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = u"Administrador"
    model = Local
    fields = ['nome']
    template_name = 'core/registros/form.html'
    success_url = reverse_lazy('listar-local')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Cadastro de Local"
        context['botao'] = "Cadastrar"
        return context

```
### Atualização de Local

A classe `LocalUpdate` é uma view baseada em classe para a atualização de locais existentes. Ela usa o modelo `Local` e o campo `nome` para a entrada de dados. A view redireciona para a página de listagem de locais após a atualização bem-sucedida de um local. A view requer que o usuário esteja logado e seja um membro do grupo "Administrador".
```
class LocalUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = u"Administrador"
    model = Local
    fields = ['nome']
    template_name = 'core/registros/form.html'
    success_url = reverse_lazy('listar-local')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Editar Local"
        context['botao'] = "Salvar"
        context['url'] = reverse('listar-local')

        return context

```
### Exclusão de Local

A classe `LocalDelete` é uma view baseada em classe para a exclusão de locais. Ela usa o modelo `Local` para identificar o local a ser excluído. A view redireciona para a página de listagem de locais após a exclusão bem-sucedida de um local. A view requer que o usuário esteja logado e seja um membro do grupo "Administrador".
```
class LocalDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = u"Administrador"
    model = Local
    template_name = 'core/registros/form_excluir.html'
    success_url = reverse_lazy('listar-local')
```
### Listagem de Locais

A classe `LocalList` é uma view baseada em classe para a listagem de locais. Ela usa o modelo `Local` para obter a lista de locais a serem exibidos. A view requer que o usuário esteja logado e seja um membro dos grupos "Administrador" ou "Docente".

```
class LocalList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador", u"Docente"]
    model = Local
    template_name = 'core/listas/Local.html'
```
#CRUD de Atividades
## Criação de Atividade

A classe `AtividadeCreate` é uma view baseada em classe para a criação de novas atividades. Ela usa o modelo `Atividade` e os campos `tema`, `descricao`, `local`, `quantidade_ptc`, `data_inicio`, `data_encerramento` e `duracao` para a entrada de dados. A view redireciona para a página de listagem de atividades após a criação bem-sucedida de uma atividade. A view requer que o usuário esteja logado.
```

class AtividadeCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Atividade
    fields = ['tema', 'descricao', 'local', 'quantidade_ptc',
              'data_inicio', 'data_encerramento', 'duracao']
    template_name = 'core/registros/form-upload.html'
    success_url = reverse_lazy('listar-atividade')
    success_message = 'Atividade registrada com Sucesso!'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Registro de Atividade"
        context['botao'] = "Registrar"
        context['url'] = reverse('listar-atividade')
        context['breadcrumb'] = [
            {'title': 'Inicio', 'url': '/home/'},
            {'title': 'Atividades', 'url': '/listar/atividades/'},
            {'title': 'Registro de atividade', 'url': '/cadastro-atividade/'},
        ]
        # Cria formset de Arquivos relacionados à Atividade
        ArquivoFormSet = inlineformset_factory(
            Atividade, Arquivo, fields=['arquivo',], extra=3)
        if self.request.POST:
            # Se dados forem submetidos, popula os formulários com os dados enviados
            context['formset'] = ArquivoFormSet(
                self.request.POST, self.request.FILES)
        else:
            # Se não, cria um formset vazio
            context['formset'] = ArquivoFormSet()
        return context
    #validação de formulario
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        url = super().form_valid(form)
        messages.success(self.request, self.success_message)
        #salva os arquivos associados à atividade
        formset = ArquivoFormSet(
            self.request.POST, self.request.FILES, instance=self.object)
        if formset.is_valid():
            formset.save()
        return url
```
## Atualização de Atividade

A classe `AtividadeUpdate` é uma view baseada em classe para a atualização de atividades existentes. Ela usa o modelo `Atividade` e os campos `tema`, `descricao`, `local`, `quantidade_ptc`, `data_inicio`, `data_encerramento` e `arquivo` para a entrada de dados. A view redireciona para a página de listagem de atividades após a atualização bem-sucedida de uma atividade. A view requer que o usuário esteja logado.
```

class AtividadeUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Atividade
    fields = ['tema', 'descricao', 'local', 'quantidade_ptc',
              'data_inicio', 'data_encerramento', 'arquivo']
    template_name = 'core/registros/form-upload.html'
    success_url = reverse_lazy('listar-atividade')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        self.object = get_object_or_404(
            Atividade, pk=pk, usuario=self.request.user)
        return self.object

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Editar Registro de Atividade"
        context['botao'] = "Salvar"
        context['url'] = reverse('listar-atividade')
        return context


```
## Exclusão de Atividade

A classe `AtividadeDelete` é uma view baseada em classe para a exclusão de atividades. Ela usa o modelo `Atividade` para identificar a atividade a ser excluída. A view redireciona para a página de listagem de atividades após a exclusão bem-sucedida de uma atividade. A view requer que o usuário esteja logado.
```

class AtividadeDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Atividade
    template_name = 'core/registros/form_excluir.html'
    success_url = reverse_lazy('listar-atividade')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        self.object = get_object_or_404(
            Atividade, pk=pk, usuario=self.request.user)
        return self.object

```
## Listagem de Atividades

A classe `AtividadeList` é uma view baseada em classe para a listagem de atividades. Ela usa o modelo `Atividade` para obter a lista de atividades a serem exibidas. A view requer que o usuário esteja logado.
```

class AtividadeList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Atividade
    template_name = 'core/listas/atividade_list.html'
    paginate_by = 30
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'title': 'Inicio', 'url': '/home/'},
            {'title': 'Atividades', 'url': '/listar-atividade/'},
        ]

        return context

    def get_queryset(self):
        search_term = self.request.GET.get('search')
        queryset = Atividade.objects.filter(usuario=self.request.user)

        if search_term:
            queryset = queryset.filter(tema__icontains=search_term)

        queryset = queryset.order_by('-data_registro')
        return queryset

```
## Listagem Geral de Atividades

A classe `AtividadeGeralList` é uma view baseada em classe para a listagem geral de atividades. Ela requer que o usuário esteja logado.
```

class AtividadeGeralList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador", u"Tecnico"]
    model = Atividade
    template_name = 'core/listas/atividadesGerais.html'
    paginate_by = 5
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['url'] = reverse('listar-atividade-geral')
        context['locais'] = Local.objects.all()
        context['usuario'] = CustomUsuario.objects.all()
        return context

    def get_queryset(self):
        # Parâmetros da URL
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        last_days = self.request.GET.get('last_days')
        local = self.request.GET.get('local')
        search_term = self.request.GET.get('search')
        
        # Começa com todas as atividades
        queryset = Atividade.objects.all()

        if start_date and end_date:
            # Converte em data e adiciona um dia ao fim
            end_date = parse(end_date) + timedelta(1)
            # Filtra atividades com base nas datas de início e encerramento
            queryset = Atividade.objects.filter(
                data_inicio__gte=start_date, data_encerramento__lte=end_date)
        elif start_date:
            # Filtra atividades com base apenas na data de início
            queryset = Atividade.objects.filter(data_inicio=start_date)
        elif end_date:
            # Filtra atividades com base apenas na data de encerramento
            queryset = Atividade.objects.filter(data_encerramento=end_date)
        elif last_days:
            try:
                last_days = int(last_days)
                # Data atual
                today = datetime.now().date()
                # Data de início do período (30, 60 ou 90 dias atrás)
                start_date = today - timedelta(days=last_days)
                # Filtra atividades com base na data de início
                queryset = Atividade.objects.filter(
                    data_inicio__gte=start_date)
            except ValueError:
                # Lida com valor inválido para last_days
                queryset = Atividade.objects.all()

        if 'month' in self.request.GET:
            try:
                # Obter o mês da URL
                selected_month = int(self.request.GET.get('month'))
                # Obter o ano atual
                current_year = timezone.now().year
                # Criar uma data com o ano atual e o mês selecionado
                start_date = timezone.datetime(current_year, selected_month, 1).date()
                
                # Calcular o primeiro dia do mês seguinte
                next_month = selected_month % 12 + 1
                next_year = current_year + selected_month // 12
                end_date = timezone.datetime(next_year, next_month, 1).date()

                # Filtrar atividades com base no intervalo de datas
                queryset = queryset.filter(
                    data_inicio__gte=start_date,
                    data_inicio__lt=end_date,
                )
            except (ValueError, TypeError):
                pass


        if local:
            # Filtrar atividades por local, usando o parâmetro 'local' da URL
            queryset = queryset.filter(local=local)

        if search_term:
            queryset = queryset.filter(Q(tema__icontains=search_term) | Q(
                usuario__username__icontains=search_term))

        queryset = queryset.order_by('-data_registro')
        return queryset

```