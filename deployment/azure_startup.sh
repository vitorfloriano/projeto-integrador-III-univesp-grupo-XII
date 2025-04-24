#!/bin/bash
# Consolidated Azure deployment startup script

# Diretório base da aplicação
APP_DIR="$HOME/site/wwwroot"
echo "Diretório da aplicação: $APP_DIR"

# Explicitamente definindo ambiente de produção para Azure
export DJANGO_ENV="prod"
echo "DJANGO_ENV configurado para: $DJANGO_ENV"

# Ativação do ambiente virtual
if [ -d "$HOME/antenv" ]; then
    echo "Ativando ambiente virtual existente..."
    source $HOME/antenv/bin/activate
else
    echo "Criando novo ambiente virtual..."
    python -m venv "$HOME/antenv"
    source $HOME/antenv/bin/activate
fi

# Verificação das versões
echo "Versão do Python: $(python --version)"
echo "Versão do pip: $(pip --version)"

# Instalação das dependências
echo "Instalando dependências..."
pip install -r "$APP_DIR/requirements.txt"

# Configuração do PYTHONPATH
export PYTHONPATH="$APP_DIR:$PYTHONPATH"
echo "PYTHONPATH configurado: $PYTHONPATH"

# Aplicação das migrações
echo "Aplicando migrações do banco de dados..."
cd "$APP_DIR"
python manage.py migrate --noinput

# Coleta de arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear

# Iniciando o Gunicorn
echo "Iniciando o Gunicorn..."
GUNICORN_PATH=$(which gunicorn)
$GUNICORN_PATH core.wsgi:application --bind=0.0.0.0:8000 --log-level info --timeout 120