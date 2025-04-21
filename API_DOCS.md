# API Documentation - AutoIta Catálogo de Peças

This document describes the RESTful API endpoints available for AutoIta's parts catalog and inventory management system.

## Base URL

All API endpoints are prefixed with: `/api/`

## Authentication

Currently, the API doesn't require authentication for read operations, but it's recommended to implement proper authentication for production use.

## Endpoints

### Categories (Categorias)

#### List all categories
- **URL**: `/api/categorias/`
- **Method**: `GET`
- **Response**: List of all categories

#### Get a single category
- **URL**: `/api/categorias/{id_categoria}/`
- **Method**: `GET`
- **Response**: Details of the specified category

#### Create a new category
- **URL**: `/api/categorias/`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "nome_categoria": "Nome da categoria",
    "descricao_categoria": "Descrição da categoria"
  }
  ```
- **Response**: Created category details

#### Update a category
- **URL**: `/api/categorias/{id_categoria}/`
- **Method**: `PUT`
- **Body**: Same as for creation
- **Response**: Updated category details

#### Delete a category
- **URL**: `/api/categorias/{id_categoria}/`
- **Method**: `DELETE`
- **Response**: No content (204) if successful

### Brands (Marcas)

#### List all brands
- **URL**: `/api/marcas/`
- **Method**: `GET`
- **Response**: List of all brands

#### Get a single brand
- **URL**: `/api/marcas/{id_marca}/`
- **Method**: `GET`
- **Response**: Details of the specified brand

#### Create a new brand
- **URL**: `/api/marcas/`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "nome_marca": "Nome da marca"
  }
  ```
- **Response**: Created brand details

#### Update a brand
- **URL**: `/api/marcas/{id_marca}/`
- **Method**: `PUT`
- **Body**: Same as for creation
- **Response**: Updated brand details

#### Delete a brand
- **URL**: `/api/marcas/{id_marca}/`
- **Method**: `DELETE`
- **Response**: No content (204) if successful

### Suppliers (Fornecedores)

#### List all suppliers
- **URL**: `/api/fornecedores/`
- **Method**: `GET`
- **Response**: List of all suppliers

#### Get a single supplier
- **URL**: `/api/fornecedores/{id_fornecedor}/`
- **Method**: `GET`
- **Response**: Details of the specified supplier

#### Create a new supplier
- **URL**: `/api/fornecedores/`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "nome_fornecedor": "Nome do fornecedor",
    "cnpj": "XX.XXX.XXX/XXXX-XX",
    "telefone": "(XX) XXXXX-XXXX",
    "email": "email@fornecedor.com"
  }
  ```
- **Response**: Created supplier details

#### Update a supplier
- **URL**: `/api/fornecedores/{id_fornecedor}/`
- **Method**: `PUT`
- **Body**: Same as for creation
- **Response**: Updated supplier details

#### Delete a supplier
- **URL**: `/api/fornecedores/{id_fornecedor}/`
- **Method**: `DELETE`
- **Response**: No content (204) if successful

### Products (Produtos)

#### List all products
- **URL**: `/api/produtos/`
- **Method**: `GET`
- **Query Parameters**:
  - `categoria`: Filter by category ID
  - `marca`: Filter by brand ID
  - `nome`: Filter by product name (partial match)
- **Response**: List of all products (filtered if parameters provided)

#### Get a single product
- **URL**: `/api/produtos/{id_produto}/`
- **Method**: `GET`
- **Response**: Details of the specified product

#### Create a new product
- **URL**: `/api/produtos/`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "nome": "Nome do produto",
    "descricao": "Descrição do produto",
    "preco": "99.99",
    "quantidade_estoque": 10,
    "data_validade": "2025-12-31", // Optional
    "id_categoria": 1,
    "id_marca": 1
  }
  ```
- **Response**: Created product details

#### Update a product
- **URL**: `/api/produtos/{id_produto}/`
- **Method**: `PUT`
- **Body**: Same as for creation
- **Response**: Updated product details

#### Delete a product
- **URL**: `/api/produtos/{id_produto}/`
- **Method**: `DELETE`
- **Response**: No content (204) if successful

### Stock Management

#### Increment stock (Entrada de estoque)
- **URL**: `/api/produtos/{id_produto}/entrada-estoque/`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "quantidade": 5
  }
  ```
- **Response**: 
  ```json
  {
    "message": "Estoque incrementado em 5 unidades.",
    "novo_estoque": 15
  }
  ```

#### Decrement stock (Saída de estoque)
- **URL**: `/api/produtos/{id_produto}/saida-estoque/`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "quantidade": 3
  }
  ```
- **Response**: 
  ```json
  {
    "message": "Estoque decrementado em 3 unidades.",
    "novo_estoque": 7
  }
  ```
- **Error Response** (if insufficient stock):
  ```json
  {
    "error": "Quantidade insuficiente em estoque.",
    "estoque_atual": 10
  }
  ```

### Product-Supplier Relationships (Produto_Fornecedor)

#### List all product-supplier relationships
- **URL**: `/api/produto-fornecedor/`
- **Method**: `GET`
- **Query Parameters**:
  - `produto`: Filter by product ID
  - `fornecedor`: Filter by supplier ID
- **Response**: List of all product-supplier relationships

#### Get a single product-supplier relationship
- **URL**: `/api/produto-fornecedor/{id}/`
- **Method**: `GET`
- **Response**: Details of the specified product-supplier relationship

#### Create a new product-supplier relationship
- **URL**: `/api/produto-fornecedor/`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "id_produto": 1,
    "id_fornecedor": 1,
    "preco_compra": "18.50",
    "prazo_entrega": "3 dias úteis"
  }
  ```
- **Response**: Created product-supplier relationship details

#### Update a product-supplier relationship
- **URL**: `/api/produto-fornecedor/{id}/`
- **Method**: `PUT`
- **Body**: Same as for creation
- **Response**: Updated product-supplier relationship details

#### Delete a product-supplier relationship
- **URL**: `/api/produto-fornecedor/{id}/`
- **Method**: `DELETE`
- **Response**: No content (204) if successful

## Response Formats

All API responses are in JSON format and follow these general structures:

### Success Response
```json
{
  "id_produto": 1,
  "nome": "Filtro de Óleo",
  "descricao": "Filtro de óleo para motores a gasolina",
  "preco": "25.99",
  "quantidade_estoque": 30,
  "data_validade": null,
  "id_categoria": 1,
  "nome_categoria": "Filtros",
  "id_marca": 1,
  "nome_marca": "Fram",
  "fornecedores": [
    {
      "id": 1,
      "id_fornecedor": 1,
      "nome_fornecedor": "Distribuidora XYZ",
      "preco_compra": "18.50",
      "prazo_entrega": "3 dias úteis"
    }
  ]
}
```

### Error Response
```json
{
  "error": "Descrição do erro",
  "detail": "Detalhes sobre o erro, quando disponíveis"
}
```

## Error Codes

- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Authenticated but not authorized
- `404 Not Found`: Resource not found
- `405 Method Not Allowed`: Method not supported for this resource
- `500 Internal Server Error`: Server error