from django.db import models
from Registry.models import Person
from Sale.models import Venda
from Service.models import VendaService
from purchase.models import Compra
from config.models import ChartOfAccounts, PaymentMethod, Situation
from django.utils import timezone
from django.contrib.auth.models import User 

class Accounts(models.Model):
    INSTALLMENT_RANGE_CHOICES = [
        ('15', 'A cada 15 dias'),
        ('20', 'A cada 20 dias'),
        ('23', 'A cada 23 dias'),
        ('28', 'A cada 28 dias'),
        ('30', 'A cada 30 dias'),
    ]

    description = models.TextField(
        verbose_name='Descrição da Conta',
        null=False,
        blank=False 
        )
    pessoa_id = models.ForeignKey(Person,on_delete=models.SET_NULL, null=True,verbose_name="Pessoa")
    chartOfAccounts = models.ForeignKey(ChartOfAccounts, on_delete=models.SET_NULL, null=True, verbose_name="Plano de Contas")
    documentNumber = models.PositiveIntegerField(verbose_name="Numero do Documento")
    date_account = models.DateField(
        verbose_name="Data da Conta"
        )
    numberOfInstallments = models.PositiveIntegerField(verbose_name="Numero de Parcelas")
    installment_Range = models.CharField(
        max_length=20,
        choices=INSTALLMENT_RANGE_CHOICES,
        verbose_name="Intervalo de Parcelas",
        default='este mês',
        null=True,
        blank=True
    )
    date_init = models.DateField(verbose_name="Data de Inicio")
    totalValue = models.DecimalField(
        decimal_places=2, 
        max_digits=10,
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
    is_active = models.BooleanField(default=False,verbose_name='Está Ativo')

class PaymentMethod_Accounts(models.Model):
    INTEREST_CHOICES = [
        ('percent', '(%)'),
        ('value', '(R$)'),
    ]
    FINE_CHOICES = [
        ('percent', '(%)'),
        ('value', '(R$)'),
    ]
    conta = models.ForeignKey(
        Accounts,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='id_Accounts'
    )
    venda = models.ForeignKey(Venda,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='id_venda'
    )
  
    compra = models.ForeignKey(Compra,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='id_compra'
    )
    ordem_servico = models.ForeignKey(VendaService,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='id_vendaservico'
    )
    forma_pagamento = models.ForeignKey(PaymentMethod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Forma de Pagamento'
    )
    expirationDate = models.DateField(
        max_length=50,
        verbose_name='Data de Vencimento',
        blank=True
    )
    days = models.IntegerField(             #dias entre as parcelas
        verbose_name='Dias',
        blank=True
    ) 
    value_old = models.DecimalField(        #valor original sem alterações
        decimal_places=2,   
        max_digits=8,
        verbose_name='Valor da Conta:',
        default = 0
    )
    value = models.DecimalField(decimal_places=2,
        max_digits=8,
        verbose_name='Valor Pago:',
        blank=True
    )  
    interestType = models.CharField(
        max_length=10, 
        choices=INTEREST_CHOICES,
        verbose_name="Tipo de Juros",
        default='value',
        null=True,
        blank=True
    )
    interest = models.DecimalField(
        decimal_places=2, 
        max_digits=8, 
        verbose_name='juros',
        null=True,
        blank=True
    )
    fineType = models.CharField(
        max_length=10,
        choices=FINE_CHOICES,
        verbose_name="Tipo de Multa",
        default='value',
        null=True,
        blank=True
    )
    fine = models.DecimalField(
        decimal_places=2, 
        max_digits=8, 
        verbose_name='Multa R$',
        null=True,
        blank=True
    )
    acc = models.BooleanField(
        verbose_name='Tipo de Conta'
    )

    activeCredit = models.BooleanField(
    default=False,
    blank=True  
)


class Tax_PaymentMethod_Accounts(models.Model):
    compra = models.ForeignKey(Compra,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='id_compra'
    )
    forma_pagamento = models.ForeignKey(PaymentMethod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Forma de Pagamento'
    )
    expirationDate = models.DateField(
        max_length=50,
        verbose_name='Data de Vencimento',
        blank=True
    )
    days = models.IntegerField(             #dias entre as parcelas
        verbose_name='Dias',
        blank=True
    )
    value = models.DecimalField(decimal_places=2,
        max_digits=8,
        verbose_name='Valor Pago:',
        blank=True
    )
    acc = models.BooleanField(
        verbose_name='Tipo de Conta'
    )
    activeCredit = models.BooleanField(
        default=False,
        blank=True
    )

class Freight_PaymentMethod_Accounts(models.Model):
    compra = models.ForeignKey(Compra,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='id_compra'
    )
    forma_pagamento = models.ForeignKey(PaymentMethod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Forma de Pagamento'
    )
    expirationDate = models.DateField(
        max_length=50,
        verbose_name='Data de Vencimento',
        blank=True
    )
    days = models.IntegerField(             #dias entre as parcelas
        verbose_name='Dias',
        blank=True
    )
    value = models.DecimalField(decimal_places=2,
        max_digits=8,
        verbose_name='Valor Pago:',
        blank=True
    )
    acc = models.BooleanField(
        verbose_name='Tipo de Conta'
    )
    activeCredit = models.BooleanField(
        default=False,
        blank=True
    )
class Romaneio_PaymentMethod_Accounts(models.Model):
    compra = models.ForeignKey(Compra,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='id_compra'
    )
    forma_pagamento = models.ForeignKey(PaymentMethod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Forma de Pagamento'
    )
    expirationDate = models.DateField(
        max_length=50,
        verbose_name='Data de Vencimento',
        blank=True
    )
    days = models.IntegerField(             #dias entre as parcelas
        verbose_name='Dias',
        blank=True
    )
    value = models.DecimalField(decimal_places=2,
        max_digits=8,
        verbose_name='Valor Pago:',
        blank=True
    )
    acc = models.BooleanField(
        verbose_name='Tipo de Conta'
    )
    activeCredit = models.BooleanField(
        default=False,
        blank=True
    )
    # interestPercent = models.DecimalField(
    #     decimal_places=2, 
    #     max_digits=8, 
    #     verbose_name='Juros (%)',
    #     null=True,
    #     blank=True
    # )
    # interestValue = models.DecimalField(
    #     decimal_places=2, 
    #     max_digits=8, 
    #     verbose_name='juros R$',
    #     null=True,
    #     blank=True
    # )
    # finePercent = models.DecimalField(
    #     decimal_places=2, 
    #     max_digits=8, 
    #     verbose_name='multa (%)',
    #     null=True,
    #     blank=True
    # )
    # fineValue = models.DecimalField(
    #     decimal_places=2, 
    #     max_digits=8, 
    #     verbose_name='multa R$',
    #     null=True,
    #     blank=True
    # )


class CaixaDiario(models.Model): #abertura de caixa
    usuario_responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    data = models.DateField(default=timezone.now)  # Um registro por dia
    saldo_inicial = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    saldo_final = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Caixa {self.data} - Saldo Final: R${self.saldo_final:.2f}"

class CashMovement(models.Model):  # transações do caixa diario
    # TIPO_MOVIMENTACAO = [
    #     ('entrada', 'Entrada'),
    #     ('saida', 'Saída'),
    # ]

    cash = models.ForeignKey(
        CaixaDiario,
        null=True,
        on_delete=models.SET_NULL, 
        related_name="movimentacoes"
    )
    accounts_in_cash = models.ForeignKey(
        PaymentMethod_Accounts,
        null=True,
        on_delete=models.SET_NULL, 
        # related_name="conta",
        related_name='cash_movements'
    )
    # tipo_movimentacao = models.CharField(max_length=10, choices=TIPO_MOVIMENTACAO) 
    #FIXME a movimentação de caixa se deve pelo campo acc presente em contas
    # descricao = models.CharField(max_length=255)
    #FIXME a descriçao de caixa se deve pelo campo description presente em contas
    forma_pagamento = models.ForeignKey(
        PaymentMethod,
        null=True,
        on_delete=models.SET_NULL,
        max_length=15, 
    )
    categoria = models.CharField(max_length=100) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.accounts_in_cash.description} - R${self.accounts_in_cash.totalValue:.2f}"

class FechamentoCaixa(models.Model):  # fechamento do caixa
    caixa = models.OneToOneField(CaixaDiario, on_delete=models.CASCADE)
    observacoes = models.TextField(blank=True, null=True)
    closed_in = models.DateTimeField(auto_now_add=True, verbose_name='fechado_em')

    def __str__(self):
        return f"Fechamento {self.caixa.data} - Responsável: {self.caixa.usuario_responsavel}"

