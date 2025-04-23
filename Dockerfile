FROM python:3.12-slim

# Defina variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instale pacotes necessários
RUN apt-get update && apt-get install -y netcat-traditional && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Cria e define o diretório de trabalho
WORKDIR /app

# Copie os arquivos de requisitos primeiro para aproveitar o cache do Docker
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copie o projeto
COPY . /app/

# Configurar script de inicialização
RUN chmod +x /app/deployment/docker_startup.sh

# Exponha a porta que o aplicativo utilizará
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["/app/deployment/docker_startup.sh"]