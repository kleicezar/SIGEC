from django.db import models
from django.contrib.auth.models import User
from auditlog.registry import auditlog
from functools import partial
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Address(models.Model):
    cep = models.CharField('CEP', max_length=10)
    road = models.CharField('rua', max_length=100)
    number = models.PositiveIntegerField('numero da casa' )
    neighborhood = models.CharField('Bairro', max_length=100)
    reference = models.CharField('Ponto de Referencia', max_length=100, null=True, blank=True)
    complement = models.CharField('Complemento', max_length=100, null=True, blank=True)
    city = models.CharField('cidade', max_length=100)
    uf = models.CharField('UF', max_length=2)
    country = models.CharField('país', max_length=100)

    def __str__(self):
        return f"{self.road}, {self.number}, {self.city}"

class FisicPerson(models.Model):
    name = models.CharField('Nome', max_length=100)
    cpf = models.CharField('Cadastro de Pessoa Fisica - CPF', max_length=100)
    rg = models.CharField('Registro Geral - RG', max_length=100)
    dateOfBirth = models.CharField('Data de Aniversario', max_length=14)
    id_address_fk = models.OneToOneField ('Address', on_delete=models.CASCADE, db_column='id_address_fk')

    def __str__(self):
        return self.name
    
class ForeignPerson(models.Model):
    name = models.CharField('Nome', max_length=100)
    num_foreigner = models.CharField('Numero do Documento', max_length=100)
    id_address_fk = models.OneToOneField ('Address', on_delete=models.CASCADE, db_column='id_address_fk')

    def __str__(self):
        return self.name

class LegalPerson(models.Model):
    name = models.CharField('Nome Fantasia', max_length=100)
    cnpj = models.CharField('CNPJ', max_length=100)
    socialReason = models.CharField('Razão Social', max_length=100)
    StateRegistration = models.CharField('Inscrição Estadual', max_length=100)
    typeOfTaxpayer = models.CharField('Tipo de Contribuinte', max_length=100)
    MunicipalRegistration = models.CharField('Inscrição Municipal', max_length=100)
    suframa = models.CharField('SUFRAMA', max_length=100)
    Responsible = models.CharField('Responsavel', max_length=100)
    id_address_fk = models.OneToOneField ('Address', on_delete=models.CASCADE, db_column='id_address_fk')

    def __str__(self):
        return self.name
    
class Person(models.Model):
    WorkPhone = models.CharField('WorkPhone', max_length=100)
    PersonalPhone = models.CharField('PersonalPhone', max_length=100)
    isActive = models.BooleanField('isActive', max_length=100)
    site = models.CharField('site', max_length=100,null=True, blank=True) 
    salesman = models.CharField('salesman', max_length=100,null=True, blank=True)
    creditLimit = models.DecimalField('creditLimit', max_length=100, decimal_places=2, max_digits=10,default=0)
    isClient = models.BooleanField("Cliente",null=True, blank=True)
    isSupllier = models.BooleanField("Fornecedor",null=True, blank=True)
    isUser = models.BooleanField("Usuario do Sistema",null=True, blank=True)
    isEmployee = models.BooleanField("Funcionario",null=True, blank=True)
    isSalesman = models.BooleanField("Vendedor",null=True, blank=True)
    isFormer_employee = models.BooleanField("Ex-Funcionario",null=True, blank=True)
    isCarrier = models.BooleanField("Transportadora",null=True, blank=True)
    isDelivery_man = models.BooleanField("Entregador",null=True, blank=True)
    isTechnician = models.BooleanField("Tecnico",null=True, blank=True)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, db_column='person_type')
    object_id = models.PositiveIntegerField() 
    content_object = GenericForeignKey('content_type', 'object_id')

    # id_FisicPerson_fk = models.OneToOneField ('FisicPerson', on_delete=models.SET_NULL,null=True, blank=True, db_column='id_FisicPerson_fk')
    # id_LegalPerson_fk = models.OneToOneField ('LegalPerson', on_delete=models.SET_NULL,null=True, blank=True, db_column='id_LegalPerson_fk')
    # id_ForeignPerson_fk = models.OneToOneField ('ForeignPerson', on_delete=models.SET_NULL,null=True, blank=True, db_column='id_ForeignPerson_fk')
    id_address_fk = models.OneToOneField ('Address', on_delete=models.CASCADE, db_column='id_address_fk')
    id_user_fk = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, db_column='id_user_fk')

    def __str__(self):
        return self.content_object.name

class Credit(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name="pessoa_creditada")
    credit_data = models.DateTimeField(verbose_name='Data do Crédito')
    credit_value = models.IntegerField(default=0)

def custom_field_formatter(field_name, old_value, new_value, nome_amigavel_map):
    """
    Função personalizada para renomear atributos no campo 'changes',
    recebendo o mapa de nomes amigáveis.
    """
    formatted_field_name = nome_amigavel_map.get(field_name, field_name)

    if field_name == 'preco_venda':
        old_value = f"R$ {old_value:.2f}" if old_value is not None else old_value
        new_value = f"R$ {new_value:.2f}" if new_value is not None else new_value
    
    return formatted_field_name, old_value, new_value

auditlog.register(Address)
auditlog.register(FisicPerson)
auditlog.register(ForeignPerson)
auditlog.register(LegalPerson)
auditlog.register(Person)
auditlog.register(Credit)
