"""
WSGI app para implantação no Azure App Service.
Esse arquivo serve como ponto de entrada para o Gunicorn no ambiente Azure.
"""

import os
import sys

# Adiciona o caminho do projeto ao PYTHONPATH
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)

# Adiciona o diretório do projeto Django ao PYTHONPATH
project_path = os.path.join(path, 'PI_2')
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# Configura o módulo de configurações do Django para produção
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PI_2.settings_production')

# Importa o objeto application do Django WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()