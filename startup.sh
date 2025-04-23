#!/bin/bash

# Diretório base da aplicação
APP_DIR="$HOME/site/wwwroot"
echo "Diretório da aplicação: $APP_DIR"
echo "Listando conteúdo do diretório da aplicação:"
ls -la "$APP_DIR"

# Verificar se o diretório do projeto existe
if [ -d "$APP_DIR/PI_2" ]; then
    echo "Diretório PI_2 encontrado"
    ls -la "$APP_DIR/PI_2"
else
    echo "ERRO: Diretório PI_2 não encontrado!"
fi

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
export PYTHONPATH="$APP_DIR:$APP_DIR/PI_2:$PYTHONPATH"
echo "PYTHONPATH configurado: $PYTHONPATH"

# Verificação se os arquivos necessários existem
if [ -f "$APP_DIR/PI_2/manage.py" ]; then
    echo "manage.py encontrado"
else
    echo "ERRO: manage.py não encontrado!"
fi

if [ -f "$APP_DIR/PI_2/PI_2/wsgi.py" ]; then
    echo "wsgi.py encontrado"
else
    echo "ERRO: wsgi.py não encontrado!"
fi

# Navegação para o diretório do projeto
cd "$APP_DIR"

# Aplicação das migrações
echo "Aplicando migrações do banco de dados..."
cd PI_2
python manage.py migrate --noinput

# Coleta de arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear

# Voltando para o diretório raiz
cd "$APP_DIR"

# Testar se o módulo PI_2 está acessível
python -c "import sys; print(sys.path); try: import PI_2; print('Módulo PI_2 importado com sucesso!'); except Exception as e: print(f'Erro ao importar PI_2: {e}')"

# Iniciando o Gunicorn com o arquivo wsgi_app.py na raiz
echo "Iniciando o Gunicorn com wsgi_app.py..."
echo "Comandos alternativos que podem ser usados em caso de falha:"
echo "gunicorn --pythonpath $APP_DIR PI_2.wsgi:application --bind=0.0.0.0:8000"
echo "gunicorn --pythonpath $APP_DIR/PI_2 PI_2.wsgi:application --bind=0.0.0.0:8000"

# Usando --pythonpath para garantir que o Gunicorn encontre os módulos
gunicorn --pythonpath "$APP_DIR" wsgi_app:application --bind=0.0.0.0:8000 --log-level debug --timeout 120
