from django.db import models

class geral(models.Model):
    class Meta:
        verbose_name_plural = 'Tabelas Gerais'
    
    nome = models.CharField(max_length=80)
    idade = models.IntegerField()
    CPF = models.CharField(max_length=14)
    RG = models.CharField(max_length=12)
    admissao = models.CharField(max_length=10)
    cargo = models.CharField(max_length=80)
    salario = models.CharField()

    def __str__(self):
        return self.nome
    
class empresa2(models.Model):
    class Meta:
        verbose_name_plural = 'Exemplo Empresa 1 ----------- CNPJ 11.111.111/1111-11'
    
    nome = models.CharField(max_length=80)
    idade = models.IntegerField()
    CPF = models.CharField(max_length=14)
    RG = models.CharField(max_length=12)
    admissao = models.CharField(max_length=10)
    cargo = models.CharField(max_length=80)
    salario = models.CharField()
    
    def __str__(self):
        return self.nome

class empresa3(models.Model):
    class Meta:
        verbose_name_plural = 'Exemplo Empresa 2 ----------- CNPJ 22.222.222/2222-22'
    
    nome = models.CharField(max_length=80)
    idade = models.IntegerField()
    CPF = models.CharField(max_length=14)
    RG = models.CharField(max_length=12)
    admissao = models.CharField(max_length=10)
    cargo = models.CharField(max_length=80)
    salario = models.CharField()

    def __str__(self):
        return self.nome