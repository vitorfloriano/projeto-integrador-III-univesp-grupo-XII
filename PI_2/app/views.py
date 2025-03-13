from django.shortcuts import render

def homepage(request):
    return render(request, 'homepage/HomePage.html')
def contatos(request):
    return render(request, 'contatos/Contato.html')
def form(request):
    return render(request, 'formulario/Forms.html')