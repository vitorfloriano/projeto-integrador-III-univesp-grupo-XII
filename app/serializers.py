from rest_framework import serializers
from .models import Categoria, Marca, Fornecedor, Produto, Produto_Fornecedor

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'

class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = '__all__'

class Produto_FornecedorSerializer(serializers.ModelSerializer):
    nome_fornecedor = serializers.ReadOnlyField(source='id_fornecedor.nome_fornecedor')
    
    class Meta:
        model = Produto_Fornecedor
        fields = ['id', 'id_produto', 'id_fornecedor', 'nome_fornecedor', 'preco_compra', 'prazo_entrega']

class ProdutoSerializer(serializers.ModelSerializer):
    nome_categoria = serializers.ReadOnlyField(source='id_categoria.nome_categoria')
    nome_marca = serializers.ReadOnlyField(source='id_marca.nome_marca')
    
    class Meta:
        model = Produto
        fields = ['id_produto', 'nome', 'descricao', 'preco', 'quantidade_estoque', 
                  'data_validade', 'id_categoria', 'id_marca', 'nome_categoria', 'nome_marca']

class EstoqueUpdateSerializer(serializers.Serializer):
    quantidade = serializers.IntegerField(min_value=1)