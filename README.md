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
- **Banco de Dados**: SQLite (em desenvolvimento) e PostgreSQL (em produção)
- **Deploy**: Azure App Services

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
python -m venv venv

# Ative o ambiente virtual
# No Linux/Mac:
source venv/bin/activate
# No Windows:
venv\Scripts\activate
# No PowerShell:
venv\Scripts\Activate.ps1

# Instale as dependências
pip install -r requirements.txt

# Aplique as migrações
python manage.py makemigrations
python manage.py migrate

# Execute o servidor de desenvolvimento
python manage.py runserver
```

#### Lidando com problemas de porta

Se você encontrar o erro "port already in use", use o seguinte comando para liberar a porta:

```bash
fuser -k 8000/tcp
```

### 2. Usando GitHub Codespaces

#### Prerequisites

- Acesso ao GitHub Codespaces e permissões necessárias para criar um codespace para este repositório.

#### Criando um Codespace

1. Navegue até o repositório no GitHub.
2. Clique no botão `Code` e selecione `Open with Codespaces`.
3. Clique em `New codespace` para criar um novo codespace para este repositório.

#### Configurando o ambiente

1. Uma vez criado o codespace, ele abrirá automaticamente em um ambiente VS Code baseado na web.
2. Abra o terminal no codespace.
3. Crie um ambiente virtual chamado `venv`:
   ```bash
   python -m venv venv
   ```
4. Ative o ambiente virtual:
   - No Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
   - No Windows:
     ```bash
     venv\Scripts\activate
     ```
5. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```
6. Aplique as migrações do banco de dados:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
7. Inicie o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```

#### Lidando com problemas de porta

Se você encontrar o erro "port already in use", use o seguinte comando para liberar a porta:

```bash
fuser -k 8000/tcp
```

## Executando testes

O projeto inclui testes automatizados para garantir o funcionamento correto das funcionalidades:

```bash
python manage.py test
```

## Estrutura da Aplicação

- `app/`: Aplicação principal contendo os modelos e lógica de negócio
- `core/`: Configurações do projeto Django
  - `settings/`: Configurações modularizadas por ambiente
    - `base.py`: Configurações compartilhadas
    - `dev.py`: Configurações para desenvolvimento
    - `prod.py`: Configurações para produção
- `static/`: Arquivos estáticos (CSS, JS, imagens)
- `app/templates/`: Templates HTML para as diferentes seções do site
  - `catalog/`: Templates do catálogo de produtos
  - `homepage/`: Templates da página inicial
  - `contatos/`: Templates da página de contato
  - `formulario/`: Templates para o formulário "Trabalhe Conosco"
- `app/api_views.py`: Endpoints da API REST
- `app/api_urls.py`: URLs da API REST
- `app/serializers.py`: Serializadores para a API REST
- `deployment/`: Scripts e configurações para implantação

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

## Exemplos de Uso da API

### Filtrando Produtos

#### Por Categoria

```bash
GET /api/produtos/?categoria=<categoria_id>
```

#### Por Marca

```bash
GET /api/produtos/?marca=<marca_id>
```

#### Por Nome

```bash
GET /api/produtos/?nome=<nome>
```

### Gerenciamento de Estoque

#### Entrada de Estoque

```bash
POST /api/produtos/<produto_id>/entrada-estoque/
{
  "quantidade": <quantidade>
}
```

#### Saída de Estoque

```bash
POST /api/produtos/<produto_id>/saida-estoque/
{
  "quantidade": <quantidade>
}
```

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adicionando nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request
