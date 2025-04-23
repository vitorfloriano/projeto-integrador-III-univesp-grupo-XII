#!/bin/bash

# Espere até que o banco de dados esteja disponível (se estiver usando PostgreSQL)
# Se estiver usando SQLite, pode remover esta parte
# Se estiver usando outros bancos de dados, ajuste conforme necessário
if [ "$DATABASE_ENGINE" = "postgresql" ]; then
  echo "Aguardando o banco de dados PostgreSQL..."
  while ! nc -z ${DATABASE_HOST:-localhost} ${DATABASE_PORT:-5432}; do
    sleep 0.1
  done
  echo "Banco de dados disponível!"
fi

# Navegue para o diretório do projeto Django
cd PI_2

# Colete arquivos estáticos
python manage.py collectstatic --noinput

# Aplique as migrações
python manage.py migrate --noinput

# Inicie o servidor
if [ "$DJANGO_ENV" = "production" ]; then
  # Em produção, use gunicorn ou outro servidor WSGI
  gunicorn PI_2.wsgi:application --bind 0.0.0.0:8000
else
  # Em desenvolvimento, use o servidor de desenvolvimento do Django
  python manage.py runserver 0.0.0.0:8000
fi