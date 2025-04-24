from django.db import models

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nome_categoria = models.CharField(max_length=100)
    descricao_categoria = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome_categoria


class Marca(models.Model):
    id_marca = models.AutoField(primary_key=True)
    nome_marca = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

    def __str__(self):
        return self.nome_marca


class Fornecedor(models.Model):
    id_fornecedor = models.AutoField(primary_key=True)
    nome_fornecedor = models.CharField(max_length=150)
    cnpj = models.CharField(max_length=18, unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'

    def __str__(self):
        return self.nome_fornecedor


class Produto(models.Model):
    id_produto = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_estoque = models.IntegerField(default=0)
    data_validade = models.DateField(blank=True, null=True)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='produtos')
    id_marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='produtos')
    fornecedores = models.ManyToManyField(Fornecedor, through='Produto_Fornecedor')
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.nome


class Produto_Fornecedor(models.Model):
    id_produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    id_fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    preco_compra = models.DecimalField(max_digits=10, decimal_places=2)
    prazo_entrega = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Produto-Fornecedor'
        verbose_name_plural = 'Produtos-Fornecedores'
        unique_together = ['id_produto', 'id_fornecedor']

    def __str__(self):
        return f"{self.id_produto.nome} - {self.id_fornecedor.nome_fornecedor}"