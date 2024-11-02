from django.db import models

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
    