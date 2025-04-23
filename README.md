# Projeto Integrador III - UNIVESP Grupo XII - Sistema AutoIta

Este projeto é um sistema de gerenciamento de estoque e catálogo online para a loja de autopeças AutoIta, desenvolvido com Django e Django REST Framework.

## Funcionalidades

- **Catálogo de Produtos**: Interface amigável para visualização do estoque de peças
- **Sistema de Filtros**: Busca de produtos por categoria, marca ou nome
- **Gerenciamento de Estoque**: Controle de entrada e saída de produtos
- **API REST**: Endpoints para integração com outros sistemas
- **Painel Administrativo**: Interface de administração completa para gerenciamento de dados
- **Interface Responsiva**: Suporte a dispositivos móveis e desktop
- **Tema Claro/Escuro**: Opção de alternância entre temas

## Tecnologias Utilizadas

- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, CSS, JavaScript
- **Banco de Dados**: PostgreSQL (em produção) e SQLite (em desenvolvimento)
- **Containerização**: Docker e Docker Compose
- **Deploy**: Azure App Service, configuração para ambientes de produção com variáveis de ambiente

## API REST

O sistema conta com uma API REST completa para:

- Gerenciamento de Categorias
- Gerenciamento de Marcas
- Gerenciamento de Fornecedores
- Gerenciamento de Produtos
- Controle de Estoque (entrada e saída)
- Relacionamento entre Produtos e Fornecedores

Para mais informações, consulte a documentação detalhada da API no arquivo `API_DOCS.md`.

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
export DATABASE_ENGINE=postgresql

# Para PostgreSQL, defina estas variáveis adicionais
export DATABASE_NAME=dbpi
export DATABASE_USER=postgres
export DATABASE_PASSWORD=senha-segura
export DATABASE_HOST=db
export DATABASE_PORT=5432

# Execute o Docker Compose
docker-compose up -d
```

### 4. Implantação no Azure App Service

O projeto está configurado para ser implantado no Azure App Service, permitindo escalabilidade e gerenciamento simplificado.

#### Configurando o Azure App Service

1. **Crie um App Service no Portal do Azure**:
   - Escolha "Web App" como tipo de aplicação
   - Selecione "Python" como runtime stack
   - Escolha Python 3.12 ou superior

2. **Configure as variáveis de ambiente**:
   - No portal do Azure, acesse "Configuration" > "Application settings"
   - Adicione as seguintes variáveis:
     - `DJANGO_ENV=production`
     - `DJANGO_SECRET_KEY=sua-chave-secreta`
     - `DEBUG=False`
     - `ALLOWED_HOSTS=seu-app.azurewebsites.net`
     - `SCM_DO_BUILD_DURING_DEPLOYMENT=true`
     - `WEBSITE_WEBDEPLOY_USE_SCM=false`

3. **Deploy via GitHub Actions ou Azure DevOps**:
   - Configure o pipeline para usar o arquivo `azure.yml` incluído neste repositório
   - O script `startup.sh` será executado para configurar o ambiente e iniciar a aplicação

4. **Deploy manual via ZIP Deploy**:
   ```bash
   # Prepare o projeto para deploy
   pip install -r requirements.txt
   cd PI_2
   python manage.py collectstatic --noinput
   
   # Comprima o projeto
   cd ..
   zip -r app.zip .
   
   # Faça upload utilizando o Azure CLI
   az webapp deployment source config-zip --resource-group <seu-grupo-recursos> --name <seu-app-service> --src app.zip
   ```

5. **Solução de Problemas Comuns**:
   - Se a aplicação não iniciar, verifique os logs no portal do Azure
   - Certifique-se de que o caminho WSGI está correto em `startup.sh`
   - Verifique se todas as dependências estão em `requirements.txt`

## Executando testes

O projeto inclui testes automatizados para garantir o funcionamento correto das funcionalidades:

```bash
# No diretório do projeto (PI_2)
python manage.py test
```

## Estrutura da Aplicação

- `app/`: Aplicação principal contendo os modelos e lógica de negócio
- `PI_2/`: Configurações do projeto Django
- `static/`: Arquivos estáticos (CSS, JS, imagens)
- `app/templates/`: Templates HTML para as diferentes seções do site
  - `catalog/`: Templates do catálogo de produtos
  - `homepage/`: Templates da página inicial
  - `contatos/`: Templates da página de contato
  - `formulario/`: Templates para o formulário "Trabalhe Conosco"
- `app/api_views.py`: Endpoints da API REST
- `app/api_urls.py`: URLs da API REST
- `app/serializers.py`: Serializadores para a API REST
- `Scripts_Database/`: Scripts para povoamento inicial do banco de dados

## Modelos de Dados

O sistema é composto pelos seguintes modelos principais:

- **Categoria**: Categorias de produtos
- **Marca**: Marcas de produtos
- **Fornecedor**: Dados de fornecedores
- **Produto**: Informações de produtos, incluindo estoque
- **Produto_Fornecedor**: Relacionamento entre produtos e fornecedores

## Funcionalidades da API

- Filtragem de produtos por categoria, marca e nome
- Controle de permissões baseado em autenticação
- Endpoints para gestão de estoque (entrada/saída)
- Documentação completa de todos os endpoints

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adicionando nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request


