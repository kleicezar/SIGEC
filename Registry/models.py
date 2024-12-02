from django.db import models

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
    name_foreigner = models.CharField('Nome', max_length=100)
    num_foreigner = models.CharField('Numero do Documento', max_length=100)
    id_address_fk = models.OneToOneField ('Address', on_delete=models.CASCADE, db_column='id_address_fk')

    def __str__(self):
        return self.name_foreigner
    
class LegalPerson(models.Model):
    fantasyName = models.CharField('Nome Fantasia', max_length=100)
    cnpj = models.CharField('CNPJ', max_length=100)
    socialReason = models.CharField('Razão Social', max_length=100)
    StateRegistration = models.CharField('Inscrição Estadual', max_length=100)
    typeOfTaxpayer = models.CharField('Tipo de Contribuinte', max_length=100)
    MunicipalRegistration = models.CharField('Inscrição Municipal', max_length=100)
    suframa = models.CharField('SUFRAMA', max_length=100)
    Responsible = models.CharField('Responsavel', max_length=100)
    id_address_fk = models.OneToOneField ('Address', on_delete=models.CASCADE, db_column='id_address_fk')

    def __str__(self):
        return self.fantasyName
    
class Person(models.Model):
    WorkPhone = models.CharField('WorkPhone', max_length=100)
    PersonalPhone = models.CharField('PersonalPhone', max_length=100)
    isActive = models.BooleanField('isActive', max_length=100)
    site = models.CharField('site', max_length=100,null=True, blank=True)
    salesman = models.CharField('salesman', max_length=100,null=True, blank=True)
    creditLimit = models.DecimalField('creditLimit', max_length=100, decimal_places=2, max_digits=10)
    isClient = models.BooleanField("É Cliente")
    isSupllier = models.BooleanField("É Fornecedor")
    isUser = models.BooleanField("É Usuario do Sistema")
    isEmployee = models.BooleanField("É Funcionario")
    isFormer_employee = models.BooleanField("É Ex-Funcionario")
    isCarrier = models.BooleanField("É Transportadora")
    isDelivery_man = models.BooleanField("É Entregador")
    isTechnician = models.BooleanField("É Tecnico")

    id_FisicPerson_fk = models.OneToOneField ('FisicPerson', on_delete=models.CASCADE,null=True, blank=True, db_column='id_FisicPerson_fk')
    id_LegalPerson_fk = models.OneToOneField ('LegalPerson', on_delete=models.CASCADE,null=True, blank=True, db_column='id_LegalPerson_fk')
    id_ForeignPerson_fk = models.OneToOneField ('ForeignPerson', on_delete=models.CASCADE,null=True, blank=True, db_column='id_ForeignPerson_fk')

    def __str__(self):
        return self.fantasyName
    
# no cadastro de clientes/fornecedores todos os campos is_(alguma função) serao respectivamente
# is_client                 1
# is_supllier               1
# is_user                   0
# is_employee               0
# is_former_employee        0
# is_carrier                0
# is_delivery_man           0
# is_technician             0

# no cadastro de usuarios todos os campos is_(alguma função) serao respectivamente
# is_client                 1
# is_supllier               0
# is_user                   1
# is_employee               1
# is_former_employee        0
# is_carrier                0
# is_delivery_man           0
# is_technician             0

# no cadastro de technicos todos os campos is_(alguma função) serao respectivamente
# is_client                 1
# is_supllier               0
# is_user                   0
# is_employee               1
# is_former_employee        0
# is_carrier                0
# is_delivery_man           0
# is_technician             1

# no cadastro de entregadores todos os campos is_(alguma função) serao respectivamente
# is_client                 1
# is_supllier               0
# is_user                   0
# is_employee               1
# is_former_employee        0
# is_carrier                0
# is_delivery_man           1
# is_technician             0

# no cadastro de transportadoras todos os campos is_(alguma função) serao respectivamente
# is_client                 1
# is_supllier               1
# is_user                   0
# is_employee               0
# is_former_employee        0
# is_carrier                1
# is_delivery_man           0
# is_technician             0

# no cadastro de transportadoras todos os campos is_(alguma função) serao respectivamente
# is_client                 1
# is_supllier               1
# is_user                   0
# is_employee               0
# is_former_employee        0
# is_carrier                1
# is_delivery_man           0
# is_technician             0