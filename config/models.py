from django.db import models
from registry.models import Person
from django.db import transaction
from django.contrib.auth.models import User, Group
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
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

def sync_user_groups_from_supergroups(user_pk):
    """
    Sincroniza os grupos Django de um usuário com base nos SuperGroups aos quais ele pertence.
    """
    try:
        user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        return

    desired_groups = set()
    # Garante que a relação 'super_groups' exista no modelo User
    if hasattr(user, 'super_groups'):
        for supergroup in user.super_groups.all():
            desired_groups.update(supergroup.groups.all())

    current_groups = set(user.groups.all())

    # Adiciona grupos que estão nos MetaGroups mas não diretamente no usuário
    groups_to_add = desired_groups - current_groups
    if groups_to_add:
        user.groups.add(*groups_to_add)

    # Remove grupos que estão no usuário mas não são mais justificados por nenhum SuperGroup
    # ATENÇÃO: Isso significa que os MetaGroups gerenciam completamente os grupos.
    # Se um grupo for atribuído diretamente ao usuário e não estiver em nenhum SuperGroup do usuário,
    # ele será removido por esta lógica.
    groups_to_remove = current_groups - desired_groups
    if groups_to_remove:
        user.groups.remove(*groups_to_remove)

@receiver(m2m_changed, sender=SuperGroup.members.through)
def supergroup_members_changed_handler(sender, instance, action, reverse, pk_set, **kwargs):
    """
    Chamado quando a relação many-to-many SuperGroup.members é alterada.
    (Ex: um usuário é adicionado/removido de um SuperGroup)
    """
    if action in ["post_add", "post_remove", "post_clear"]:
        if reverse:
            # 'instance' é um User, 'pk_set' contém PKs de SuperGroup
            # Ex: user_instance.super_groups.add(supergroup_instance)
            user_instance = instance
            sync_user_groups_from_supergroups(user_instance.pk)
        else:
            # 'instance' é um SuperGroup, 'pk_set' contém PKs de User
            # Ex: supergroup_instance.members.add(user_instance)
            for user_pk in pk_set:
                sync_user_groups_from_supergroups(user_pk)

@receiver(m2m_changed, sender=SuperGroup.groups.through)
def supergroup_definition_changed_handler(sender, instance, action, pk_set, **kwargs):
    """
    Chamado quando a relação many-to-many SuperGroup.groups é alterada.
    (Ex: um Group é adicionado/removido da definição de um SuperGroup)
    'instance' é o SuperGroup que foi modificado.
    """
    if action in ["post_add", "post_remove", "post_clear"]:
        # Todos os membros do SuperGroup modificado precisam ter seus grupos recalculados.
        supergroup = instance
        for user in supergroup.members.all():
            sync_user_groups_from_supergroups(user.pk)