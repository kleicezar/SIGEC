from django.db import models
from registry.models import Person
from config.models import Situation, PaymentMethod

class Product(models.Model):
    description = models.CharField(max_length=255, verbose_name='Descrição')  # descrição
    product_code = models.CharField(max_length=100, verbose_name='Código do Produto')  # código do produto
    barcode = models.CharField(max_length=100, verbose_name='Código de Barras')  # código de barras
    unit_of_measure = models.CharField(max_length=50, verbose_name='Unidade de Medida')  # unidade de medida
    brand = models.CharField(max_length=100, verbose_name='Marca')                      # marca
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

class Compra(models.Model):
    data_da_compra = models.DateTimeField(verbose_name='Data da Compra')
    total_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total", blank=True, null=True)
    product_total =  models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Total de Produtos")
    discount_total = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Total de Descontos")
    fornecedor = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, verbose_name="Fornecedor")
    situacao = models.ForeignKey(Situation, on_delete=models.SET_NULL, null=True,blank=True, verbose_name="Situação")
    is_active = models.BooleanField(default=True, verbose_name='Está Ativo')  # está ativo

    observation_product =  models.TextField(verbose_name='Observação sobre Produtos',null=True,blank=True)

    rmnExists = models.BooleanField(default=False,verbose_name='Romaneio')
    freightExists = models.BooleanField(default=False,verbose_name='Frete')
    taxExists = models.BooleanField(default=False,verbose_name='Imposto')

    def __str__(self):
        return f"Compra {self.id} por "
class Frete(models.Model):
    FREIGHT_CHOICES = [
        ('FOB','FOB'),
        ('CIF','CIF')
    ]
    compra = models.ForeignKey(Compra,on_delete=models.SET_NULL, null=True, blank=True)
    freight_type = models.CharField(choices=FREIGHT_CHOICES,max_length=3,verbose_name='Tipo de Frete',null=True, blank=True)
    valueFreight = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Valor do Frete',null=True,blank=True)
    numberOfInstallmentsFreight = models.IntegerField(verbose_name='Número de Parcelas',null=True,blank=True)
    observation_freight = models.TextField(verbose_name='Observação sobre Frete',null=True,blank=True)
  

class Tax(models.Model):
    compra = models.ForeignKey(Compra,on_delete=models.SET_NULL, null=True, blank=True)
    valueTax =  models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Valor do Imposto')
    numberOfInstallmentsTax = models.IntegerField(verbose_name='Número de Parcelas')
    observation_tax = models.TextField(verbose_name='Observação sobre Imposto',null=True,blank=True)


class PickingList(models.Model):
    compra = models.ForeignKey(Compra,on_delete=models.SET_NULL, null=True, blank=True)
    valuePickingList = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Valor do RMN')
    numberOfInstallmentsRMN = models.IntegerField(verbose_name='Número de Parcelas')
    observation_picking_list = models.TextField(verbose_name='Observação sobre Romaneio',null=True,blank=True)

class CompraItem(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.SET_NULL, null=True, verbose_name="Compra")
    produto = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Produto")
    quantidade = models.PositiveIntegerField(verbose_name="Quantidade do Produto")
    preco_unitario = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Preço Unitário")
    discount = models.DecimalField(max_digits=5, decimal_places=2) # porcentagem aplicada no produto
    price_total = models.DecimalField(max_digits=10, decimal_places=2) # valor total do produto
    status = models.CharField(max_length=50,default='Pendente')

    # Calcula o total automaticamente ao salvar a instância
    def save(self, *args, **kwargs):
        self.total = self.quantidade * self.preco_unitario  # Calcula o total
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.produto.description} - {self.quantidade} unidades"

# class PaymentMethod_Compra(models.Model):
#     compra = models.ForeignKey(Compra, on_delete=models.SET_NULL, null=True, verbose_name='id_compra')
#     forma_pagamento = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, verbose_name='id_forma_de_pagamento')
#     expirationDate = models.CharField(max_length=50, verbose_name='Data de Vencimento')
#     valor = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Valor Pago:')

