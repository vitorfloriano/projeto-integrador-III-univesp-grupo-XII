"""
Arquivo de ponto de entrada alternativo para o Azure App Service.
Este arquivo é um fallback caso o wsgi_app.py falhe.
"""

import os
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Adicionar o diretório atual ao sys.path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Adicionar o diretório PI_2 ao sys.path
    project_dir = os.path.join(current_dir, 'PI_2')
    if project_dir not in sys.path:
        sys.path.insert(0, project_dir)
    
    # Verificação de diretórios
    logger.info(f"Diretório atual: {current_dir}")
    logger.info(f"Diretório do projeto: {project_dir}")
    logger.info(f"Conteúdo do diretório atual: {os.listdir(current_dir)}")
    
    if os.path.exists(project_dir):
        logger.info(f"Conteúdo do diretório PI_2: {os.listdir(project_dir)}")
    else:
        logger.error(f"ERRO: Diretório {project_dir} não existe!")
    
    # Configurar variáveis de ambiente para o Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PI_2.settings')
    
    # Importar e obter a aplicação WSGI
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    
    logger.info("Aplicação WSGI carregada com sucesso!")
    
except Exception as e:
    logger.error(f"Erro ao inicializar a aplicação: {e}")
    logger.error(f"sys.path: {sys.path}")
    
    # Fornecer um objeto application para evitar erro no Gunicorn
    def application(environ, start_response):
        status = '500 Internal Server Error'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        error_msg = f"Erro ao inicializar a aplicação Django: {e}"
        return [error_msg.encode()]