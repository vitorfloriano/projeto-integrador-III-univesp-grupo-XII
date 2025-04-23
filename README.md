# Projeto Integrador III - UNIVESP Grupo XII - Sistema AutoIta

Este projeto é um sistema de gerenciamento de estoque para autopeças desenvolvido com Django.

## Formas de Execução

O projeto pode ser executado de várias maneiras, dependendo do seu ambiente e necessidades:

### 1. Execução Local com Ambiente Virtual

#### Preparando o ambiente

```bash
# Crie um ambiente virtual
python -m venv projeto

# Ative o ambiente virtual
# No Linux/Mac:
source projeto/bin/activate
# No Windows:
projeto\Scripts\activate
# No PowerShell:
projeto\Scripts\Activate.ps1

# Instale as dependências
pip install -r requirements.txt

# Entre no diretório do projeto
cd PI_2

# Aplique as migrações
python manage.py migrate

# Execute o servidor de desenvolvimento
python manage.py runserver
```

### 2. Execução com Docker (Desenvolvimento)

Para executar o projeto em um ambiente Docker isolado:

```bash
# Construir e iniciar os containers
docker-compose up -d

# Para visualizar os logs
docker-compose logs -f

# Para parar os containers
docker-compose down
```

### 3. Implantação em Produção

Para ambientes de produção, o projeto está configurado para usar variáveis de ambiente para maior segurança e flexibilidade.

#### Usando Docker em Produção

```bash
# Configure as variáveis de ambiente necessárias
export DJANGO_ENV=production
export DJANGO_SECRET_KEY='sua-chave-secreta'
export DEBUG=False
export ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
export DATABASE_ENGINE=sqlite  # ou postgresql

# Para PostgreSQL, defina estas variáveis adicionais
# export DATABASE_NAME=dbpi
# export DATABASE_USER=postgres
# export DATABASE_PASSWORD=senha-segura
# export DATABASE_HOST=db
# export DATABASE_PORT=5432

# Execute o Docker Compose
docker-compose up -d
```

## Configurações de Banco de Dados

O projeto suporta tanto SQLite (padrão) quanto PostgreSQL:

### SQLite (Padrão)
- Não requer configuração adicional
- Ideal para desenvolvimento e testes

### PostgreSQL
- Requer a definição de variáveis de ambiente
- Melhor para ambientes de produção com maior volume de dados
- Configure usando as variáveis DATABASE_* mencionadas acima

## Executando testes

```bash
# No diretório do projeto (PI_2)
python manage.py test
```

## Estrutura da Aplicação

- `app/`: Aplicação principal contendo os modelos e lógica de negócio
- `PI_2/`: Configurações do projeto Django
- `static/`: Arquivos estáticos (CSS, JS, imagens)
- `app/templates/`: Templates HTML
- `app/migrations/`: Migrações do banco de dados

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adicionando nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request


