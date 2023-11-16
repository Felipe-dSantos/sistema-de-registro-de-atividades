# Importações de módulos padrão
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
from .models import Atividade
from datetime import datetime
from django.http import HttpResponse
import datetime
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
from .forms import AtividadeForm
from django.templatetags.static import static
from django.conf import settings
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
    fields = ['tema', 'descricao', 'local',
              'quantidade_ptc', 'data_inicio', 'data_encerramento', 'arquivos']
    template_name = 'core/registros/form-upload.html'
    success_url = reverse_lazy('listar-atividade')
    success_message = 'Atividade registrada com Sucesso!'

    def form_valid(self, form):

        # captura o usuario que esta fazendo o cadastro
        form.instance.usuario = self.request.user
        url = super().form_valid(form)
        messages.success(self.request, self.success_message)

        return url

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Registro de Atividade"
        context['botao'] = "Registrar"
        context['url'] = reverse('listar-atividade')
        context['breadcrumb'] = [
            {'title': 'Inicio', 'url': '/home/'},
            {'title': 'atividades', 'url': '/listar/atividades/'},
            {'title': 'registro de atividade', 'url': '/cadastro-atividade/'},
        ]

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
    paginate_by = 6

    def get_queryset(self):
        self.object_list = Atividade.objects.filter(usuario=self.request.user)
        return self.object_list
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'title': 'Inicio', 'url': '/home/'},
            {'title': 'atividades', 'url': '/listar-atividade/'},
            
        ]
        return context


class AtividadeGeralList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = [u"Administrador", u"Tecnico"]
    model = Atividade
    template_name = 'core/listas/atividadesGerais.html'
    paginate_by = 6

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['url'] = reverse('listar-atividade-geral')
        return context

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
                queryset = Atividade.objects.filter(
                    data_inicio__gte=start_date)
            except ValueError:
                # Lida com valor inválido para last_days
                queryset = Atividade.objects.all()
        else:
            queryset = Atividade.objects.all()

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

    # Obtenha todas as atividades
    relatorios = Atividade.objects.all()

    # Cria um objeto BytesIO para armazenar o PDF
    buffer = BytesIO()

    # Cria o documento PDF usando o ReportLab
    doc = SimpleDocTemplate(buffer, pagesize=A4)

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
    header_table = Table(header_data, colWidths=[50, 400])
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

    # Para cada relatório, crie uma tabela de dados
    for relatorio in relatorios:
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

        table = Table(data, colWidths=[150, 300])
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
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))

        # Adicione a tabela à lista de elementos
        # table_in_frame = KeepInFrame(0, 0, [table], mode="shrink")
        elements.append(table)
        # Adicione um espaço em branco após a tabela
        elements.append(Spacer(1, 10))

        # # Adicione um FrameBreak para passar para a próxima página
        # elements.append(FrameBreak())

    # Adicione um parágrafo para a assinatura do responsável
    line = Table(
        [[Paragraph('<u>' + ' ' * 100 + '</u>', style_paragraph)]], colWidths=[500])
    elements.append(line)

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
    assinatura = Paragraph('<b>Assinatura do Responsável</b>', style_paragraph)
    elements.append(assinatura)

    # Construa o PDF
    doc.build(elements, c)

    # Retorne o PDF como uma resposta HTTP para abrir em uma nova guia
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=Relatório' + \
        '-' + datetime.now().strftime("%d-%m-%y") + '.pdf'
    response.write(buffer.getvalue())
    buffer.close()

    return response


def exibir_relatorio(request, pk):
    relatorio = get_object_or_404(Atividade, id=pk)
    context = {
        'relatorio': relatorio,
        'breadcrumb': [
            {'title': 'Inicio', 'url': '/home/'},
            {'title': 'atividades', 'url': '/listar/atividades/'},
            {'title': 'detalhes', 'url': '/detalhes/'},
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



# def login_view(request):
#     if request.method == 'POST':
#         cpf = request.POST['cpf']
#         password = request.POST['password']
#         print(cpf)
#         print(password)
#         user = authenticate(request, cpf=cpf, password=password)
#         print(user)
#         if user is not None:
#             login(request, user)
#             print('entrou aqui')
#             # Autenticação bem-sucedida, redirecione para a página de sucesso ou faça o que for necessário
#             messages.success(request, 'Bem Vindo (a) '+ user.first_name)
#             return redirect('home')
#         else:
#             # Autenticação falhou, lide com isso de acordo
#             messages.debug(request, 'Ops! Aconteceu algum erro.') 
#     # Renderize o formulário de login
#     return render(request, 'core/usuarios/login.html')