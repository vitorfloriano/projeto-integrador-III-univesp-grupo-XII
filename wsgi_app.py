"""
WSGI app para implantação no Azure App Service.
Esse arquivo serve como ponto de entrada para o Gunicorn no ambiente Azure.
"""

import os
import sys
import site

# Adiciona o diretório atual ao sys.path
current_path = os.path.abspath(os.path.dirname(__file__))
if current_path not in sys.path:
    sys.path.insert(0, current_path)

# Adiciona o diretório do projeto Django ao PYTHONPATH
project_path = os.path.join(current_path, 'PI_2')
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# Debug - Imprimir informações sobre o ambiente
print("Caminhos Python:")
for p in sys.path:
    print(f"  - {p}")

print("Conteúdo do diretório atual:")
print(os.listdir(current_path))

if os.path.exists(project_path):
    print("Conteúdo do diretório PI_2:")
    print(os.listdir(project_path))
else:
    print(f"ERRO: Diretório {project_path} não existe!")

# Configura o módulo de configurações do Django para produção
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PI_2.settings')

# Importa o objeto application do Django WSGI
try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    print("Aplicação WSGI carregada com sucesso!")
except Exception as e:
    print(f"ERRO ao carregar a aplicação WSGI: {e}")
    print(f"sys.path = {sys.path}")
    raise