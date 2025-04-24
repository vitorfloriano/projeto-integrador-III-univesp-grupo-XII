#!/bin/bash
# Consolidated Azure deployment startup script with improved error handling
set -e  # Exit immediately if a command exits with non-zero status

# Function for error logging
log_error() {
    echo "ERROR: $1" >&2
    exit 1
}

# Function for info logging
log_info() {
    echo "INFO: $1"
}

# Diretório base da aplicação
APP_DIR="$HOME/site/wwwroot"
log_info "Diretório da aplicação: $APP_DIR"

# Explicitamente definindo ambiente de produção para Azure
export DJANGO_ENV="prod"
log_info "DJANGO_ENV configurado para: $DJANGO_ENV"

# Ensure we're in the right directory
cd "$APP_DIR" || log_error "Failed to change to app directory: $APP_DIR"

# Check if Python exists and print version
if command -v python3 &> /dev/null; then
    log_info "Python 3 encontrado: $(python3 --version)"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    log_info "Python encontrado: $(python --version)"
    PYTHON_CMD="python"
else
    log_error "Python não encontrado. Verifique a configuração do ambiente."
fi

# Use built-in venv for Python installations on Azure App Service
if [ -d "$HOME/site/wwwroot/env" ]; then
    log_info "Ativando ambiente virtual existente..."
    source "$HOME/site/wwwroot/env/bin/activate" || log_error "Falha ao ativar ambiente virtual."
elif [ -d "$HOME/.python_packages" ]; then
    log_info "Usando Python packages em $HOME/.python_packages"
    export PYTHONPATH="$HOME/.python_packages/lib/site-packages:$PYTHONPATH"
fi

# Verify pip installation
if ! command -v pip &> /dev/null; then
    log_error "Pip não encontrado. Verifique a instalação do Python."
fi

log_info "Versão do pip: $(pip --version)"

# Install dependencies with error handling
log_info "Instalando dependências..."
pip install -r "$APP_DIR/requirements.txt" || log_error "Falha ao instalar dependências."

# Set appropriate PYTHONPATH
export PYTHONPATH="$APP_DIR:$PYTHONPATH"
log_info "PYTHONPATH configurado: $PYTHONPATH"

# Set the correct Django settings module
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-"core.settings.prod"}
log_info "DJANGO_SETTINGS_MODULE configurado para: $DJANGO_SETTINGS_MODULE"

# Run database migrations with error handling
log_info "Aplicando migrações do banco de dados..."
$PYTHON_CMD manage.py migrate --noinput || log_error "Falha ao aplicar migrações."

# Collect static files with error handling
log_info "Coletando arquivos estáticos..."
$PYTHON_CMD manage.py collectstatic --noinput --clear || log_error "Falha ao coletar arquivos estáticos."

# Start Gunicorn
log_info "Iniciando o Gunicorn..."
if command -v gunicorn &> /dev/null; then
    gunicorn core.wsgi:application --bind=0.0.0.0:${PORT:-8000} --log-level info --timeout 120
else
    log_info "Gunicorn não encontrado, instalando..."
    pip install gunicorn || log_error "Falha ao instalar Gunicorn."
    gunicorn core.wsgi:application --bind=0.0.0.0:${PORT:-8000} --log-level info --timeout 120
fi