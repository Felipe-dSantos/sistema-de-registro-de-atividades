
# Importações de módulos padrão
import datetime
import tempfile


# Importações do Django
from django.http import HttpResponse, request
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import Group
from django.template.loader import render_to_string


# Importações de módulos do Django específicos
from django.views.generic.edit import View, CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.forms.models import BaseModelForm


# Importações de módulos de terceiros
import weasyprint
from braces.views import GroupRequiredMixin

# Importações locais
from .models import Local, Atividade
from .forms import UsuarioForm
from django.contrib.auth.mixins import LoginRequiredMixin
from dateutil.parser import parse
from datetime import timedelta, datetime


# Create views.

class UsuarioCreate(CreateView):
    template_name = 'core/usuarios/form.html'
    form_class = UsuarioForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):

        grupo = get_object_or_404(Group, name="Docente")
        url = super().form_valid(form)
        self.object.groups.add(grupo)
        self.object.save()

        return url

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Registro de Usuario"
        context['botao'] = "Registrar"
        return context

################### CRUD LOCAL #########################


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


class LocalDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = u"Administrador"
    model = Local
    template_name = 'core/registros/form_excluir.html'
    success_url = reverse_lazy('listar-local')


class LocalList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador", u"Docente"]
    model = Local
    template_name = 'core/listas/Local.html'

################### CRUD ATIVIDADE #########################


class AtividadeCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Atividade
    fields = ['tema', 'descricao', 'local',
              'quantidade_ptc', 'data_inicio', 'data_encerramento', 'arquivos']
    template_name = 'core/registros/form-upload.html'
    success_url = reverse_lazy('listar-atividade')

    def form_valid(self, form):

        # captura o usuario que esta fazendo o cadastro
        form.instance.usuario = self.request.user
        url = super().form_valid(form)

        return url

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Registro de Atividade"
        context['botao'] = "Registrar"
        context['url'] = reverse('listar-atividade')
        return context


class AtividadeUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Atividade
    fields = ['tema', 'descricao', 'local', 'quantidade_ptc',
              'data_inicio', 'data_encerramento', 'arquivos']
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


class AtividadeList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Atividade
    template_name = 'core/listas/Atividade.html'
    paginate_by = 10

    def get_queryset(self):
        self.object_list = Atividade.objects.filter(usuario=self.request.user)
        return self.object_list


class AtividadeGeralList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador", u"Tecnico"]
    model = Atividade
    template_name = 'core/listas/atividadesGerais.html'
    paginate_by = 15

    def get_queryset(self):
        # Parâmetros da URL
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        last_days = self.request.GET.get('last_days')

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
                queryset = Atividade.objects.filter(data_inicio__gte=start_date)
            except ValueError:
                # Lida com valor inválido para last_days
                queryset = Atividade.objects.all()
        else:
            queryset = Atividade.objects.all()

        return queryset

class CustomLoginRedirectView(View):
    def get(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Tecnico').exists():
            # Substitua pelo nome da URL da página inicial do técnico
            return redirect('listar-atividade-geral')
        elif request.user.groups.filter(name='Dicente').exists():
            # Substitua pelo nome da URL da página inicial do dicente
            return redirect('listar-atividade')
        else:
            return redirect('listar-atividade')

#################### GERAR RELATÓRIO EM PDF#####################################

def export_pdf(request):
    obj = request.GET.get('obj')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    last_days = request.GET.get('last_days')

    # Filtra as atividades com base nos parâmetros de filtro
   
    if obj:
        atividades = Atividade.objects.filter(tema__icontains=obj)
    elif start_date and end_date:
        end_date = parse(end_date) + timedelta(1)
        atividades = Atividade.objects.filter(
            data_inicio__gte=start_date, data_encerramento__lte=end_date)
    elif start_date:
        atividades = Atividade.objects.filter(data_inicio=start_date)
    elif end_date:
        atividades = Atividade.objects.filter(data_encerramento=end_date)
    elif last_days:
        try:
            last_days = int(last_days)
            today = datetime.now().date()
            start_date = today - timedelta(days=last_days)
            atividades = Atividade.objects.filter(data_inicio__gte=start_date)
        except ValueError:
            atividades = Atividade.objects.all()
    else:
        atividades = Atividade.objects.all()

    context = {'atividades': atividades}

    html_index = render_to_string('core/listas/relatorio.html', context)

    weasyprint_html = weasyprint.HTML(
        string=html_index, base_url='http://localhost:8000/media')
    pdf = weasyprint_html.write_pdf(stylesheets=[weasyprint.CSS(
        string='body { font-family: serif} img {margin: 10px; width: 50px;}')])

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=Relatório-de-Atividades-LIFE' + datetime.now().strftime("%Y-%m-%d %H-%M-%S") + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(pdf)
        output.flush()
        output.seek(0)
        response.write(output.read())
    return response
