from django.contrib import admin
from .models import Categoria, Marca, Fornecedor, Produto, Produto_Fornecedor

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome_categoria', 'descricao_categoria')
    search_fields = ('nome_categoria',)

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nome_marca',)
    search_fields = ('nome_marca',)

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('nome_fornecedor', 'cnpj', 'telefone', 'email')
    search_fields = ('nome_fornecedor', 'cnpj')

class Produto_FornecedorInline(admin.TabularInline):
    model = Produto_Fornecedor
    extra = 1

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'id_categoria', 'id_marca', 'preco', 'quantidade_estoque')
    list_filter = ('id_categoria', 'id_marca')
    search_fields = ('nome', 'descricao')
    inlines = [Produto_FornecedorInline]
    
    # Custom actions for stock management
    actions = ['increment_stock', 'decrement_stock']
    
    def increment_stock(self, request, queryset):
        for produto in queryset:
            produto.quantidade_estoque += 1
            produto.save()
        self.message_user(request, f"{queryset.count()} produto(s) tiveram seu estoque incrementado.")
    increment_stock.short_description = "Incrementar estoque dos produtos selecionados"
    
    def decrement_stock(self, request, queryset):
        for produto in queryset:
            if produto.quantidade_estoque > 0:
                produto.quantidade_estoque -= 1
                produto.save()
        self.message_user(request, f"{queryset.count()} produto(s) tiveram seu estoque decrementado.")
    decrement_stock.short_description = "Decrementar estoque dos produtos selecionados"

@admin.register(Produto_Fornecedor)
class Produto_FornecedorAdmin(admin.ModelAdmin):
    list_display = ('id_produto', 'id_fornecedor', 'preco_compra', 'prazo_entrega')
    list_filter = ('id_fornecedor',)