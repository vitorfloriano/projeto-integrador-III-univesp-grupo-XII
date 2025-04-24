from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    CategoriaViewSet, MarcaViewSet, FornecedorViewSet,
    ProdutoViewSet, Produto_FornecedorViewSet
)

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'marcas', MarcaViewSet)
router.register(r'fornecedores', FornecedorViewSet)
router.register(r'produtos', ProdutoViewSet)
router.register(r'produto-fornecedor', Produto_FornecedorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]