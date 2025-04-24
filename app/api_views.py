from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoModelPermissions
from rest_framework.response import Response
from .models import Categoria, Marca, Fornecedor, Produto, Produto_Fornecedor
from .serializers import (
    CategoriaSerializer, MarcaSerializer, FornecedorSerializer,
    ProdutoSerializer, Produto_FornecedorSerializer, EstoqueUpdateSerializer
)

# Classe de permissão personalizada para permitir leitura a todos, mas restringir modificações
class ReadOnlyOrIsAuthenticated(IsAuthenticated):
    """
    Permite acesso de leitura a qualquer usuário, mas requer autenticação para modificações.
    """
    def has_permission(self, request, view):
        # Permitir GET, HEAD ou OPTIONS para qualquer usuário
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Para outros métodos (POST, PUT, DELETE), requer autenticação
        return super().has_permission(request, view)

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [ReadOnlyOrIsAuthenticated]

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [ReadOnlyOrIsAuthenticated]

class FornecedorViewSet(viewsets.ModelViewSet):
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer
    # Fornecedores contêm dados mais sensíveis, exigindo autenticação completa
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [ReadOnlyOrIsAuthenticated]
    
    def get_queryset(self):
        queryset = Produto.objects.all()
        
        # Filtering by categoria
        categoria_id = self.request.query_params.get('categoria')
        if categoria_id:
            try:
                queryset = queryset.filter(id_categoria=int(categoria_id))
            except (ValueError, TypeError):
                # Proteção contra injeção - retorna conjunto vazio caso o ID não seja válido
                return Produto.objects.none()
            
        # Filtering by marca
        marca_id = self.request.query_params.get('marca')
        if marca_id:
            try:
                queryset = queryset.filter(id_marca=int(marca_id))
            except (ValueError, TypeError):
                return Produto.objects.none()
            
        # Filtering by nome (search)
        nome = self.request.query_params.get('nome')
        if nome:
            queryset = queryset.filter(nome__icontains=nome)
            
        return queryset
    
    @action(detail=True, methods=['post'], url_path='entrada-estoque')
    def entrada_estoque(self, request, pk=None):
        # Verificar se o usuário está autenticado
        if not request.user.is_authenticated:
            return Response({'error': 'Autenticação necessária'}, status=status.HTTP_403_FORBIDDEN)
            
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
        # Verificar se o usuário está autenticado
        if not request.user.is_authenticated:
            return Response({'error': 'Autenticação necessária'}, status=status.HTTP_403_FORBIDDEN)
            
        produto = self.get_object()
        serializer = EstoqueUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            quantidade = serializer.validated_data['quantidade']
            
            if produto.quantidade_estoque >= quantidade:
                produto.quantidade_estoque -= quantidade
                produto.save()
                return Response({'message': f'Estoque reduzido em {quantidade} unidades.', 
                               'novo_estoque': produto.quantidade_estoque},
                              status=status.HTTP_200_OK)
            else:
                return Response({'error': f'Estoque insuficiente. Disponível: {produto.quantidade_estoque}'},
                              status=status.HTTP_400_BAD_REQUEST)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Produto_FornecedorViewSet(viewsets.ModelViewSet):
    queryset = Produto_Fornecedor.objects.all()
    serializer_class = Produto_FornecedorSerializer
    # Relações produto-fornecedor geralmente são informações internas da empresa
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    
    def get_queryset(self):
        queryset = Produto_Fornecedor.objects.all()
        
        # Filtering by produto
        produto_id = self.request.query_params.get('produto')
        if produto_id:
            try:
                queryset = queryset.filter(id_produto=int(produto_id))
            except (ValueError, TypeError):
                return Produto_Fornecedor.objects.none()
            
        # Filtering by fornecedor
        fornecedor_id = self.request.query_params.get('fornecedor')
        if fornecedor_id:
            try:
                queryset = queryset.filter(id_fornecedor=int(fornecedor_id))
            except (ValueError, TypeError):
                return Produto_Fornecedor.objects.none()
            
        return queryset