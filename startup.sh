#!/bin/bash

# Ativação do ambiente virtual (caso exista)
if [ -d "$HOME/antenv" ]; then
    source $HOME/antenv/bin/activate
fi

# Instalação das dependências
pip install -r requirements.txt

# Navegação para o diretório do projeto Django
cd PI_2

# Aplicação das migrações (opcional, remover em produção se necessário)
python manage.py migrate --noinput

# Coleta de arquivos estáticos
python manage.py collectstatic --noinput

# Inicialização do Gunicorn
gunicorn PI_2.wsgi:application --bind=0.0.0.0:8000
