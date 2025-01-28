from django.db import models
from Registry.models import Person
from config.models import ChartOfAccounts, PaymentMethod, Situation

class AccountsPayable(models.Model):
    INSTALLMENT_RANGE_CHOICES = [
        ('15', 'A cada 15 dias'),
        ('20', 'A cada 20 dias'),
        ('23', 'A cada 23 dias'),
        ('28', 'A cada 28 dias'),
        ('30', 'A cada 30 dias'),
    ]

    pessoa_id = models.ForeignKey(Person,on_delete=models.SET_NULL, null=True,verbose_name="Pessoa")
    chartOfAccounts = models.ForeignKey(
        ChartOfAccounts,
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name="Plano de Contas"
        )
    # situation = models.ForeignKey(Situation,on_delete=models.SET_NULL, null=True,verbose_name="Situação")
    documentNumber = models.PositiveIntegerField(
        verbose_name="Numero do Documento"
        )
    date_account = models.DateTimeField(
        verbose_name="Data da Conta"
        )
    numberOfInstallments = models.PositiveIntegerField(
        verbose_name="Numero de Parcelas"
        )
    installment_Range = models.CharField(
        max_length=20,
        choices=INSTALLMENT_RANGE_CHOICES,
        verbose_name="Intervalo de Parcelas",
        default='este mês',
        null=True,
        blank=True
    )
    date_init = models.DateTimeField(
        verbose_name="Data de Inicio"
        )
    valueOfInstallments = models.DecimalField(
        decimal_places=2, 
        max_digits=8,
        verbose_name="Valor da Parcelas"
        )
    totalValue = models.DecimalField(
        decimal_places=2, 
        max_digits=8,
        verbose_name="Valor Total"
        )
    peopleWatching = models.TextField(
        verbose_name="Observações para a Pessoas",
        blank=True,
        null=True
        )
    systemWatching = models.TextField(
        verbose_name="Observações para o Sistema",
        blank=True,
        null=True
        )


class PaymentMethod_AccountsPayable(models.Model):

    INTEREST_CHOICES = [
        ('percent', '(%)'),
        ('value', '(R$)'),
    ]
    FINE_CHOICES = [
        ('percent', '(%)'),
        ('value', '(R$)'),
    ]

    conta = models.ForeignKey(AccountsPayable, on_delete=models.SET_NULL, null=True, verbose_name='id_AccountsPayable')
    forma_pagamento = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, verbose_name='Forma de Pagamento')
    expirationDate = models.DateField(max_length=50, verbose_name='Data de Vencimento')
    days = models.DateField(max_length=50, verbose_name='Dias') #dias entre as parcelas
    value = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Valor Pago:')
    
    interestType = models.CharField(
        max_length=10,
        choices=INTEREST_CHOICES,
        verbose_name="Tipo de Juros",
        default='percent',
        null=True,
        blank=True
    )
    interestPercent = models.DecimalField(
        decimal_places=2, 
        max_digits=8, 
        verbose_name='Juros (%)',
        null=True,
        blank=True)
    
    interestValue = models.DecimalField(
        decimal_places=2, 
        max_digits=8, 
        verbose_name='juros R$',
        null=True,
        blank=True)
    
    fineType = models.CharField(
        max_length=10,
        choices=FINE_CHOICES,
        verbose_name="Tipo de Multa",
        default='percent',
        null=True,
        blank=True
    )
    finePercent = models.DecimalField(
        decimal_places=2, 
        max_digits=8, 
        verbose_name='multa (%)',
        null=True,
        blank=True)
    
    fineValue = models.DecimalField(
        decimal_places=2, 
        max_digits=8, 
        verbose_name='multa R$',
        null=True,
        blank=True)


class AccountsReceivable(models.Model):
    pessoa = models.ForeignKey(Person,on_delete=models.SET_NULL, null=True,verbose_name="Pessoa")
    chartOfAccounts = models.ForeignKey(ChartOfAccounts,on_delete=models.SET_NULL, null=True,verbose_name="Plano de Contas")
    documentNumber = models.PositiveIntegerField(verbose_name="Numero do Documento")
    data_da_conta = models.DateTimeField(verbose_name="Data da Conta a Pagar")
    numberOfInstallments = models.PositiveIntegerField(verbose_name="Numero de Parcelas")
    valueOfInstallments = models.DecimalField(decimal_places=2, max_digits=8,verbose_name="Numero de Parcelas")
    totalValue = models.DecimalField(decimal_places=2, max_digits=8,verbose_name="Valor Total")
    peopleWatching = models.TextField(verbose_name="Observações para a Pessoas",blank=True,null=True)
    systemWatching = models.TextField(verbose_name="Observações para o Sistema",blank=True,null=True)


class PaymentMethod_AccountsReceivable(models.Model):
    conta = models.ForeignKey(AccountsReceivable, on_delete=models.SET_NULL, null=True, verbose_name='id_AccountsReceivable')
    forma_pagamento = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, verbose_name='id_forma_de_pagamento')
    expirationDate = models.DateField(max_length=50, verbose_name='Data de Vencimento')
    days = models.DateField(max_length=50, verbose_name='Dias') #dias entre as parcelas
    value = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Valor Pago:')
    interestPercent = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Juros (%)', null=True)
    interestValue = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='juros R$', null=True)
    finePercent = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='multa (%)', null=True)
    fineValue = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='multa R$', null=True)