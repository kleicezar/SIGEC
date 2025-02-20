from django.db import models
from Registry.models import Person

class PaymentMethod(models.Model):
    name_paymentMethod = models.CharField('Nome da Forma de Pagamento', max_length=50)
    creditPermission = models.BooleanField('creditPermission',default=False)
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
 