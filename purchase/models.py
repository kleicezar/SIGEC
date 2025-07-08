from django.db import models
from registry.models import Person
from config.models import Situation, PaymentMethod
from auditlog.registry import auditlog

class Product(models.Model):
    description = models.CharField(max_length=255, verbose_name='Descrição')  # descrição
    product_code = models.CharField(max_length=100, verbose_name='Código do Produto')  # código do produto
    barcode = models.CharField(max_length=100, verbose_name='Código de Barras')  # código de barras
    unit_of_measure = models.CharField(max_length=50, verbose_name='Unidade de Medida')  # unidade de medida
    brand = models.CharField(max_length=100, verbose_name='Marca')                      # marca
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
    # product = models.ForeignKey(ProductGroup, on_delete=models.SET_NULL, verbose_name='Grupo de Produtos')


    def __str__(self):
        return self.description  # retorna a descrição

class Compra(models.Model):
    data_da_compra = models.DateTimeField(verbose_name='Data da Compra')
    total_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total", blank=True, null=True)
    product_total =  models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Total de Produtos")
    discount_total = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Total de Descontos")
    fornecedor = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, verbose_name="Fornecedor")
    situacao = models.ForeignKey(Situation, on_delete=models.SET_NULL, null=True, verbose_name="Situação")
    is_active = models.BooleanField(default=True, verbose_name='Está Ativo')  # está ativo

    observation_product =  models.TextField(verbose_name='Observação sobre Produtos',null=True,blank=True)

    rmnExists = models.BooleanField(default=False,verbose_name='Romaneio')
    freightExists = models.BooleanField(default=False,verbose_name='Frete')
    taxExists = models.BooleanField(default=False,verbose_name='Imposto')

    def __str__(self):
        ...
        # return f"Compra {self.id} por }"
class Frete(models.Model):
    FREIGHT_CHOICES = [
        ('FOB','FOB'),
        ('CIF','CIF')
    ]
    compra = models.ForeignKey(Compra,on_delete=models.SET_NULL, null=True, blank=True)
    freight_type = models.CharField(choices=FREIGHT_CHOICES,max_length=3,verbose_name='Tipo de Frete',null=True, blank=True)
    valueFreight = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Valor do Frete')
    numberOfInstallmentsFreight = models.IntegerField(verbose_name='Número de Parcelas')
    observation_freight = models.TextField(verbose_name='Observação sobre Frete',null=True,blank=True)
class Tax(models.Model):
    compra = models.ForeignKey(Compra,on_delete=models.SET_NULL, null=True, blank=True)
    valueTax =  models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Valor do Imposto')
    numberOfInstallmentsTax = models.IntegerField(verbose_name='Número de Parcelas')
    observation_tax = models.TextField(verbose_name='Observação sobre Imposto',null=True,blank=True)
class PickingList(models.Model):
    compra = models.ForeignKey(Compra,on_delete=models.SET_NULL, null=True, blank=True)
    valuePickingList = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Valor do RMN')
    numberOfInstallmentsRMN = models.IntegerField(verbose_name='Número de Parcelas')
    observation_picking_list = models.TextField(verbose_name='Observação sobre Romaneio',null=True,blank=True)

class CompraItem(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.SET_NULL, null=True, verbose_name="Compra")
    produto = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Produto")
    quantidade = models.PositiveIntegerField(verbose_name="Quantidade do Produto")
    preco_unitario = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Preço Unitário")
    discount = models.DecimalField(max_digits=5, decimal_places=2) # porcentagem aplicada no produto
    price_total = models.DecimalField(max_digits=10, decimal_places=2) # valor total do produto
    status = models.CharField(max_length=50,default='Pendente')

    # Calcula o total automaticamente ao salvar a instância
    def save(self, *args, **kwargs):
        self.total = self.quantidade * self.preco_unitario  # Calcula o total
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.produto.description} - {self.quantidade} unidades"

class NomeGrupoPessoas(models.Model):
    name_group = models.CharField(max_length=255, verbose_name='Nome do Grupo')

class NomeGrupoPessoasQuantidade(models.Model):
    group = models.ForeignKey(NomeGrupoPessoas, on_delete=models.CASCADE, verbose_name='NomeGrupoPessoasQuantidades')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='Pessoa')

class ProductGroup(models.Model):
    name_group = models.CharField(max_length=255, verbose_name='Nome do Grupo')

class AllProductGroup(models.Model):
    group_name = models.ForeignKey(ProductGroup, on_delete=models.CASCADE, verbose_name='NomeGrupoPessoasQuantidades')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Produtos')
    customized_price = models.IntegerField( verbose_name='Preço Customizado')

class ProductPrice(models.Model):
    person_group = models.ForeignKey(NomeGrupoPessoasQuantidade, on_delete=models.SET_NULL, null=True, verbose_name='Pessoa')
    product_group = models.ForeignKey(AllProductGroup, on_delete=models.CASCADE, verbose_name='Produtos')


#     RESTO DE CODIGO PARA USO FUTURO (DELETAREI EM BREVE)
#     # person = models.ForeignKey(Person, on_delete=models.SET_NULL, verbose_name='Pessoa')
#     product = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='Produtos')
#     customized_price = models.CharField(max_length=255, verbose_name='Preço Customizado')

# Como fazer o cálculo para análise da curva

# No caso da elaboração da Curva ABC, tanto planilhas de excel quanto softwares ERP podem elaborá-la automaticamente a partir do envio dos dados.

# Grande parte das empresas já utilizam sistemas de informação integrados (ERP) em seu dia a dia, o que facilita a organização destas informações e assertividade nos dados. Os sistemas ERP têm a inteligência de ranquear todos os produtos da empresa (conforme volume de vendas) e fornecer dados para que o gestor compreenda quais são mais importantes e têm mais valor.

# Já em relação às planilhas no Excel, essa é uma ferramenta menos completa porém acessível para quase todas as empresas. No excel, por exemplo, é possível elaborar uma Curva ABC listando os produtos e as informações de cada um. Com a planilha em mãos, é necessário completar com todos os produtos disponíveis para venda, indicando o valor por unidade e o valor total de acordo com a quantidade vendida naquela semana, mês ou trimestre – o período que a organização definir.

# Após alocar esses dados na planilha, o segundo passo é dividir o valor total de cada produto pelo valor de vendas da loja no período determinado. O resultado será uma porcentagem, que deverá ser colocado em uma nova coluna.

# As colunas serão, respectivamente:

#     Nome do produto;
#     Quantidade vendida;
#     Valor por unidade;
#     Valor total por quantidade vendida;
#     Porcentagem do produto (valor total por quantidade dividido por quantidade vendida, em %);
#     Porcentagem acumulada (soma das porcentagens dos produtos, até chegar a 100%, que representa todas as vendas da empresa); e
#     Classificação ABC (a partir da porcentagem do produto).

# Portanto, vale relembrar:

#     A = produtos que representam até 80% das vendas;
#     B = produtos que representam até 15% das vendas; e
#     C = produtos que representam até 5% das vendas.
#
auditlog.register(Compra)
auditlog.register(Product)
auditlog.register(Frete)
auditlog.register(Tax)
auditlog.register(PickingList)
auditlog.register(CompraItem)
auditlog.register(NomeGrupoPessoas)
auditlog.register(NomeGrupoPessoasQuantidade)
auditlog.register(ProductGroup)
auditlog.register(AllProductGroup)
auditlog.register(ProductPrice)