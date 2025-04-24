#!/bin/bash
# Unified startup script for both development and production environments

# Function for error logging
log_error() {
    echo "ERROR: $1" >&2
    exit 1
}

# Function for info logging
log_info() {
    echo "INFO: $1"
}

# Set environment variable based on DJANGO_ENV or auto-detect based on environment
export DJANGO_ENV=${DJANGO_ENV:-"dev"}
log_info "DJANGO_ENV configurado para: $DJANGO_ENV"

# Ensure Python is available
if command -v python3 &> /dev/null; then
    log_info "Using Python 3: $(python3 --version)"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    log_info "Using Python: $(python --version)"
    PYTHON_CMD="python"
else
    log_info "Python not found in PATH. Installing dependencies..."
    pip install -r requirements.txt || log_error "Failed to install dependencies"
    PYTHON_CMD="python"
fi

# Install gunicorn if not available
if ! command -v gunicorn &> /dev/null; then
    log_info "Installing Gunicorn..."
    pip install gunicorn || log_error "Failed to install Gunicorn"
fi

# Define o diretório da aplicação
APP_DIR=$(pwd)
cd $APP_DIR

# Colete arquivos estáticos
log_info "Coletando arquivos estáticos..."
$PYTHON_CMD manage.py collectstatic --noinput || log_error "Failed to collect static files"

# Aplique as migrações
log_info "Aplicando migrações..."
$PYTHON_CMD manage.py migrate --noinput || log_error "Failed to apply migrations"

# Set Django settings module based on environment
if [ "$DJANGO_ENV" = "prod" ]; then
  export DJANGO_SETTINGS_MODULE="core.settings.prod"
else
  export DJANGO_SETTINGS_MODULE="core.settings.dev"
fi
log_info "DJANGO_SETTINGS_MODULE set to: $DJANGO_SETTINGS_MODULE"

# Inicie o servidor baseado no ambiente
if [ "$DJANGO_ENV" = "dev" ]; then
  log_info "Iniciando servidor de desenvolvimento Django..."
  $PYTHON_CMD manage.py runserver 0.0.0.0:${PORT:-8000}
else
  log_info "Iniciando servidor Gunicorn para produção..."
  gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers ${GUNICORN_WORKERS:-3} --timeout ${GUNICORN_TIMEOUT:-120}
fi
