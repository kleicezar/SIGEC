from django.db import models
from registry.models import Person
from django.db import transaction
from django.contrib.auth.models import User, Group
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Permission

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
    name_Situation = models.CharField('Nome da Situação', max_length=50)
    is_Active = models.BooleanField('ativo',default=True)

    def __str__(self):
        return self.name_Situation
    
class Position(models.Model): #desativado
    name_position = models.CharField('Nome do Cargo', max_length=25)
    is_Active = models.BooleanField('ativo',default=True)

    def __str__(self):
        return self.name_position
 
class service(models.Model):
    name_service = models.CharField('Nome do Serviço',max_length=500)
    is_Active = models.BooleanField('ativo',default=True)
    value_service = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor do Serviço", blank=True, null=True)
    
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
