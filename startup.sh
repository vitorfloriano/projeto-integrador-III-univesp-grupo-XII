#!/bin/bash
# Unified startup script for both development and production environments

# Set environment variable based on DJANGO_ENV or auto-detect based on environment
if [ -n "$WEBSITE_HOSTNAME" ]; then
  # Azure environment detected
  export DJANGO_ENV="prod"
else
  # Default to the specified environment or use dev if not specified
  export DJANGO_ENV=${DJANGO_ENV:-"dev"}
fi
echo "DJANGO_ENV configurado para: $DJANGO_ENV"

# Espere até que o banco de dados esteja disponível (se estiver usando PostgreSQL)
if [ "$DATABASE_ENGINE" = "postgresql" ]; then
  echo "Aguardando o banco de dados PostgreSQL..."
  while ! nc -z ${DATABASE_HOST:-localhost} ${DATABASE_PORT:-5432}; do
    sleep 0.1
  done
  echo "Banco de dados disponível!"
fi

# Define o diretório da aplicação
APP_DIR=$(pwd)
cd $APP_DIR

# Colete arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Aplique as migrações
echo "Aplicando migrações..."
python manage.py migrate --noinput

# Inicie o servidor baseado no ambiente
if [ "$DJANGO_ENV" = "dev" ]; then
  echo "Iniciando servidor de desenvolvimento Django..."
  python manage.py runserver 0.0.0.0:${PORT:-8000}
else
  echo "Iniciando servidor Gunicorn para produção..."
  gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers ${GUNICORN_WORKERS:-3} --timeout ${GUNICORN_TIMEOUT:-120}
fi