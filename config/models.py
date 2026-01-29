from django.db import models
from registry.models import Person
from django.db import transaction
from django.contrib.auth.models import User, Group
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Permission
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField

class Bank(models.Model):
    bank_name = models.CharField(verbose_name='Nome do Banco', max_length=250)
    agencia =  models.CharField(verbose_name='Agencia do Banco', max_length=250, null=True, blank=True)
    conta =  models.CharField(verbose_name='Conta', max_length=250, null=True, blank=True)
    is_Active = models.BooleanField('ativo', default=True)
    value_in_bank = models.IntegerField(verbose_name='valor arrecadado no banco',default=0)
    
    def __str__(self):
        return self.bank_name

class PaymentMethod(models.Model):
    # CONSIDERINCASH = [
    #     ('entrada', 'Entrada'),
    #     ('saida', 'Saída'),

    # ]
    name_paymentMethod = models.CharField('Nome da Forma de Pagamento', max_length=50)
    creditPermission = models.BooleanField('creditPermission',default=False)
    is_Active = models.BooleanField('ativo',default=True) 
    considerInCash = models.BooleanField('considerar em caixa', default=False, blank=True, null=True) 
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, verbose_name='Banco que recebe a Forma de Pagamento')
    # considerInCash = models.CharField('considerar em caixa',choices= CONSIDERINCASH, default=False, blank=True, null=True, max_length=50)
    is_Active = models.BooleanField('ativo', default=True) 

    def __str__(self):
        return self.name_paymentMethod

class ChartOfAccounts(models.Model): 
    NatureOfTheAccount = [
            ('E', 'Entrada'),
            ('S', 'Saída'),
        ]

    code = models.CharField(max_length=20, unique=True, blank=True, verbose_name='Codigo de Conta')
    name_ChartOfAccounts = models.CharField('Nome do Plano de Contas', max_length=50)
    father = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='filhos', #onde os filhos vão receber o id do pai 
        verbose_name='Referente a'
    )
    natureOfTheAccount =  models.CharField(
        max_length=1,
        choices=NatureOfTheAccount,
        default='E',
        verbose_name='Natureza da Conta'
    )
    is_Active = models.BooleanField('ativo',default=True)
    historico = AuditlogHistoryField()

    def save(self, *args, **kwargs):
        if not self.code:
            with transaction.atomic():  # evita conflito em ambiente concorrente
                #se o plano de contas ja estiver uma linha pai 
                if self.father:
                    lastson = ChartOfAccounts.objects.filter(father=self.father).order_by('-code').first()
                    if lastson:
                        #cria uma lista que divide o plano de contas em subniveis
                        newlastson = lastson.code.split(".")
                        # pega o ultimo item da lista e incrementa adicionando 1 ao valor do item da lista
                        # deixando ele sempre com 3 digitos
                        newlastson[-1] = str(int(newlastson[-1]) + 1).zfill(3)
                        self.code = '.'.join(newlastson)
                    else: # se nao tiver nenhum filho é criado o primeiro
                        self.code = f'{self.father.code}.001'
                else: # se for a raiz do plano de contas
                    roots = ChartOfAccounts.objects.filter(father__isnull=True)
                    if roots.exists():
                        # pega o ultimo codigo do plano de contas e adiciona '1' para o novo plano de contas
                        last_code = roots.order_by('-code').first().code
                        self.code = str(int(last_code) + 1)
                    else:
                        self.code = '1'

        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.code} - {self.name_ChartOfAccounts}'
    
class Situation(models.Model):
    # CLOSURE_LEVEL_OPTIONS = [
    #     ('Situação Aberta','Situação Aberta'),
    #     ('Situação Concluída','Situação Concluída'),
    #     ('Trancamento Parcial','Trancamento Parcial'),
    #     ('Trancamento Total','Trancamento Total')
    # ]
    # closure_level = models.CharField(
    #     max_length=50,
    #     choices=CLOSURE_LEVEL_OPTIONS,
    #     default='Situação Concluída'
    # )
    # salePerms = models.CharField('Permissoes ' \
    # '', max_length=50)
    # purchasePerms = models.CharField('Nome da Situação', max_length=50)
    # servicePerms = models.CharField('Nome da Situação', max_length=50)

    # salePerms = models.CharField('Nome da Situação', max_length=50)
    
    name_Situation = models.CharField('Nome da Situação', max_length=50)
 
    V_estagio_inicial = models.BooleanField('estagio inicial para venda',null=True,blank=True)
    V_movement_storage  = models.BooleanField('Movimentar Estoque',null=True,blank=True)
    V_movement_accounts = models.BooleanField('Movimentar Financeiro',null=True,blank=True)

    OS_estagio_inicial = models.BooleanField('estagio inicial para ordem de servico',null=True,blank=True)
    OS_movement_storage  = models.BooleanField('Movimentar Estoque',null=True,blank=True)
    OS_movement_accounts = models.BooleanField('Movimentar Financeiro',null=True,blank=True)
    
    C_estagio_inicial = models.BooleanField('estagio inicial para compras',null=True,blank=True)
    C_movement_storage  = models.BooleanField('Movimentar Estoque',null=True,blank=True)
    C_movement_accounts = models.BooleanField('Movimentar Financeiro',null=True,blank=True)
    
    ACC_estagio_inicial = models.BooleanField('estagio inicial para contas',null=True,blank=True)
    ACC_movement_storage  = models.BooleanField('Movimentar Estoque',null=True,blank=True)
    ACC_movement_accounts = models.BooleanField('Movimentar Financeiro',null=True,blank=True)

    V_pessoa = models.BooleanField('Nome do Cliente') 
    V_data_da_venda = models.BooleanField('Data da Venda') 
    V_total_value = models.BooleanField('Valor Total')
    V_discount_total = models.BooleanField('Desconto Total')
    V_value_apply_credit = models.BooleanField('Credito')
    V_product = models.BooleanField('Produto') 
    V_quantidade = models.BooleanField('Quantidade') 
    V_preco_unitario = models.BooleanField('Preco Unitario') 
    V_discount = models.BooleanField('Desconto') 
    V_price_total = models.BooleanField('Total do Produto') 
    V_status = models.BooleanField('Status')
    V_apply_credit = models.BooleanField('Aplicar Credito')
    V_product_total = models.BooleanField('Quantidade Total de Produtos') 
    V_forma_pagamento = models.BooleanField('Forma de Pagamento') 
    V_expirationDate = models.BooleanField('Data de Vencimento') 
    V_valor = models.BooleanField('Valor da Parcela')
    V_observacao_pessoas = models.BooleanField('Observacao visivel para clientes') 
    V_observacao_sistema = models.BooleanField('Observacao do Sistema')

    OS_apply_credit = models.BooleanField('Aplicar Credito') 
    OS_pessoa = models.BooleanField('Nome do Cliente')
    OS_data_da_venda = models.BooleanField('Data da Ordem de Serviço') 
    OS_observacao_pessoas = models.BooleanField('Observacao visivel para clientes')
    OS_observacao_sistema = models.BooleanField('Observacao do Sistema')
    OS_total_value = models.BooleanField("Valor Total da Ordem de Serviço")
    OS_product_total = models.BooleanField("Total de Produtos")
    OS_discount_total = models.BooleanField("Total de Descontos de Produtos")
    OS_value_apply_credit = models.BooleanField('Valor do Crédito Aplicado')
    OS_service_total = models.BooleanField("Total de Servicos")
    OS_discount_total_service = models.BooleanField("Total de Descontos")
    OS_total_value_service = models.BooleanField("Valor Total do Serviço")
    OS_preco = models.BooleanField("Preço Unitário")
    OS_discount = models.BooleanField("Desconto")
    OS_technician = models.BooleanField('Técnico Responsavel')
    OS_expirationDate = models.BooleanField('Data de Vencimento')
    OS_valor = models.BooleanField('Valor Pago:')
    OS_quantidade = models.BooleanField("Quantidade do Produto")
    OS_preco_unitario = models.BooleanField("Preço Unitário")
    OS_discount = models.BooleanField("Desconto(%)")
    OS_price_total = models.BooleanField("Valor Total")
    OS_status = models.BooleanField('Pendente')

    # C_

    C_fornecedor = models.BooleanField('Nome do Fornecedor')  
    C_description = models.BooleanField('Descrição')  
    C_product_code = models.BooleanField('Código do Produto')
    C_barcode = models.BooleanField('Código de Barras')
    C_unit_of_measure = models.BooleanField('Unidade de Medida')
    C_brand = models.BooleanField('Marca')
    C_cost_of_product = models.BooleanField('Custo do Produto') 
    C_selling_price = models.BooleanField('Preço de Venda')
    C_ncm = models.BooleanField('NCM')  # NCM (Nomenclatura Comum do Mercosul
    C_csosn = models.BooleanField('CSOSN')  # CSOSN (Código de Situação da Operação de Substituição Tributária
    C_cfop = models.BooleanField('CFOP')  # CFOP (Código Fiscal de Operações e Prestações
    C_current_quantity = models.BooleanField('Quantidade Atual')
    C_maximum_quantity = models.BooleanField('Quantidade Máxima')
    C_minimum_quantity = models.BooleanField('Quantidade Mínima')
    C_data_da_compra = models.BooleanField('Data da Compra')
    C_total_value = models.BooleanField("Total")
    C_product_total =  models.BooleanField("Total de Produtos")
    C_discount_total = models.BooleanField("Total de Descontos")
    C_observation_product =  models.BooleanField('Observação sobre Produtos')
    C_freight_type = models.BooleanField('Tipo de Frete')
    C_valueFreight = models.BooleanField('Valor do Frete')
    C_numberOfInstallmentsFreight = models.BooleanField('Número de Parcelas')
    C_observation_freight = models.BooleanField('Observação sobre Frete')
    C_valueTax =  models.BooleanField('Valor do Imposto')
    C_numberOfInstallmentsTax = models.BooleanField('Número de Parcelas')
    C_observation_tax = models.BooleanField('Observação sobre Imposto')
    C_valuePickingList = models.BooleanField('Valor do RMN')
    C_numberOfInstallmentsRMN = models.BooleanField('Número de Parcelas')
    C_observation_picking_list = models.BooleanField('Observação sobre Romaneio')
    C_quantidade = models.BooleanField("Quantidade do Produto")
    C_preco_unitario = models.BooleanField("Preço Unitário")
    C_discount = models.BooleanField("Desconto") # porcentagem aplicada no produto
    C_price_total = models.BooleanField("Valor Total") # valor total do produto
    
    ACC_description = models.BooleanField('Descrição da Conta')
    ACC_pessoa_id = models.BooleanField("Pessoa")
    ACC_chartOfAccounts = models.BooleanField("Plano de Contas")
    ACC_documentNumber = models.BooleanField("Numero do Documento")
    ACC_date_account = models.BooleanField("Data da Conta")            
    ACC_numberOfInstallments = models.BooleanField("Numero de Parcelas")
    ACC_installment_Range = models.BooleanField("Intervalo de Parcelas")
    ACC_date_init = models.BooleanField("Data de Inicio")
    ACC_totalValue = models.BooleanField("Valor Total")
    ACC_peopleWatching = models.BooleanField("Observações para a Pessoas")
    ACC_systemWatching = models.BooleanField("Observações para o Sistema")
    ACC_plannedAccount = models.BooleanField('Conta Prevista')
    ACC_venda = models.BooleanField('id_venda')
    ACC_compra = models.BooleanField('id_compra')
    ACC_ordem_servico = models.BooleanField('id_vendaservico')
    ACC_forma_pagamento = models.BooleanField('Forma de Pagamento')
    ACC_expirationDate = models.BooleanField('Data de Vencimento')
    ACC_days = models.BooleanField('Dias') #dias entre as parcelas  
    ACC_value_old = models.BooleanField('Valor da Conta') #valor original sem alterações
    ACC_value = models.BooleanField('Valor Pago')  
    ACC_interestType = models.BooleanField("Tipo de Juros")
    ACC_interest = models.BooleanField('juros')
    ACC_fineType = models.BooleanField("Tipo de Multa")
    ACC_fine = models.BooleanField('Multa R$')
    ACC_acc = models.BooleanField('Tipo de Conta')
    ACC_activeCredit = models.BooleanField("Usar Credito")
    ACC_paymentPurpose = models.BooleanField("Próposito do Pagamento")

    is_Active = models.BooleanField('ativo',default=True)
    historico = AuditlogHistoryField()

    # def save(self, *args, **kwargs):
    #     if not self.code:
    #         with transaction.atomic():  # evita conflito em ambiente concorrente
    #             #se o plano de contas ja estiver uma linha pai 
    #             if self.father:
    #                 lastson = ChartOfAccounts.objects.filter(father=self.father).order_by('-code').first()
    #                 if lastson:
    #                     #cria uma lista que divide o plano de contas em subniveis
    #                     newlastson = lastson.code.split(".")
    #                     # pega o ultimo item da lista e incrementa adicionando 1 ao valor do item da lista
    #                     # deixando ele sempre com 3 digitos
    #                     newlastson[-1] = str(int(newlastson[-1]) + 1).zfill(3)
    #                     self.code = '.'.join(newlastson)
    #                 else: # se nao tiver nenhum filho é criado o primeiro
    #                     self.code = f'{self.father.code}.001'
    #             else: # se for a raiz do plano de contas
    #                 roots = ChartOfAccounts.objects.filter(father__isnull=True)
    #                 if roots.exists():
    #                     # pega o ultimo codigo do plano de contas e adiciona '1' para o novo plano de contas
    #                     last_code = roots.order_by('-code').first().code
    #                     self.code = str(int(last_code) + 1)
    #                 else:
    #                     self.code = '1'

    #     super().save(*args, **kwargs)



    def __str__(self):
        return self.name_Situation

class Situation_new(models.Model):
    name_Situation = models.CharField('Nome da Situação', max_length=100)
    # salePerms = models.CharField('Permissoes de Venda ', max_length=300)
    # purchasePerms = models.CharField('Permissoes de Compras', max_length=300)
    # servicePerms = models.CharField('Permissoes de Ordens de Serviço', max_length=300)
    is_Active = models.BooleanField('ativo',default=True)
    historico = AuditlogHistoryField()
    def __str__(self):
        return self.name_Situation
    
class Position(models.Model): #desativado
    name_position = models.CharField('Nome do Cargo', max_length=25)
    is_Active = models.BooleanField('ativo',default=True)
    
    def __str__(self):
        return self.name_position
 
class Service(models.Model):
    name_service = models.CharField('Nome do Serviço',max_length=500)
    is_Active = models.BooleanField('ativo',default=True)
    value_service = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor do Serviço", blank=True, null=True)
    historico = AuditlogHistoryField()

    def __str__(self):
        return self.name_service 

class SuperGroup(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='nome do super grupo'
    )
    # Grupos que este SuperGroup contém
    groups = models.ManyToManyField(
        Group,
        blank=True,
        verbose_name='grupos contidos',
        help_text='Os grupos que este super grupo engloba.'
    )
    # Usuários que pertencem a este SuperGroup
    members = models.ManyToManyField(
        User,
        blank=True,
        verbose_name='membros',
        help_text='Usuários que pertencem a este super grupo.',
        related_name='super_groups'  # Importante para evitar conflito com user.groups
    )
    historico = AuditlogHistoryField()
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'super grupo'
        verbose_name_plural = 'super grupos'

class GroupSetBackend(ModelBackend):
    def get_group_permissions(self, user_obj, obj=None):
        if not user_obj.is_active or user_obj.is_anonymous:
            return set()

        permissions = set()

        # Permissões dos grupos normais
        permissions.update(super().get_group_permissions(user_obj, obj))

        # Permissões dos grupos agrupados (GroupSet)
        group_sets = user_obj.groupset_set.all()
        for group_set in group_sets:
            for group in group_set.groups.all():
                perms = group.permissions.values_list(
                    "content_type__app_label", "codename"
                ).order_by()
                permissions.update(
                    ["%s.%s" % (ct, name) for ct, name in perms]
                )

        return permissions

class Log(models.Model):
    """
    user: usuario presente na requisição " request.user "

    date: data atual do log " datetime.now().strftime("%d/%m/%Y as %H:%M:%S") "

    type: tipo de modulo ou ação usada numerado entre 1 a 13
    
    01 : pessoa 

    02 : produtos 

    03 : compras 

    04 : vendas 

    05 : ordem de serviço 

    06 : contas a pagar 

    07 : contas a receber 

    08 : formas de pagamento 

    09 : situação 

    10 : plano de contas 

    11 : serviços 

    12 : Login 

    13 : logout

    action: conjunto de caracteres descrevendo o que foi feito no log
    """
    CHOICES_LOG_TYPE = {
        ('01','pessoa'),
        ('02','produtos'),
        ('03','compras'),
        ('04','vendas'),
        ('05','ordem de serviço'),
        ('06','contas a pagar'),
        ('07','contas a receber'),
        ('08','formas de pagamento'),
        ('09','situação'),
        ('10','plano de contas'),
        ('11','serviços'),
        ('12','Login'),
        ('13','logout'),

    }
    CHOICES_LOG = {
        ('e','login'),
        ('s','logout'),
        ('c','create'),
        ('r','read'),
        ('u','update'),
        ('d','delete')
    }

    user = models.ForeignKey(User, verbose_name='Usuario', on_delete=models.CASCADE)
    date = models.DateTimeField( auto_created=True, verbose_name="data e hora do log")
    # action = models.CharField(max_length=255, null=False, blank=False, verbose_name="Ação feita pelo usuario")

    type = models.CharField(max_length=2, choices=CHOICES_LOG_TYPE, verbose_name='tipo de transação')
    action = models.CharField(max_length=1, choices=CHOICES_LOG, verbose_name='tipo de transação')

class Info_logs(models.Model):
    """
    log_principal: id do log principal

    info_old: informação antiga cadastrada

    info_now: Informação nova para update

    field: nome do campo que foi modificado
    """

    log_principal = models.ForeignKey(Log, verbose_name='log principal', on_delete=models.CASCADE)

    info_old = models.CharField(max_length=255, null=False, blank=False, verbose_name="Informação antiga")
    info_now = models.CharField(max_length=255, null=True, blank=False, verbose_name="Informação atual")
    field = models.CharField(max_length=255, null=True, blank=False, verbose_name="nome do campo")
   


auditlog.register(PaymentMethod)
auditlog.register(ChartOfAccounts)
auditlog.register(Situation)
auditlog.register(Service)
auditlog.register(SuperGroup)