from django.db import models
from Registry.models import *
from config.models import Situation, PaymentMethod
from purchase.models import Product
# Create your models here.
class Service(models.Model):
    name_Service = models.CharField('Nome do Serviço',max_length=500)
    is_Active = models.BooleanField('ativo',default=True)
    value_Service = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor do Serviço", blank=True, null=True)
    def __str__(self):
        return self.name_Service
    
class VendaService(models.Model):
    pessoa = models.ForeignKey(Person,on_delete=models.CASCADE,verbose_name="Pessoa",related_name="vendaService")
    data_da_venda = models.DateTimeField(verbose_name="Data da Venda" )
    observacao_pessoas = models.TextField(verbose_name="Observações sobre as Pessoas",blank=True,null=True)
    observacao_sistema = models.TextField(verbose_name="Observações do Sistema",blank=True,null=True)
    situacao = models.ForeignKey(Situation,on_delete=models.CASCADE,verbose_name="Situação",related_name="vendaService",blank=True,null=True)
    is_active = models.BooleanField(default=True, verbose_name='Está Ativo') 
    total_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Total", blank=True, null=True)
    product_total = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Total de Produtos")
    discount_total = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Total de Descontos de Produtos")

    service_total = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Total de Servicos")
    discount_total_service = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Total de Descontos")
    total_value_service = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Total", blank=True, null=True)

class VendaItemService(models.Model):
    venda = models.ForeignKey(VendaService, on_delete=models.CASCADE, verbose_name="vendaService")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Servico")
    preco = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Preço Unitário")
    discount = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Desconto(%)")

class VendaItem(models.Model):
    venda = models.ForeignKey(VendaService,on_delete=models.CASCADE, verbose_name="vendaProduct")
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="VendaServiceProduto",related_name='VendaServiceProduto')
    quantidade = models.PositiveIntegerField(verbose_name="Quantidade do Produto")
    preco_unitario = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Preço Unitário")
    discount = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Desconto(%)")
    price_total = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Valor Total")
    status = models.CharField(max_length=50,default='Pendente')
    
class PaymentMethod_VendaService(models.Model):
    venda = models.ForeignKey(VendaService,on_delete=models.SET_NULL,null=True,verbose_name='id_vendaService')
    forma_pagamento = models.ForeignKey(PaymentMethod,on_delete=models.SET_NULL, null=True, verbose_name='id_forma_de_pagamento')
    expirationDate = models.CharField(max_length=50, verbose_name='Data de Vencimento')
    valor = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Valor Pago:')