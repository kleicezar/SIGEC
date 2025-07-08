from django.db import models
from registry.models import *
from config.models import Situation, PaymentMethod
from purchase.models import Product
from service.models import Vendaservice

class   Venda(models.Model):
    pessoa = models.ForeignKey(Person,on_delete=models.CASCADE,verbose_name="Pessoa")
    data_da_venda = models.DateTimeField(verbose_name="Data da Venda" )
    observacao_pessoas = models.TextField(verbose_name="Observações sobre as Pessoas",blank=True,null=True)
    observacao_sistema = models.TextField(verbose_name="Observações do Sistema",blank=True,null=True)
    situacao = models.ForeignKey(Situation,on_delete=models.CASCADE,verbose_name="Situação",related_name="vendas",blank=True,null=True)
    is_active = models.BooleanField(default=True, verbose_name='Está Ativo')  # está ativo
    total_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Total", blank=True, null=True)
    product_total = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Total de Produtos")
    discount_total = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Total de Descontos")
    apply_credit = models.BooleanField(default=False,verbose_name='Crédito Aplicado')
    value_apply_credit = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='Valor do Crédito Aplicado',null=True,blank=True,default=0)

    def __str__(self):
        return f"Venda {self.id} - {self.pessoa}"
    
    def save(self, *args, **kwargs):
        if not self.apply_credit:
            self.value_apply_credit = 0.00
        super().save(*args, **kwargs)
           

class VendaItem(models.Model):
    
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, verbose_name="Venda",null=True,blank=True)
    servico =  models.ForeignKey(Vendaservice, on_delete=models.CASCADE, verbose_name="Ordem de Serviço",null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produto",related_name='VendaProduto')
    quantidade = models.PositiveIntegerField(verbose_name="Quantidade do Produto")
    current_quantity = models.PositiveIntegerField(verbose_name="Quantidade atual de Produtos",default=0)
    preco_unitario = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Preço Unitário")
    discount = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Desconto(%)")
    price_total = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Valor Total")
    status = models.CharField(max_length=50,default='Pendente')
    # Calcula o total automaticamente ao salvar a instância
    def save(self, *args, **kwargs):    
        if self.quantidade is not None and self.preco_unitario is not None:
            self.total = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.description} - {self.quantidade} unidades"
        
    
class PaymentMethod_Venda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.SET_NULL, null=True, verbose_name='id_venda')
    forma_pagamento = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, verbose_name='id_forma_de_pagamento')
    expirationDate = models.CharField(max_length=50, verbose_name='Data de Vencimento')
    valor = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Valor Pago:')