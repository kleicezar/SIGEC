from django.db import models
from Registry.models import Person

class PaymentMethod(models.Model):
    # CONSIDERINCASH = [
    #     ('entrada', 'Entrada'),
    #     ('saida', 'Saída'),

    # ]
    name_paymentMethod = models.CharField('Nome da Forma de Pagamento', max_length=50)
    creditPermission = models.BooleanField('creditPermission',default=False)
    is_Active = models.BooleanField('ativo',default=True)
    considerInCash = models.BooleanField('considerar em caixa', default=False, blank=True, null=True) 
    # considerInCash = models.CharField('considerar em caixa',choices= CONSIDERINCASH, default=False, blank=True, null=True, max_length=50)
    is_Active = models.BooleanField('ativo',default=True) 

    def __str__(self):
        return self.name_paymentMethod

class ChartOfAccounts(models.Model): 
    name_ChartOfAccounts = models.CharField('Nome do Plano de Contas', max_length=50)
    is_Active = models.BooleanField('ativo',default=True)

    def __str__(self):
        return self.name_ChartOfAccounts
    
class Situation(models.Model):
    name_Situation = models.CharField('Nome da Situação', max_length=50)
    is_Active = models.BooleanField('ativo',default=True)

    def __str__(self):
        return self.name_Situation
    
class Position(models.Model):
    name_position = models.CharField('Nome do Cargo', max_length=25)
    is_Active = models.BooleanField('ativo',default=True)

    def __str__(self):
        return self.name_position
 
class Service(models.Model):
    name_Service = models.CharField('Nome do Serviço',max_length=500)
    is_Active = models.BooleanField('ativo',default=True)
    value_Service = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor do Serviço", blank=True, null=True)
    
    def __str__(self):
        return self.name_Service