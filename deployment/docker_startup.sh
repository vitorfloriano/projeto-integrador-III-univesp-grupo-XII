#!/bin/bash
# Startup script for Docker/container environments

# Set environment variable based on DJANGO_ENV or default to prod if not specified
export DJANGO_ENV=${DJANGO_ENV:-"dev"}
echo "DJANGO_ENV configurado para: $DJANGO_ENV"

# Espere até que o banco de dados esteja disponível (se estiver usando PostgreSQL)
if [ "$DATABASE_ENGINE" = "postgresql" ]; then
  echo "Aguardando o banco de dados PostgreSQL..."
  while ! nc -z ${DATABASE_HOST:-localhost} ${DATABASE_PORT:-5432}; do
    sleep 2
    echo "Ainda esperando o PostgreSQL..."
  done
  echo "Banco de dados disponível!"
fi

# Navegue para o diretório do projeto Django
cd /app

# Exibir estrutura do diretório para debug
echo "Conteúdo do diretório atual:"
ls -la

# Verificar variáveis de ambiente críticas
echo "Verificando variáveis de ambiente:"
echo "DJANGO_ENV=${DJANGO_ENV}"
echo "DATABASE_ENGINE=${DATABASE_ENGINE}"
echo "DATABASE_HOST=${DATABASE_HOST}"
echo "DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-core.settings}"

# Definir DJANGO_SETTINGS_MODULE se não estiver definido
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-core.settings}

# Colete arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Aplique as migrações
echo "Aplicando migrações..."
python manage.py migrate --noinput

# Inicie o servidor
echo "Iniciando servidor Gunicorn..."
gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers ${GUNICORN_WORKERS:-3} --timeout ${GUNICORN_TIMEOUT:-120} --log-level debug