#!/bin/bash
# Startup script for Docker/container environments

# Espere até que o banco de dados esteja disponível (se estiver usando PostgreSQL)
if [ "$DATABASE_ENGINE" = "postgresql" ]; then
  echo "Aguardando o banco de dados PostgreSQL..."
  while ! nc -z ${DATABASE_HOST:-localhost} ${DATABASE_PORT:-5432}; do
    sleep 0.1
  done
  echo "Banco de dados disponível!"
fi

# Navegue para o diretório do projeto Django
cd /app/PI_2

# Colete arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Aplique as migrações
echo "Aplicando migrações..."
python manage.py migrate --noinput

# Inicie o servidor
echo "Iniciando servidor Gunicorn..."
gunicorn PI_2.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers ${GUNICORN_WORKERS:-3} --timeout ${GUNICORN_TIMEOUT:-120}