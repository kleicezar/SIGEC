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
    

class Address(models.Model):
    road = models.CharField('rua', max_length=100)
    number = models.DecimalField('numero da casa' , decimal_places=2, max_digits=10)
    cep = models.CharField('CEP', max_length=10)
    neighborhood = models.CharField('Bairro', max_length=100)
    reference = models.CharField('Ponto de Referencia', max_length=100)
    complement = models.CharField('Complemento', max_length=100)
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
    id_address_fk = models.ForeignKey ('Address', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
class ForeignPerson(models.Model):
    name_foreigner = models.CharField('Nome', max_length=100)
    num_foreigner = models.CharField('Numero do Documento', max_length=100)
    id_address_fk = models.OneToOneField ('Address', on_delete=models.CASCADE)

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
    id_address_fk = models.OneToOneField ('Address', on_delete=models.CASCADE)

    def __str__(self):
        return self.fantasyName
class Person(models.Model):
    fantasyName = models.CharField('Nome Fantasia', max_length=100)
    cnpj = models.CharField('CNPJ', max_length=100)
    socialReason = models.CharField('Razão Social', max_length=100)
    StateRegistration = models.CharField('Inscrição Estadual', max_length=100)
    typeOfTaxpayer = models.CharField('Tipo de Contribuinte', max_length=100)
    MunicipalRegistration = models.CharField('Inscrição Municipal', max_length=100)
    suframa = models.CharField('SUFRAMA', max_length=100)
    Responsible = models.CharField('Responsavel', max_length=100)
    PersonalPhone = models.CharField('PersonalPhone', max_length=100)
    isActive = models.BooleanField('isActive', max_length=100)
    # WorkPhone = models.CharField('WorkPhone', max_length=100)
    # site = models.CharField('site', max_length=100)
    # salesman = models.CharField('salesman', max_length=100)
    # creditLimit = models.DecimalField('creditLimit', max_length=100, decimal_places=2, max_digits=10)
    # id_FisicPerson_fk = models.OneToOneField ('FisicPerson', on_delete=models.CASCADE,null=True, blank=True)
    # id_LegalPerson_fk = models.OneToOneField ('LegalPerson', on_delete=models.CASCADE,null=True, blank=True)
    # id_ForeignPerson_fk = models.OneToOneField ('ForeignPerson', on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.fantasyName
    

class Product(models.Model):
    description = models.CharField(max_length=255, verbose_name='Descrição')  # descrição
    product_code = models.CharField(max_length=100, verbose_name='Código do Produto')  # código do produto
    barcode = models.CharField(max_length=100, verbose_name='Código de Barras')  # código de barras
    unit_of_measure = models.CharField(max_length=50, verbose_name='Unidade de Medida')  # unidade de medida
    brand = models.CharField(max_length=100, verbose_name='Marca')  # marca
    cost_of_product = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Custo do Produto')  # custo do produto
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço de Venda')  # preço de venda
    ncm = models.CharField(max_length=10, verbose_name='NCM')  # NCM (Nomenclatura Comum do Mercosul)
    csosn = models.CharField(max_length=5, verbose_name='CSOSN')  # CSOSN (Código de Situação da Operação de Substituição Tributária)
    cfop = models.CharField(max_length=7, verbose_name='CFOP')  # CFOP (Código Fiscal de Operações e Prestações)
    current_quantity = models.IntegerField(verbose_name='Quantidade Atual')  # quantidade atual
    maximum_quantity = models.IntegerField(verbose_name='Quantidade Máxima')  # quantidade máxima
    minimum_quantity = models.IntegerField(verbose_name='Quantidade Mínima')  # quantidade mínima
    is_active = models.BooleanField(default=True, verbose_name='Está Ativo')  # está ativo
    supplier = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='Fornecedor')  # fornecedor

    def __str__(self):
        return self.description  # retorna a descrição
class Client(models.Model):
    telefone_pessoal = models.CharField(max_length=15,verbose_name="Telefone Pessoal",blank=True,null=True )
    telefone_trabalho = models.CharField(max_length=15,verbose_name="Telefone de Trabalho",blank=True,null=True )
    site = models.URLField(verbose_name="Site",blank=True,null=True )
    ativo = models.BooleanField(default=True,verbose_name="Está Ativo" )
    limite_credito = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Limite de Crédito",blank=True,null=True )
    endereco = models.ForeignKey(Address,on_delete=models.CASCADE,null=True,blank=True,verbose_name="Endereço" )
    pessoa_fisica = models.OneToOneField(FisicPerson,on_delete=models.CASCADE,verbose_name="Pessoa Física")

    def __str__(self):
        return f"Cliente {self.id} - {self.pessoa_fisica}"
    



class Venda(models.Model):
    pessoa = models.ForeignKey(Client,on_delete=models.CASCADE,verbose_name="Pessoa",related_name="vendas")
    data_da_venda = models.DateTimeField(verbose_name="Data da Venda" )
    observacao_pessoas = models.TextField(verbose_name="Observações sobre as Pessoas",blank=True,null=True)
    observacao_sistema = models.TextField(verbose_name="Observações do Sistema",blank=True,null=True)
    situacao = models.ForeignKey(Situation,on_delete=models.CASCADE,verbose_name="Situação",related_name="vendas")
    is_active = models.BooleanField(default=True, verbose_name='Está Ativo')  # está ativo
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total", blank=True, null=True)

    def __str__(self):
        return f"Venda {self.id} - {self.pessoa}"
    

        

class VendaItem(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, verbose_name="Venda")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produto")
    quantidade = models.PositiveIntegerField(verbose_name="Quantidade do Produto")
    preco_unitario = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Preço Unitário")

    # Calcula o total automaticamente ao salvar a instância
    def save(self, *args, **kwargs):
        self.total = self.quantidade * self.preco_unitario  # Calcula o total
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.description} - {self.quantidade} unidades"

class Purchase(models.Model):
    datePurchase = models.CharField(max_length=10, verbose_name='Data da Compra')
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total", blank=True, null=True)
    id_fornecedor_fk = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, verbose_name="Fornecedor")
    id_Situation_fk = models.ForeignKey(Situation, on_delete=models.SET_NULL, null=True, verbose_name="Situação")


    def calcular_total(self):
        self.total = sum(item.subtotal() for item in self.itens.all())
        self.save()

    def __str__(self):
        return f"Compra {self.id} por {self.usuario.username}"
    
class PurchaseItem(models.Model):
    compra = models.ForeignKey(Venda, on_delete=models.SET_NULL, null=True, verbose_name="Venda")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Produto")
    quantidade = models.PositiveIntegerField(verbose_name="Quantidade do Produto")
    preco_unitario = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Preço Unitário")

    # Calcula o total automaticamente ao salvar a instância
    def save(self, *args, **kwargs):
        self.total = self.quantidade * self.preco_unitario  # Calcula o total
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.description} - {self.quantidade} unidades"

class PaymentMethod_Purchase(models.Model):
    compra = models.ForeignKey(Purchase, on_delete=models.SET_NULL, null=True, verbose_name='id_compra')
    forma_pagamento = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, verbose_name='id_forma_de_pagamento')
    expirationDate = models.CharField(max_length=50, verbose_name='Data de Vencimento')
    valor = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Valor Pago:')