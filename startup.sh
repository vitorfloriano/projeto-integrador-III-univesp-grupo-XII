#!/bin/bash

# Diretório base da aplicação
APP_DIR="$HOME/site/wwwroot"
echo "Diretório da aplicação: $APP_DIR"

# Ativação do ambiente virtual (caso exista)
if [ -d "$HOME/antenv" ]; then
    echo "Ativando ambiente virtual encontrado"
    source $HOME/antenv/bin/activate
else
    echo "Ambiente virtual não encontrado, criando novo..."
    python -m venv "$HOME/antenv"
    source $HOME/antenv/bin/activate
fi

# Verificação das versões
echo "Versão do Python: $(python --version)"
echo "Versão do pip: $(pip --version)"

# Instalação das dependências
echo "Instalando dependências..."
pip install -r "$APP_DIR/requirements.txt"

# Configuração do PYTHONPATH para garantir que os módulos sejam encontrados
export PYTHONPATH="$APP_DIR:$PYTHONPATH"
echo "PYTHONPATH configurado: $PYTHONPATH"

# Navegação para o diretório do projeto
cd "$APP_DIR"

# Aplicação das migrações
echo "Aplicando migrações do banco de dados..."
cd PI_2
python manage.py migrate --noinput

# Coleta de arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Voltando para o diretório raiz
cd "$APP_DIR"

# Iniciando o Gunicorn com o arquivo wsgi_app.py na raiz
echo "Iniciando o Gunicorn com wsgi_app.py..."
gunicorn --log-level debug --bind=0.0.0.0:8000 wsgi_app:application
