from django.db import models
from Registry.models import Person
# from Sale.models import *

class PaymentMethod(models.Model):
    name_paymentMethod = models.CharField('Nome da Forma de Pagamento', max_length=50)
    is_Active = models.BooleanField('ativo')

    def __str__(self):
        return self.name_paymentMethod
    
class Situation(models.Model):
    name_Situation = models.CharField('Nome da Situação', max_length=50)
    is_Active = models.BooleanField('ativo')

    def __str__(self):
        return self.name_Situation
    
class Position(models.Model):
    name_position = models.CharField('Nome do Cargo', max_length=25)
    is_Active = models.BooleanField('ativo')

    def __str__(self):
        return self.name_position

class Product(models.Model):
    description = models.CharField(max_length=255, verbose_name='Descrição')  # descrição
    product_code = models.CharField(max_length=100, verbose_name='Código do Produto')  # código do produto
    barcode = models.CharField(max_length=100, verbose_name='Código de Barras')  # código de barras
    unit_of_measure = models.CharField(max_length=50, verbose_name='Unidade de Medida')  # unidade de medida
    brand = models.CharField(max_length=100, verbose_name='Marca')  # marca
    cost_of_product = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Custo do Produto')  # custo do produto
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço de Venda')  # preço de venda
    ncm = models.CharField(max_length=10, verbose_name='NCM')  # NCM (Nomenclatura Comum do Mercosul)
    csosn = models.CharField(max_length=5, verbose_name='CSOSN')  # CSOSN (Código de Situação da Operação de Substituição Tributária)
    cfop = models.CharField(max_length=7, verbose_name='CFOP')  # CFOP (Código Fiscal de Operações e Prestações)
    current_quantity = models.IntegerField(verbose_name='Quantidade Atual')  # quantidade atual
    maximum_quantity = models.IntegerField(verbose_name='Quantidade Máxima')  # quantidade máxima
    minimum_quantity = models.IntegerField(verbose_name='Quantidade Mínima')  # quantidade mínima
    is_active = models.BooleanField(default=True, verbose_name='Está Ativo')  # está ativo
    supplier = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='Fornecedor')  # fornecedor

    def __str__(self):
        return self.description  # retorna a descrição
    
# class Client(models.Model):
#     telefone_pessoal = models.CharField(max_length=15,verbose_name="Telefone Pessoal",blank=True,null=True )
#     telefone_trabalho = models.CharField(max_length=15,verbose_name="Telefone de Trabalho",blank=True,null=True )
#     site = models.URLField(verbose_name="Site",blank=True,null=True )
#     ativo = models.BooleanField(default=True,verbose_name="Está Ativo" )
#     limite_credito = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Limite de Crédito",blank=True,null=True )
#     endereco = models.ForeignKey(Address,on_delete=models.CASCADE,null=True,blank=True,verbose_name="Endereço" )
#     pessoa_fisica = models.OneToOneField(FisicPerson,on_delete=models.CASCADE,verbose_name="Pessoa Física")

#     def __str__(self):
#         return f"Cliente {self.id} - {self.pessoa_fisica}"

# class Venda(models.Model):
#     pessoa = models.ForeignKey(Person,on_delete=models.CASCADE,verbose_name="Pessoa",related_name="vendas")
#     data_da_venda = models.DateTimeField(verbose_name="Data da Venda" )
#     observacao_pessoas = models.TextField(verbose_name="Observações sobre as Pessoas",blank=True,null=True)
#     observacao_sistema = models.TextField(verbose_name="Observações do Sistema",blank=True,null=True)
#     situacao = models.ForeignKey(Situation,on_delete=models.CASCADE,verbose_name="Situação",related_name="vendas")
#     is_active = models.BooleanField(default=True, verbose_name='Está Ativo')  # está ativo
#     total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total", blank=True, null=True)

#     def __str__(self):
#         return f"Venda {self.id} - {self.pessoa}"
           

# class VendaItem(models.Model):
#     venda = models.ForeignKey(Venda, on_delete=models.CASCADE, verbose_name="Venda")
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produto")
#     quantidade = models.PositiveIntegerField(verbose_name="Quantidade do Produto")
#     preco_unitario = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Preço Unitário")

#     # Calcula o total automaticamente ao salvar a instância
#     def save(self, *args, **kwargs):
#         self.total = self.quantidade * self.preco_unitario  # Calcula o total
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.product.description} - {self.quantidade} unidades"

# class PaymentMethod_Venda(models.Model):
#     venda = models.ForeignKey(Venda, on_delete=models.SET_NULL, null=True, verbose_name='id_venda')
#     forma_pagamento = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, verbose_name='id_forma_de_pagamento')
#     expirationDate = models.CharField(max_length=50, verbose_name='Data de Vencimento')
#     valor = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Valor Pago:')

class Compra(models.Model):
    data_da_compra = models.CharField(max_length=10, verbose_name='Data da Compra')
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total", blank=True, null=True)
    fornecedor = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, verbose_name="Fornecedor")
    situacao = models.ForeignKey(Situation, on_delete=models.SET_NULL, null=True, verbose_name="Situação")


    def calcular_total(self):
        self.total = sum(item.subtotal() for item in self.itens.all())
        self.save()

    def __str__(self):
        return f"Compra {self.id} por {self.usuario.username}"
    
class CompraItem(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.SET_NULL, null=True, verbose_name="Compra")
    produto = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Produto")
    quantidade = models.PositiveIntegerField(verbose_name="Quantidade do Produto")
    preco_unitario = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Preço Unitário")

    # Calcula o total automaticamente ao salvar a instância
    def save(self, *args, **kwargs):
        self.total = self.quantidade * self.preco_unitario  # Calcula o total
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.description} - {self.quantidade} unidades"

class PaymentMethod_Compra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.SET_NULL, null=True, verbose_name='id_compra')
    forma_pagamento = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, verbose_name='id_forma_de_pagamento')
    expirationDate = models.CharField(max_length=50, verbose_name='Data de Vencimento')
    valor = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Valor Pago:')

