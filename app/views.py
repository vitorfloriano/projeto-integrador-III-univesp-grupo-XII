from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
import logging

from .models import Categoria, Marca, Produto
from .forms import ContatoForm, EmpregoForm

# Configure logger
logger = logging.getLogger(__name__)

# View de teste sem nenhuma dependência
def test_view(request):
    return HttpResponse("Página de teste funcionando!")

# View para a homepage
def homepage(request):
    return render(request, 'homepage/pagina_inicial.html')

# View para a página de contatos
def contatos(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            # Get form data
            nome = form.cleaned_data['nome']
            email = form.cleaned_data['email']
            mensagem = form.cleaned_data['mensagem']
            
            # Process the form data (e.g., save to database, send email)
            try:
                # Example: Sending email notification
                subject = f'Nova mensagem de contato de {nome}'
                message = f'Nome: {nome}\nEmail: {email}\nMensagem: {mensagem}'
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [settings.CONTACT_EMAIL]
                
                # Uncomment when email settings are configured
                # send_mail(subject, message, from_email, recipient_list)
                
                # Add success message
                messages.success(request, 'Sua mensagem foi enviada com sucesso! Entraremos em contato em breve.')
                return redirect('contato')
            except Exception as e:
                logger.error(f"Erro ao processar formulário de contato: {e}")
                messages.error(request, 'Ocorreu um erro ao enviar sua mensagem. Por favor, tente novamente mais tarde.')
        else:
            # Form is invalid
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = ContatoForm()
        
    return render(request, 'contatos/contato.html', {'form': form})

# View para o formulário
def form(request):
    if request.method == 'POST':
        form = EmpregoForm(request.POST)
        if form.is_valid():
            # Get form data
            nome = form.cleaned_data['nome_c']
            email = form.cleaned_data['email']
            
            # Process the form data (e.g., save to database, send email)
            try:
                # Example: Sending email notification
                subject = f'Nova candidatura de {nome}'
                message = f'Nome: {nome}\nEmail: {email}\nExperiência: {form.cleaned_data["experiencia"]}'
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [settings.HR_EMAIL]
                
                # Uncomment when email settings are configured
                # send_mail(subject, message, from_email, recipient_list)
                
                # Add success message
                messages.success(request, 'Sua candidatura foi enviada com sucesso! Entraremos em contato se houver interesse.')
                return redirect('formulario')
            except Exception as e:
                logger.error(f"Erro ao processar formulário de candidatura: {e}")
                messages.error(request, 'Ocorreu um erro ao enviar sua candidatura. Por favor, tente novamente mais tarde.')
        else:
            # Form is invalid
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = EmpregoForm()
        
    return render(request, 'formulario/formulario.html', {'form': form})

# View para o catálogo de produtos
def catalogo(request):
    # Obtendo todas as categorias e marcas para filtros
    categorias = Categoria.objects.all().order_by('nome_categoria')
    marcas = Marca.objects.all().order_by('nome_marca')
    
    # Inicializando queryset de produtos
    produtos = Produto.objects.all()
    
    # Aplicando filtros se fornecidos via GET
    categoria_id = request.GET.get('categoria')
    marca_id = request.GET.get('marca')
    search_term = request.GET.get('search')
    
    # Filtrar por categoria se especificado
    if categoria_id:
        try:
            produtos = produtos.filter(id_categoria=int(categoria_id))
        except (ValueError, TypeError):
            # Log invalid input but continue without this filter
            logger.warning(f"Valor inválido para filtro de categoria: {categoria_id}")
    
    # Filtrar por marca se especificado
    if marca_id:
        try:
            produtos = produtos.filter(id_marca=int(marca_id))
        except (ValueError, TypeError):
            # Log invalid input but continue without this filter
            logger.warning(f"Valor inválido para filtro de marca: {marca_id}")
    
    # Buscar por termo de busca (no nome ou descrição)
    if search_term:
        produtos = produtos.filter(
            Q(nome__icontains=search_term) | 
            Q(descricao__icontains=search_term)
        )
    
    # Criando um dicionário de contexto
    context = {
        'categorias': categorias,
        'marcas': marcas,
        'produtos': produtos,
        'selected_categoria': categoria_id,
        'selected_marca': marca_id,
        'search_term': search_term or '',
    }
    
    # Renderizando o template do catálogo com o contexto
    return render(request, 'catalog/catalogo.html', context)
