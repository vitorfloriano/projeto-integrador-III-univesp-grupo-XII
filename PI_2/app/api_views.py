from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Categoria, Marca, Fornecedor, Produto, Produto_Fornecedor
from .serializers import (
    CategoriaSerializer, MarcaSerializer, FornecedorSerializer,
    ProdutoSerializer, Produto_FornecedorSerializer, EstoqueUpdateSerializer
)

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer

class FornecedorViewSet(viewsets.ModelViewSet):
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    
    def get_queryset(self):
        queryset = Produto.objects.all()
        
        # Filtering by categoria
        categoria_id = self.request.query_params.get('categoria')
        if categoria_id:
            queryset = queryset.filter(id_categoria=categoria_id)
            
        # Filtering by marca
        marca_id = self.request.query_params.get('marca')
        if marca_id:
            queryset = queryset.filter(id_marca=marca_id)
            
        # Filtering by nome (search)
        nome = self.request.query_params.get('nome')
        if nome:
            queryset = queryset.filter(nome__icontains=nome)
            
        return queryset
    
    @action(detail=True, methods=['post'], url_path='entrada-estoque')
    def entrada_estoque(self, request, pk=None):
        produto = self.get_object()
        serializer = EstoqueUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            quantidade = serializer.validated_data['quantidade']
            produto.quantidade_estoque += quantidade
            produto.save()
            return Response({'message': f'Estoque incrementado em {quantidade} unidades.', 
                            'novo_estoque': produto.quantidade_estoque},
                           status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='saida-estoque')
    def saida_estoque(self, request, pk=None):
        produto = self.get_object()
        serializer = EstoqueUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            quantidade = serializer.validated_data['quantidade']
            
            if produto.quantidade_estoque >= quantidade:
                produto.quantidade_estoque -= quantidade
                produto.save()
                return Response({'message': f'Estoque decrementado em {quantidade} unidades.', 
                                'novo_estoque': produto.quantidade_estoque},
                               status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Quantidade insuficiente em estoque.', 
                                'estoque_atual': produto.quantidade_estoque},
                               status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Produto_FornecedorViewSet(viewsets.ModelViewSet):
    queryset = Produto_Fornecedor.objects.all()
    serializer_class = Produto_FornecedorSerializer
    
    def get_queryset(self):
        queryset = Produto_Fornecedor.objects.all()
        
        # Filtering by produto
        produto_id = self.request.query_params.get('produto')
        if produto_id:
            queryset = queryset.filter(id_produto=produto_id)
            
        # Filtering by fornecedor
        fornecedor_id = self.request.query_params.get('fornecedor')
        if fornecedor_id:
            queryset = queryset.filter(id_fornecedor=fornecedor_id)
            
        return queryset