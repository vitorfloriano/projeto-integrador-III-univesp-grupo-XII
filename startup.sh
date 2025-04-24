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
if [ -n "$WEBSITE_HOSTNAME" ]; then
  # Azure environment detected
  export DJANGO_ENV="prod"
else
  # Default to the specified environment or use dev if not specified
  export DJANGO_ENV=${DJANGO_ENV:-"dev"}
fi
log_info "DJANGO_ENV configurado para: $DJANGO_ENV"

# Ensure Python is available in Azure App Service Linux
if [ -d "$HOME/site/wwwroot/env" ]; then
    log_info "Activating existing virtual environment..."
    source "$HOME/site/wwwroot/env/bin/activate" || log_error "Failed to activate virtual environment"
    PYTHON_CMD="python"
elif command -v python3 &> /dev/null; then
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

# Espere até que o banco de dados esteja disponível (se estiver usando PostgreSQL)
if [ "$DATABASE_ENGINE" = "postgresql" ]; then
  log_info "Aguardando o banco de dados PostgreSQL..."
  while ! nc -z ${DATABASE_HOST:-localhost} ${DATABASE_PORT:-5432}; do
    sleep 0.1
  done
  log_info "Banco de dados disponível!"
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

# Inicie o servidor baseado no ambiente
if [ "$DJANGO_ENV" = "dev" ]; then
  log_info "Iniciando servidor de desenvolvimento Django..."
  $PYTHON_CMD manage.py runserver 0.0.0.0:${PORT:-8000}
else
  log_info "Iniciando servidor Gunicorn para produção..."
  gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers ${GUNICORN_WORKERS:-3} --timeout ${GUNICORN_TIMEOUT:-120}
fi
