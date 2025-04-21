from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from decimal import Decimal
from .models import Categoria, Marca, Fornecedor, Produto, Produto_Fornecedor

class CategoriaAPITests(APITestCase):
    def test_create_categoria(self):
        """
        Ensure we can create a new categoria.
        """
        url = '/api/categorias/'
        data = {'nome_categoria': 'Categoria de Teste', 'descricao_categoria': 'Descrição de teste'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Categoria.objects.count(), 1)
        self.assertEqual(Categoria.objects.get().nome_categoria, 'Categoria de Teste')

    def test_get_categorias(self):
        """
        Ensure we can get a list of categorias.
        """
        Categoria.objects.create(nome_categoria='Categoria 1', descricao_categoria='Descrição 1')
        Categoria.objects.create(nome_categoria='Categoria 2', descricao_categoria='Descrição 2')
        url = '/api/categorias/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class MarcaAPITests(APITestCase):
    def test_create_marca(self):
        """
        Ensure we can create a new marca.
        """
        url = '/api/marcas/'
        data = {'nome_marca': 'Marca de Teste'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Marca.objects.count(), 1)
        self.assertEqual(Marca.objects.get().nome_marca, 'Marca de Teste')

    def test_get_marcas(self):
        """
        Ensure we can get a list of marcas.
        """
        Marca.objects.create(nome_marca='Marca 1')
        Marca.objects.create(nome_marca='Marca 2')
        url = '/api/marcas/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class ProdutoAPITests(APITestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nome_categoria='Categoria de Teste',
            descricao_categoria='Descrição de teste'
        )
        self.marca = Marca.objects.create(nome_marca='Marca de Teste')
        self.produto = Produto.objects.create(
            nome='Produto de Teste',
            descricao='Descrição do produto de teste',
            preco=Decimal('99.99'),
            quantidade_estoque=10,
            id_categoria=self.categoria,
            id_marca=self.marca
        )

    def test_get_produtos(self):
        """
        Ensure we can get a list of produtos.
        """
        url = '/api/produtos/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_produtos_by_categoria(self):
        """
        Ensure we can filter produtos by categoria.
        """
        url = f'/api/produtos/?categoria={self.categoria.id_categoria}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_produtos_by_marca(self):
        """
        Ensure we can filter produtos by marca.
        """
        url = f'/api/produtos/?marca={self.marca.id_marca}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_produtos_by_nome(self):
        """
        Ensure we can filter produtos by nome.
        """
        url = '/api/produtos/?nome=Teste'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class EstoqueAPITests(APITestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome_categoria='Categoria de Teste')
        self.marca = Marca.objects.create(nome_marca='Marca de Teste')
        self.produto = Produto.objects.create(
            nome='Produto de Teste',
            descricao='Descrição do produto de teste',
            preco=Decimal('99.99'),
            quantidade_estoque=10,
            id_categoria=self.categoria,
            id_marca=self.marca
        )

    def test_entrada_estoque(self):
        """
        Ensure we can increment stock quantity.
        """
        url = f'/api/produtos/{self.produto.id_produto}/entrada-estoque/'
        data = {'quantidade': 5}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.quantidade_estoque, 15)

    def test_saida_estoque(self):
        """
        Ensure we can decrement stock quantity.
        """
        url = f'/api/produtos/{self.produto.id_produto}/saida-estoque/'
        data = {'quantidade': 3}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.quantidade_estoque, 7)

    def test_saida_estoque_insuficiente(self):
        """
        Ensure we cannot decrement more than available stock.
        """
        url = f'/api/produtos/{self.produto.id_produto}/saida-estoque/'
        data = {'quantidade': 20}  # More than available (10)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.quantidade_estoque, 10)  # Unchanged