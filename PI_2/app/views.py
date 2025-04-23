from django.shortcuts import render
from django.http import HttpResponse
from .models import Categoria, Marca, Produto

# View de teste sem nenhuma dependência
def test_view(request):
    return HttpResponse("Página de teste funcionando!")

def homepage(request):
    return render(request, 'homepage/HomePage.html')

def contatos(request):
    return render(request, 'contatos/Contato.html')

def form(request):
    return render(request, 'formulario/Forms.html')

def catalogo(request):
    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()
    produtos = Produto.objects.all()
    
    context = {
        'categorias': categorias,
        'marcas': marcas,
        'produtos': produtos
    }
    
    return render(request, 'catalog/catalog.html', context)