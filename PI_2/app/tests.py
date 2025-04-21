from django.test import TestCase
from .models import Categoria, Marca, Fornecedor, Produto, Produto_Fornecedor
from decimal import Decimal
from django.db import IntegrityError

class CategoriaModelTest(TestCase):
    def test_create_categoria(self):
        categoria = Categoria.objects.create(
            nome_categoria="Peças de Motor",
            descricao_categoria="Componentes e peças para motor automotivo"
        )
        self.assertEqual(categoria.nome_categoria, "Peças de Motor")
        self.assertEqual(categoria.descricao_categoria, "Componentes e peças para motor automotivo")
        self.assertIsNotNone(categoria.id_categoria)
    
    def test_categoria_str_representation(self):
        categoria = Categoria.objects.create(
            nome_categoria="Freios",
            descricao_categoria="Sistemas de freio e componentes"
        )
        self.assertEqual(str(categoria), "Freios")

class MarcaModelTest(TestCase):
    def test_create_marca(self):
        marca = Marca.objects.create(nome_marca="Bosch")
        self.assertEqual(marca.nome_marca, "Bosch")
        self.assertIsNotNone(marca.id_marca)
    
    def test_marca_str_representation(self):
        marca = Marca.objects.create(nome_marca="Continental")
        self.assertEqual(str(marca), "Continental")

class FornecedorModelTest(TestCase):
    def test_create_fornecedor(self):
        fornecedor = Fornecedor.objects.create(
            nome_fornecedor="DistribuidoraABC",
            cnpj="12.345.678/0001-90",
            telefone="(11) 98765-4321",
            email="contato@distribuidoraabc.com"
        )
        self.assertEqual(fornecedor.nome_fornecedor, "DistribuidoraABC")
        self.assertEqual(fornecedor.cnpj, "12.345.678/0001-90")
        self.assertEqual(fornecedor.telefone, "(11) 98765-4321")
        self.assertEqual(fornecedor.email, "contato@distribuidoraabc.com")
        self.assertIsNotNone(fornecedor.id_fornecedor)
    
    def test_fornecedor_str_representation(self):
        fornecedor = Fornecedor.objects.create(
            nome_fornecedor="AutoPeças Distribuição",
            cnpj="98.765.432/0001-10"
        )
        self.assertEqual(str(fornecedor), "AutoPeças Distribuição")
    
    def test_cnpj_unique(self):
        Fornecedor.objects.create(
            nome_fornecedor="Fornecedor1",
            cnpj="11.111.111/0001-11"
        )
        with self.assertRaises(IntegrityError):
            Fornecedor.objects.create(
                nome_fornecedor="Fornecedor2",
                cnpj="11.111.111/0001-11"  # Same CNPJ
            )

class ProdutoModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nome_categoria="Suspensão",
            descricao_categoria="Componentes de suspensão"
        )
        self.marca = Marca.objects.create(nome_marca="Monroe")
    
    def test_create_produto(self):
        produto = Produto.objects.create(
            nome="Amortecedor Dianteiro",
            descricao="Amortecedor para veículos compactos",
            preco=Decimal('159.99'),
            quantidade_estoque=10,
            id_categoria=self.categoria,
            id_marca=self.marca
        )
        self.assertEqual(produto.nome, "Amortecedor Dianteiro")
        self.assertEqual(produto.descricao, "Amortecedor para veículos compactos")
        self.assertEqual(produto.preco, Decimal('159.99'))
        self.assertEqual(produto.quantidade_estoque, 10)
        self.assertEqual(produto.id_categoria, self.categoria)
        self.assertEqual(produto.id_marca, self.marca)
        self.assertIsNotNone(produto.id_produto)
    
    def test_produto_str_representation(self):
        produto = Produto.objects.create(
            nome="Mola Espiral",
            descricao="Mola espiral para suspensão traseira",
            preco=Decimal('89.99'),
            quantidade_estoque=15,
            id_categoria=self.categoria,
            id_marca=self.marca
        )
        self.assertEqual(str(produto), "Mola Espiral")

class ProdutoFornecedorModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nome_categoria="Filtros",
            descricao_categoria="Filtros automotivos"
        )
        self.marca = Marca.objects.create(nome_marca="Fram")
        self.produto = Produto.objects.create(
            nome="Filtro de Óleo",
            descricao="Filtro de óleo para motores a gasolina",
            preco=Decimal('25.99'),
            quantidade_estoque=30,
            id_categoria=self.categoria,
            id_marca=self.marca
        )
        self.fornecedor = Fornecedor.objects.create(
            nome_fornecedor="Distribuidora XYZ",
            cnpj="55.444.333/0001-22",
            telefone="(21) 98888-7777",
            email="vendas@distribuidoraxyz.com"
        )
    
    def test_create_produto_fornecedor(self):
        produto_fornecedor = Produto_Fornecedor.objects.create(
            id_produto=self.produto,
            id_fornecedor=self.fornecedor,
            preco_compra=Decimal('18.50'),
            prazo_entrega="3 dias úteis"
        )
        self.assertEqual(produto_fornecedor.id_produto, self.produto)
        self.assertEqual(produto_fornecedor.id_fornecedor, self.fornecedor)
        self.assertEqual(produto_fornecedor.preco_compra, Decimal('18.50'))
        self.assertEqual(produto_fornecedor.prazo_entrega, "3 dias úteis")
    
    def test_produto_fornecedor_str_representation(self):
        produto_fornecedor = Produto_Fornecedor.objects.create(
            id_produto=self.produto,
            id_fornecedor=self.fornecedor,
            preco_compra=Decimal('18.50'),
            prazo_entrega="3 dias úteis"
        )
        self.assertEqual(str(produto_fornecedor), "Filtro de Óleo - Distribuidora XYZ")
