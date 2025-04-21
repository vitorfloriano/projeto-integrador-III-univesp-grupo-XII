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
        fields = ['id', 'id_fornecedor', 'nome_fornecedor', 'preco_compra', 'prazo_entrega']

class ProdutoSerializer(serializers.ModelSerializer):
    nome_categoria = serializers.ReadOnlyField(source='id_categoria.nome_categoria')
    nome_marca = serializers.ReadOnlyField(source='id_marca.nome_marca')
    fornecedores = Produto_FornecedorSerializer(source='produto_fornecedor_set', many=True, read_only=True)
    
    class Meta:
        model = Produto
        fields = ['id_produto', 'nome', 'descricao', 'preco', 'quantidade_estoque', 
                  'data_validade', 'id_categoria', 'nome_categoria', 'id_marca', 
                  'nome_marca', 'fornecedores']

class EstoqueUpdateSerializer(serializers.Serializer):
    quantidade = serializers.IntegerField(required=True)
    
    def validate_quantidade(self, value):
        if value <= 0:
            raise serializers.ValidationError("A quantidade deve ser maior que zero.")
        return value