# Importações de módulos padrão
from django.contrib.auth.models import User
from .models import Atividade, Arquivo
from django.views.generic import TemplateView
from reportlab.platypus import FrameBreak
from reportlab.platypus import Image
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle, PageTemplate, Frame
from reportlab.lib.pagesizes import letter, landscape
from django.utils.timezone import now
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView)
from django.contrib.auth.forms import PasswordChangeForm
from weasyprint import HTML, CSS
from django.views.generic import FormView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.shortcuts import render
from .models import Arquivo, Atividade
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.utils import timezone
import tempfile
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Spacer
from reportlab.platypus import KeepInFrame

# Importações do Django
from django.http import HttpResponse, request
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import Group
from django.template.loader import render_to_string
from django.core.files import File
from django.views.decorators.csrf import csrf_exempt
# Importações de módulos do Django específicos
from django.views.generic.edit import View, CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.forms.models import BaseModelForm
from .forms import ArquivoForm, ArquivoFormSet, AtividadeForm
from django.templatetags.static import static
from django.conf import settings
from django.forms import inlineformset_factory
from django.db.models import Q
import os


# Importações de módulos de terceiros
import weasyprint
from braces.views import GroupRequiredMixin

# Importações locais
from .models import Local, Atividade
from .forms import UsuarioForm
from django.contrib.auth.mixins import LoginRequiredMixin
from dateutil.parser import parse
from datetime import timedelta, datetime
from django.contrib import messages


# views para registro de usuarios
class UsuarioCreate(CreateView):
    template_name = 'core/usuarios/form.html'
    form_class = UsuarioForm
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
        context['titulo'] = "Registro de Usuario"
        context['botao'] = "Registrar"
        return context


# views para reset senha
class MyPasswordReset(PasswordResetView):
    '''
    Requer
    registration/password_reset_form.html
    registration/password_reset_email.html
    registration/password_reset_subject.txt  Opcional
    '''
    template_name = 'core/usuarios/password_reset_form.html'
    ...


class MyPasswordResetDone(PasswordResetDoneView):
    '''
    Requer
    registration/password_reset_done.html
    '''

    template_name = 'core/usuarios/password_reset_done.html'
    ...


class MyPasswordResetConfirm(PasswordResetConfirmView):
    '''
    Requer password_reset_confirm.html
    '''
    template_name = 'core/usuarios/password_reset_confirm.html'

    def form_valid(self, form):
        self.user.is_active = True
        self.user.save()
        messages.success(self.request, 'Sua senha foi atualizada com sucesso!')
        return super(MyPasswordResetConfirm, self).form_valid(form)


class MyPasswordResetComplete(PasswordResetCompleteView):
    '''
    Requer password_reset_complete.html
    '''
    template_name = 'core/usuarios/password_reset_complete.html'
    ...

# view para alterar senha


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


class Home(TemplateView):
    template_name = 'core/home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'title': 'Inicio', 'url': '/home/'},
        ]
        return context


class HomeTecnico(TemplateView):
    template_name = 'inicioTecnico.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
            {'title': 'Atividades', 'url': '/listar-atividade/'},
            {'title': 'Registro de atividade', 'url': '/cadastro-atividade/'},
        ]

        # Criando o formset de Arquivos relacionados à Atividade
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

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        url = super().form_valid(form)
        messages.success(self.request, self.success_message)

        # Adicione aqui a lógica para salvar os arquivos associados à atividade

        formset = ArquivoFormSet(
            self.request.POST, self.request.FILES, instance=self.object)

        if formset.is_valid():
            formset.save()

        return url
# class AtividadeCreate(LoginRequiredMixin, CreateView):
#     login_url = reverse_lazy('login')
#     model = Atividade
#     fields = ['tema', 'descricao', 'local', 'quantidade_ptc', 'data_inicio', 'data_encerramento', 'duracao']
#     template_name = 'core/registros/form-upload.html'
#     success_url = reverse_lazy('listar-atividade')
#     success_message = 'Atividade registrada com Sucesso!'

#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context['titulo'] = "Registro de Atividade"
#         context['botao'] = "Registrar"
#         context['url'] = reverse('listar-atividade')

#         # Criando o formset de Arquivos relacionados à Atividade
#         ArquivoFormSet = inlineformset_factory(Atividade, Arquivo, fields=['arquivo',], extra=1)

#         if self.request.POST:
#             # Se dados forem submetidos, popula os formulários com os dados enviados
#             context['formset'] = ArquivoFormSet(self.request.POST, self.request.FILES)
#         else:
#             # Se não, cria um formset vazio
#             context['formset'] = ArquivoFormSet()

#         return context

#     def form_valid(self, form):
#         form.instance.usuario = self.request.user
#         url = super().form_valid(form)

#         # Adicione aqui a lógica para salvar os arquivos associados à atividade
#         formset = ArquivoFormSet(self.request.POST, self.request.FILES, instance=self.object)

#         if formset.is_valid():
#             for form in formset:
#                 if form.cleaned_data.get('arquivo'):
#                     arquivo = form.save(commit=False)  # Obtém o objeto Arquivo sem salvá-lo ainda
#                     arquivo.atividade = self.object  # Define a atividade para cada arquivo
#                     arquivo.save()  # Salva o objeto Arquivo
#         else:
#             return super().form_invalid(form)

#         messages.success(self.request, self.success_message)
#         return super().form_valid(form)


# @login_required
# def AtividadeCreate(request):
#     success_message = 'Atividade registrada com Sucesso!'
#     if request.method == 'POST':
#         form = AtividadeForm(request.POST, request.FILES)
#         formset = ArquivoFormSet(request.POST, request.FILES, instance=form.instance)
#         if form.is_valid() and formset.is_valid():
#             form.save()
#             formset.save()
#             messages.success(request, success_message)
#             return redirect('listar-atividade')
#     else:
#         form = AtividadeForm()
#         formset = ArquivoFormSet()

#     return render(request, 'core/registros/form-upload.html', {'form': form, 'formset': formset})


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
    template_name = 'templates/core/listas/Atividade.html'
    paginate_by = 6

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


class AtividadeGeralList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador", u"Tecnico"]
    model = Atividade
    template_name = 'core/listas/atividadesGerais.html'
    paginate_by = 30

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['url'] = reverse('listar-atividade-geral')
        context['locais'] = Local.objects.all()
        context['usuario'] = User.objects.all()
        return context

    def get_queryset(self):
        # Parâmetros da URL
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        last_days = self.request.GET.get('last_days')
        local = self.request.GET.get('local')
        search_term = self.request.GET.get('search')

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

        elif 'mes' in self.request.GET:
            try:
                # Obter o mês da URL
                selected_month = int(self.request.GET.get('mes'))
                # Obter o ano atual
                current_year = timezone.now().year
                # Criar uma data com o ano atual e o mês selecionado
                start_date = timezone.datetime(
                    current_year, selected_month, 1).date()
                end_date = start_date + timezone.timedelta(days=32)
                # Filtrar atividades com base no mês selecionado
                queryset = Atividade.objects.filter(
                    data_inicio__gte=start_date,
                    data_inicio__lt=end_date,
                )
            except (ValueError, TypeError):
                # Lida com valores inválidos para o mês
                queryset = Atividade.objects.all()

        elif local:
            # Filtrar atividades por local, usando o parâmetro 'local' da URL
            queryset = Atividade.objects.filter(local_id=local)

        else:
            queryset = Atividade.objects.all()

        if search_term:
            queryset = queryset.filter(Q(tema__icontains=search_term) | Q(
                usuario__username__icontains=search_term))

        return queryset


class CustomLoginRedirectView(View):
    def get(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Tecnico').exists():

            return redirect('listar-atividade-geral')
        elif request.user.groups.filter(name='Docente').exists():

            return redirect('home')
        else:
            return redirect('home')


#################### GERAR RELATÓRIO EM PDF#####################################
# def export_pdf(request):
#     c=canvas.Canvas('teste.pdf')
#     c.drawString(200,200, 'olá mundo')
#     c.showPage()
#     c.save()

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'inline; filename="nome_do_arquivo.pdf"'

#     # Escreva o PDF no objeto de resposta
#     pdf = c.getpdfdata()
#     response.write(pdf)

#     return response
def export_pdf(request):
    # Obtendo todas as atividades do modelo Atividade
    atividades = Atividade.objects.all()

    # Criando um objeto BytesIO para armazenar o PDF
    buffer = BytesIO()

    # Criando o documento PDF usando o ReportLab
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    # Criando uma lista para adicionar elementos ao PDF
    elements = []

    # Obtendo o estilo de parágrafo para o cabeçalho
    styles = getSampleStyleSheet()
    style_title = ParagraphStyle(
        name='TitleStyle',
        parent=styles['Title'],
        fontSize=16,
    )
    style_paragraph = ParagraphStyle(
        name='CenteredParagraph', alignment=1,
        parent=styles['Normal'],
        fontSize=12,
    )

   # Adiciona o cabeçalho com a imagem e o título
    # header_frame = Frame(inch, doc.height + inch, doc.width, inch)
    image_path = os.path.join(
        settings.BASE_DIR, 'static', 'img', 'Logo-ufac-cor.png')
    logo = Image(image_path, width=40, height=56)

    # Título
    titulo = Paragraph(
        '<b>REGISTRO DE ATIVIDADES REALIZADAS<br/>NO LABORATÓRIO DE INFORMÁTICA DO LIFE</b>',
        style_title
    )

    # Tabela do cabeçalho
    header_data = [[logo, titulo]]
    # Tabela do cabeçalho
    header_table = Table(header_data, colWidths=[50, 415])
    # Estilo da tabela
    table_style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinhamento centralizado
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinhamento vertical ao meio
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grade
        ('FONTSIZE', (0, 0), (-1, -1), 12),  # Tamanho da fonte
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),  # Nome da fonte
    ])

    header_table.setStyle(table_style)

    # Adicione a tabela de cabeçalho à lista de elementos
    c = canvas.Canvas("relatório.pdf")
    elements.append(header_table)
    elements.append(Spacer(1, 20))

    # Criando listas para armazenar os dados das colunas
    temas = ['Tema']
    responsaveis = ['Nome do Responsável']
    participantes = ['Nº de Participantes']
    datas_inicio = ['Início']
    datas_encerramento = ['Encerramento']

    # Preenchendo as listas com os dados das atividades
    for atividade in atividades:
        nome_completo = f"{atividade.usuario.first_name} {atividade.usuario.last_name}"

        temas.append(atividade.tema)
        responsaveis.append(nome_completo)
        participantes.append(str(atividade.quantidade_ptc))
        datas_inicio.append(atividade.data_inicio.strftime('%d/%m/%Y'))
        datas_encerramento.append(
            atividade.data_encerramento.strftime('%d/%m/%Y'))

    # Organizando os dados em colunas
    colunas = [temas, responsaveis, participantes,
               datas_inicio, datas_encerramento]
    tabela_dados = list(map(list, zip(*colunas)))
    # Criando a tabela com os dados organizados como colunas
    table = Table(tabela_dados)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Cor de fundo do cabeçalho
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Cor do texto do cabeçalho
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        # Outros estilos da tabela...
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    def footer(canvas, doc):
        canvas.saveState()
        footer = Paragraph(
            f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
            getSampleStyleSheet()['Normal']
        )
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)
        canvas.restoreState()

    frame = Frame(doc.leftMargin, doc.bottomMargin,
                  doc.width, doc.height, id='normal')
    template = PageTemplate(id='test', frames=frame, onPage=footer)
    doc.addPageTemplates([template])

    # Adicione o parágrafo alinhado ao centro

    # Construa o PDF
    doc.build(elements, c)

    # Retornando o PDF como uma resposta HTTP para abrir em uma nova guia
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=Relatorio.pdf'
    response.write(buffer.getvalue())
    buffer.close()

    return response
# def export_pdf(request):

#     # Obtenha todas as atividades
#     relatorios = Atividade.objects.all()

#     # Cria um objeto BytesIO para armazenar o PDF
#     buffer = BytesIO()

#     # Cria o documento PDF usando o ReportLab
#     doc = SimpleDocTemplate(buffer, pagesize=A4)

#     # Cria uma lista para adicionar elementos ao PDF
#     elements = []
#     styles = getSampleStyleSheet()
#     style_title = ParagraphStyle(
#         name='TitleStyle',
#         parent=styles['Title'],
#         fontSize=16,
#     )
#     style_paragraph = ParagraphStyle(
#         name='CenteredParagraph', alignment=1,
#         parent=styles['Normal'],
#         fontSize=12,
#     )

#    # Adiciona o cabeçalho com a imagem e o título
#     # header_frame = Frame(inch, doc.height + inch, doc.width, inch)
#     image_path = os.path.join(
#         settings.BASE_DIR, 'static', 'img', 'Logo-ufac-cor.png')
#     logo = Image(image_path, width=40, height=56)

#     # Título
#     titulo = Paragraph(
#         '<b>REGISTRO DE ATIVIDADES REALIZADAS<br/>NO LABORATÓRIO DE INFORMÁTICA DO LIFE</b>',
#         style_title
#     )

#     # Tabela do cabeçalho
#     header_data = [[logo, titulo]]
#     # Tabela do cabeçalho
#     header_table = Table(header_data, colWidths=[50, 400])
#     # Estilo da tabela
#     table_style = TableStyle([
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinhamento centralizado
#         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinhamento vertical ao meio
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grade
#         ('FONTSIZE', (0, 0), (-1, -1), 12),  # Tamanho da fonte
#         ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),  # Nome da fonte
#     ])

#     header_table.setStyle(table_style)

#     # Adicione a tabela de cabeçalho à lista de elementos
#     c = canvas.Canvas("relatório.pdf")
#     elements.append(header_table)
#     elements.append(Spacer(1, 20))

#     # Para cada relatório, crie uma tabela de dados
#     for relatorio in relatorios:
#         data_inicio_formatada = relatorio.data_inicio.strftime('%d/%m/%Y')
#         data_encerramento_formatada = relatorio.data_encerramento.strftime(
#             '%d/%m/%Y')
#         data = [
#             ['Tema:', Paragraph(relatorio.tema, style_paragraph)],
#             ['Descrição:', Paragraph(
#                 relatorio.descricao, getSampleStyleSheet()['Normal'])],
#             ['Nome do Responsável:', Paragraph(
#                 relatorio.usuario.username, getSampleStyleSheet()['Normal'])],
#             ['Quantidade de Participantes:', Paragraph(
#                 str(relatorio.quantidade_ptc), getSampleStyleSheet()['Normal'])],
#             ['Data de Início:', Paragraph(
#                 str(data_inicio_formatada), getSampleStyleSheet()['Normal'])],
#             ['Data de Encerramento:', Paragraph(
#                 str(data_encerramento_formatada), getSampleStyleSheet()['Normal'])],
#         ]

#         table = Table(data, colWidths=[150, 300])
#         table.setStyle(TableStyle([
#             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
#             ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#             ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#             ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#             ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#             ('LEFTPADDING', (0, 0), (-1, -1), 5),
#             ('RIGHTPADDING', (0, 0), (-1, -1), 8),
#             ('TOPPADDING', (0, 0), (-1, -1), 8),
#             ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
#         ]))

#         # Adicione a tabela à lista de elementos
#         # table_in_frame = KeepInFrame(0, 0, [table], mode="shrink")
#         elements.append(table)
#         # Adicione um espaço em branco após a tabela
#         elements.append(Spacer(1, 10))

#         # # Adicione um FrameBreak para passar para a próxima página
#         # elements.append(FrameBreak())

#     # Adicione um parágrafo para a assinatura do responsável
#     line = Table(
#         [[Paragraph('<u>' + ' ' * 100 + '</u>', style_paragraph)]], colWidths=[500])
#     elements.append(line)

#     def footer(canvas, doc):
#         canvas.saveState()
#         footer = Paragraph(
#             f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
#             getSampleStyleSheet()['Normal']
#         )
#         w, h = footer.wrap(doc.width, doc.bottomMargin)
#         footer.drawOn(canvas, doc.leftMargin, h)
#         canvas.restoreState()

#     frame = Frame(doc.leftMargin, doc.bottomMargin,
#                   doc.width, doc.height, id='normal')
#     template = PageTemplate(id='test', frames=frame, onPage=footer)
#     doc.addPageTemplates([template])

#     # Adicione o parágrafo alinhado ao centro
#     assinatura = Paragraph('<b>Assinatura do Responsável</b>', style_paragraph)
#     elements.append(assinatura)

#     # Construa o PDF
#     doc.build(elements, c)

#     # Retorne o PDF como uma resposta HTTP para abrir em uma nova guia
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'inline; filename=Relatório' + \
#         '-' + datetime.now().strftime("%d-%m-%y") + '.pdf'
#     response.write(buffer.getvalue())
#     buffer.close()

#     return response


def exibir_relatorio(request, pk):
    relatorio = get_object_or_404(Atividade, id=pk)
    arquivos = relatorio.arquivo.all()  # Use o nome correto do relacionamento
    context = {
        'relatorio': relatorio,
        'arquivos': arquivos,
        'breadcrumb': [
            {'title': 'Inicio', 'url': '/home/'},
            {'title': 'Atividades', 'url': '/listar/atividades/'},
            {'title': 'Detalhes', 'url': '/detalhes/'},
        ]
    }
    return render(request, 'core/listas/exibir_relatorio.html', context)


def gerar_pdf_relatorio(request, pk):

    relatorio = get_object_or_404(Atividade, id=pk)

    # Cria um objeto BytesIO para armazenar o PDF
    buffer = BytesIO()

    # Cria o documento PDF usando o ReportLab
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Cria uma lista para adicionar elementos ao PDF
    elements = []
    styles = getSampleStyleSheet()
    style_title = ParagraphStyle(
        name='TitleStyle',
        parent=styles['Title'],
        fontSize=16,
    )
    style_paragraph = ParagraphStyle(
        name='CenteredParagraph', alignment=1,
        parent=styles['Normal'],
        fontSize=12,
    )

    # Adiciona o cabeçalho com a imagem e o título
    image_path = os.path.join(
        settings.BASE_DIR, 'static', 'img', 'Logo-ufac-cor.png')
    logo = Image(image_path, width=40, height=56),
    titulo = Paragraph(
        '<b>REGISTRO DE ATIVIDADES REALIZADAS<br/>NO LABORATÓRIO DE INFORMÁTICA DO LIFE</b>', style_title)

    header_table = Table([[logo, titulo]], colWidths=[150, 400], rowHeights=70)
    header_table.setStyle(TableStyle([

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
    ]))

    # Adicione a tabela de cabeçalho à lista de elementos
    elements.append(header_table)
    # Crie uma tabela para os campos de dados
    data_inicio_formatada = relatorio.data_inicio.strftime('%d/%m/%Y')
    data_encerramento_formatada = relatorio.data_encerramento.strftime(
        '%d/%m/%Y')
    data = [
        ['Tema:', Paragraph(relatorio.tema, style_paragraph)],
        ['Descrição:', Paragraph(
            relatorio.descricao, getSampleStyleSheet()['Normal'])],
        ['Nome do Responsável:', Paragraph(
            relatorio.usuario.username, getSampleStyleSheet()['Normal'])],
        ['Quantidade de Participantes:', Paragraph(
            str(relatorio.quantidade_ptc), getSampleStyleSheet()['Normal'])],
        ['Data de Início:', Paragraph(
            str(data_inicio_formatada), getSampleStyleSheet()['Normal'])],
        ['Data de Encerramento:', Paragraph(
            str(data_encerramento_formatada), getSampleStyleSheet()['Normal'])],
    ]

    table = Table(data, colWidths=[150, 400])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))

    # Adicione a tabela à lista de elementos

    table_in_frame = KeepInFrame(0, 0, [table], mode="shrink")
    elements.append(table_in_frame)
    # Adicione um espaço em branco após a tabela
    elements.append(Spacer(1, 20))

    def footer(canvas, doc):
        canvas.saveState()
        footer = Paragraph(
            f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
            getSampleStyleSheet()['Normal']
        )
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)
        canvas.restoreState()

    frame = Frame(doc.leftMargin, doc.bottomMargin,
                  doc.width, doc.height, id='normal')
    template = PageTemplate(id='test', frames=frame, onPage=footer)
    doc.addPageTemplates([template])

    # Adicione um parágrafo para a assinatura do responsável
    line = Table(
        [[Paragraph('<u>' + '&nbsp;' * 100 + '</u>', style_paragraph)]], colWidths=[500])
    elements.append(line)

# Adicione o parágrafo alinhado ao centro
    assinatura = Paragraph('<b>Assinatura do Responsável</b>', style_paragraph)
    elements.append(assinatura)

    # Construa o PDF
    doc.build(elements)

    # Retorne o PDF como uma resposta HTTP para abrir em uma nova guia
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=Relatório' + \
        '-' + datetime.now().strftime("%d-%m-%y") + '.pdf'
    response.write(buffer.getvalue())
    buffer.close()

    return response
