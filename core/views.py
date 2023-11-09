# Importações de módulos padrão
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


# Create views.

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
        elif request.user.groups.filter(name='Dicente').exists():

            return redirect('listar-atividade')
        else:
            return redirect('listar-atividade')

#################### GERAR RELATÓRIO EM PDF#####################################


@login_required
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

    # Defina um estilo CSS para a tabela
    table_style = """
    table {
        border-collapse: collapse;
    }
    th {
        border: 1px solid #000;  /* Adicione bordas às células da tabela */
        padding: 5px;
        background-color: lightgray;  /* Defina a cor de fundo das células */
    }
    img{
        width: 60px
    }
    """

    weasyprint_html = HTML(
        string=html_index, base_url='http://localhost:8000/media')
    pdf = weasyprint_html.write_pdf(stylesheets=[CSS(string=table_style)])

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=Relatório-de-Atividades-LIFE' + \
        datetime.now().strftime("%Y-%m-%d %H-%M-%S") + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(pdf)
        output.flush()
        output.seek(0)
        response.write(output.read())
    return response


def exibir_relatorio(request, pk):
    relatorio = get_object_or_404(Atividade, id=pk)
    return render(request, 'core/listas/exibir_relatorio.html', {'relatorio': relatorio})


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
        context['botao'] = "Alterar"
        context['url'] = reverse('listar-atividade')
        return context


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


class MyPasswordResetComplete(PasswordResetCompleteView):
    '''
    Requer password_reset_complete.html
    '''
    template_name = 'core/usuarios/password_reset_complete.html'
    ...
