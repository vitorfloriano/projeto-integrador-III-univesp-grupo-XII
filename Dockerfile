FROM python:3.12-slim

# Defina variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Cria e define o diretório de trabalho
WORKDIR /app

# Copie os arquivos de requisitos primeiro para aproveitar o cache do Docker
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copie o projeto
COPY . /app/

# Copie o script de inicialização
COPY ./start.sh /app/
RUN chmod +x /app/start.sh

# Exponha a porta que o aplicativo utilizará
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["/app/start.sh"]