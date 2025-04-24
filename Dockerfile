FROM python:3.12-slim

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_ENV=dev

# Instalar pacotes necessários
RUN apt-get update && apt-get install -y netcat-traditional && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Criar e definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de requisitos primeiro para aproveitar o cache do Docker
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copiar o projeto
COPY . /app/

# Garantir que o script de inicialização é executável
RUN chmod +x /app/deployment/docker_startup.sh

# Criar diretório para arquivos estáticos coletados
RUN mkdir -p /app/staticfiles

# Expor a porta que a aplicação utilizará
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["/app/deployment/docker_startup.sh"]