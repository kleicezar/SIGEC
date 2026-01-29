from django import forms
from .models import *
from django.contrib.auth.models import Permission, User, Group

CHECKBOX_CLASS = {'class': 'sr-only peer'}

# class PreSituation(forms.Form):
#     V_pessoa = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     V_data_da_venda = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     V_total_value = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     V_discount_total = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     V_value_apply_credit = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     V_product = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     V_quantidade = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     V_preco_unitario = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     V_discount = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     V_price_total = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     V_status = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     V_apply_credit = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     V_product_total = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     V_forma_pagamento = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     V_expirationDate = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     V_valor = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     V_observacao_pessoas = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     V_observacao_sistema = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))

#     OS_apply_credit = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     OS_pessoa = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     OS_data_da_venda = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     OS_observacao_pessoas = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     OS_observacao_sistema = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     OS_total_value = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     OS_product_total = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     OS_discount_total = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     OS_value_apply_credit = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     OS_service_total = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     OS_discount_total_service = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     OS_total_value_service = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     OS_preco = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     OS_discount = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     OS_technician = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     OS_expirationDate = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     OS_valor = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     OS_quantidade = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     OS_preco_unitario = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     OS_price_total = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     OS_status = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))

#     C_description = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_product_code = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_barcode = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_unit_of_measure = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_brand = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_cost_of_product = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_selling_price = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_ncm = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_csosn = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_cfop = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_current_quantity = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_maximum_quantity = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_minimum_quantity = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_data_da_compra = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_total_value = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_product_total = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_discount_total = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_observation_product = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_freight_type = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_valueFreight = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_numberOfInstallmentsFreight = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_observation_freight = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_valueTax = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_numberOfInstallmentsTax = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_observation_tax = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_valuePickingList = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_numberOfInstallmentsRMN = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_observation_picking_list = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_quantidade = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_preco_unitario = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_discount = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
#     C_price_total = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))

class SituationModelForm(forms.ModelForm):
    class Meta:
        model = Situation
        fields = ['name_Situation', 'V_pessoa' ,'V_data_da_venda' ,'V_total_value' ,'V_discount_total','V_value_apply_credit','V_product' , 'V_quantidade', 'V_preco_unitario', 'V_discount', 'V_price_total', 'V_status', 'V_apply_credit', 'V_product_total', 'V_forma_pagamento', 'V_expirationDate', 'V_valor', 'V_observacao_pessoas', 'V_observacao_sistema','V_estagio_inicial','V_movement_storage','V_movement_accounts', 'OS_pessoa', 'OS_apply_credit', 'OS_data_da_venda', 'OS_observacao_pessoas','OS_observacao_sistema','OS_total_value','OS_product_total','OS_discount_total','OS_value_apply_credit','OS_service_total','OS_discount_total_service','OS_total_value_service','OS_preco','OS_discount','OS_technician','OS_expirationDate','OS_valor','OS_quantidade','OS_preco_unitario','OS_discount','OS_price_total','OS_status', 'OS_estagio_inicial','OS_movement_storage','OS_movement_accounts','C_fornecedor','C_description','C_product_code','C_barcode','C_unit_of_measure','C_brand','C_cost_of_product','C_selling_price','C_ncm','C_csosn','C_cfop','C_current_quantity','C_maximum_quantity','C_minimum_quantity','C_data_da_compra','C_total_value','C_product_total','C_discount_total','C_observation_product','C_freight_type','C_valueFreight','C_numberOfInstallmentsFreight','C_observation_freight','C_valueTax','C_numberOfInstallmentsTax','C_observation_tax','C_valuePickingList','C_numberOfInstallmentsRMN','C_observation_picking_list','C_quantidade','C_preco_unitario','C_discount','C_price_total','C_estagio_inicial','C_movement_storage','C_movement_accounts','ACC_description','ACC_pessoa_id', 'ACC_chartOfAccounts','ACC_documentNumber','ACC_date_account', 'ACC_numberOfInstallments','ACC_installment_Range',  'ACC_date_init', 'ACC_totalValue','ACC_peopleWatching','ACC_systemWatching','ACC_plannedAccount','ACC_venda', 'ACC_compra', 'ACC_ordem_servico', 'ACC_forma_pagamento','ACC_expirationDate','ACC_days','ACC_value_old','ACC_value', 'ACC_interestType','ACC_interest', 'ACC_fineType','ACC_fine', 'ACC_acc',  'ACC_activeCredit', 'ACC_paymentPurpose', 'ACC_estagio_inicial', 'ACC_movement_storage', 'ACC_movement_accounts']
        widgets = {
            'name_Situation' : forms.TextInput(
                attrs = {
                    'class':'form-input block w-full rounded-lg border-slate-300 bg-white px-4 py-2.5 text-slate-900 placeholder-slate-400 focus:border-primary focus:ring-primary shadow-sm sm:text-sm',
                    'id':'customSituationName',
                    'placeholder':'Ex: Configuração Padrão Gerencial',
                }
            ),
            
             
            'V_estagio_inicial' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ), 
            'V_movement_storage' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ), 
            'V_movement_accounts' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ), 
            'OS_estagio_inicial' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ), 
            'OS_movement_storage' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ), 
            'OS_movement_accounts' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ), 
            'C_estagio_inicial' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ), 
            'C_movement_storage' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ), 
            'C_movement_accounts' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'ACC_estagio_inicial' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ), 
            'ACC_movement_storage' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ), 
            'ACC_movement_accounts' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),

            'V_pessoa' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'V_data_da_venda' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'V_total_value' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'V_discount_total' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'V_value_apply_credit' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'V_product' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'V_quantidade' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'V_preco_unitario' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'V_discount' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'V_price_total' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'V_status' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'V_apply_credit' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'V_product_total' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'V_forma_pagamento' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'V_expirationDate' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'V_valor' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'V_observacao_pessoas' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'V_observacao_sistema' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'OS_apply_credit' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'OS_pessoa' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'OS_data_da_venda' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'OS_observacao_pessoas' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'OS_observacao_sistema' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'OS_total_value' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'OS_product_total'  : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'OS_discount_total' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'OS_value_apply_credit' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'OS_service_total' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'OS_discount_total_service' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'OS_total_value_service' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'OS_preco' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'OS_discount' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'OS_technician' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'OS_expirationDate' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'OS_valor' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'OS_quantidade' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'OS_preco_unitario' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'OS_discount' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'OS_price_total' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'OS_status' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_fornecedor' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_description' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_product_code' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_barcode' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_unit_of_measure' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_brand' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_cost_of_product' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_selling_price' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_ncm' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_csosn' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_cfop' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_current_quantity' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_maximum_quantity' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_minimum_quantity' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_data_da_compra' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_total_value' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_product_total' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_discount_total' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_observation_product' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_freight_type' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_valueFreight' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_numberOfInstallmentsFreight' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_observation_freight' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_valueTax' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_numberOfInstallmentsTax' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_observation_tax' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_valuePickingList' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_numberOfInstallmentsRMN' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_observation_picking_list' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_quantidade' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_preco_unitario' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_discount' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),
            'C_price_total' : forms.CheckboxInput(attrs = CHECKBOX_CLASS ),

            'ACC_description' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_pessoa_id' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_chartOfAccounts' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_documentNumber' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_date_account' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_numberOfInstallments' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_installment_Range' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_date_init' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_totalValue' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_peopleWatching' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_systemWatching' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_plannedAccount' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_venda' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_compra' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_ordem_servico' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_forma_pagamento' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_expirationDate' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_days' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_value_old' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_value' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_interestType' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_interest' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_fineType' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_fine' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_acc' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_activeCredit' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_paymentPurpose' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_estagio_inicial' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_movement_storage' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
            'ACC_movement_accounts' : forms.CheckboxInput(attrs = CHECKBOX_CLASS),
        }


    def __init__(self, *args, **kwargs):
        super(SituationModelForm, self).__init__(*args, **kwargs)
        self.fields['name_Situation'].widget.attrs.update({'class': 'form-input block w-full rounded-lg border-slate-300 bg-white px-4 py-2.5 text-slate-900 placeholder-slate-400 focus:border-primary focus:ring-primary shadow-sm sm:text-sm'})

class ChartOfAccountsModelForm(forms.ModelForm):
    class Meta:
        
        model = ChartOfAccounts
        fields = ['name_ChartOfAccounts', 'father', 'natureOfTheAccount']
        widgets = {
            'name_ChartOfAccounts' : forms.TextInput(
                attrs = {
                    'class':'form-control'
                }
            ),
            'father':forms.Select(
                attrs={
                    'class':'form-select ' 
                }
            ),
            'natureOfTheAccount':forms.Select(
                attrs={
                    'class':'form-select ' 
                }
            ),
            # 'natureOfTheAccount' : forms.ChoiceField(choices=NatureOfTheAccount, label='Natureza da Conta')
        }

    def __init__(self, *args, **kwargs):
        super(ChartOfAccountsModelForm, self).__init__(*args, **kwargs)
        self.fields['name_ChartOfAccounts'].widget.attrs.update({'class': 'label-text'})

class PaymentMethodModelForm(forms.ModelForm):
    # ativo = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    
    class Meta:
        model = PaymentMethod
        fields = ['name_paymentMethod','creditPermission', 'considerInCash','bank']
        widgets = {
            'considerInCash' : forms.CheckboxInput(attrs={
                'class':'form-check-input'
                }),
            'creditPermission':forms.CheckboxInput(attrs={
                'class':'form-check-input'
                })
        } 

    def __init__(self, *args, **kwargs): 
        super(PaymentMethodModelForm, self).__init__(*args, **kwargs)
        self.fields['name_paymentMethod'].widget.attrs.update({'class': 'label-text'})

class BankModelForm(forms.ModelForm):
    # ativo = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    
    class Meta:
        model = Bank
        fields = ['bank_name','agencia', 'conta']

    def __init__(self, *args, **kwargs): 
        super(BankModelForm, self).__init__(*args, **kwargs)
        self.fields['bank_name'].widget.attrs.update({'class': 'label-text'})
        self.fields['agencia'].widget.attrs.update({'class': 'label-text'})
        self.fields['conta'].widget.attrs.update({'class': 'label-text'})

class PositionModelForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name_position']

    def __init__(self, *args, **kwargs):
        super(PositionModelForm, self).__init__(*args, **kwargs)
        self.fields['name_position'].widget.attrs.update({'class': 'label-text'})

class serviceModelForm(forms.ModelForm): 
    class Meta:
        model = Service
        fields = ['name_service','value_service']
        widgets = {
            'name_service':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'value_service':forms.NumberInput(attrs={
                'class':'form-control',
                'min':0.01
            })
        }   
        # self.fields['name_position'].widget.attrs.update({'class': 'label-text'})

class PermsForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = '__all__'
        # exclude = ['name','codename'] 
        widgets = {
            # 'name': forms.
        }

class UserPermissionAssignForm(forms.ModelForm): # Renomeei para clareza
    def label_from_instance(self, obj):
        modules_perms = {
            'Pessoa':{
                'address':'Endereço',
                'fisic person':'Pessoal Fisica',
                'foreign person':'Estrangeiro',
                'legal person':'Pessoa Juridica',
                'person':'Dados Gerais de Pessoa',
            },
            'Product':{
                'Product':'Produtos',
                'person':'Dados Gerais de Pessoa',
                },
            'Purchase':{
                'Product':'Produtos',
                'compra item':'Compras',
                'compra item':'Itens Presentes em Compras',
                },
            'accounts':{
                'accounts':'Contas',
                'accounts':'Contas',
                'accounts':'Contas',
                'accounts':'Contas',
                },
            'registry':'Cadastro',
            'sale':'Venda',
            'service':'Serviço',
            }
        # modules_name = {
        #     'Config':'Configuração',
        #     'Finance':'Financeiro',
        #     'Purchase':'Compras',
        #     'registry':'Cadastro',
        #     'sale':'Venda',
        #     'service':'Serviço',
        #     }
        # modules_perms = {
        #     'Config':'Configuração',
        #     'Finance':'Financeiro',
        #     'Purchase':'Compras',
        #     'registry':'Cadastro',
        #     'sale':'Venda',
        #     'service':'Serviço',
        #     }
        # models = {
        #     'chart of accounts':'Plano de Contas',
        #     'payment method':'Forma de Pagamento',
        #     'position':'Cargo',
        #     'service':'Serviço',
        #     'situation':'Situação',
        #     'accounts':'Contas',
        #     'caixa diario':'Caixa Diario',
        #     'cash movement':'Movimentação de Caixa',
        #     'fechamento de caixa':'Fechamento de Caixa',
        #     'paypayment method_ accounts':'Forma de Pagamento de Contas',
        #     '':'',
        # }

        # obj é uma instância do modelo Permission
        # O método __str__ padrão de Permission retorna algo como:
        # f"{obj.content_type.app_label} | {obj.content_type.model} | {obj.name}"

        # Você pode retornar o que quiser aqui. Exemplos:
        # return f"{obj.name}"  # Apenas o nome legível da permissão
        # return f"Permissão: {obj.name.upper()} (App: {obj.content_type.app_label})"
        # return f"Código: {obj.codename}" # Se quiser mostrar o codename
        
        # Exemplo de transformação simples (como um "pipe" faria):
        return obj.name.replace("Can ", "").capitalize() # Ex: "add user" -> "Add user"

    
    # user_permissions = forms.ModelMultipleChoiceField(
    #     queryset=Permission.objects.filter(content_type_id__gte = 7).order_by('content_type__app_label', 'content_type__model', 'name'),
    #     widget=forms.CheckboxSelectMultiple, # ISSO GERA OS CHECKBOXES
    #     required=False,
    #     label="Atribuir Permissões ao Usuário"
    # )

    group = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        label='Selecione as Permissões'
    )

    class Meta:
        model = Group # O formulário é para um Usuário
        fields = ['group'] # O campo que queremos editar no Usuário
    # Este formulário, quando instanciado com um objeto User,
    # mostrará todas as permissões como checkboxes,
    # e as permissões que o usuário já possui virão marcadas.

class PermissionMultipleSelectForm(forms.Form):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Permissões"
    )

class SuperGroupForm(forms.ModelForm):
    class Meta:
        model = SuperGroup
        fields = ['name', 'groups', 'members']  # Campos que estarão no formulário
        widgets = {
            'groups': forms.CheckboxSelectMultiple,  # Lista de grupos com checkboxes
            'members': forms.CheckboxSelectMultiple, # Lista de usuários com checkboxes (opcional, pode ser outro widget)
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opcional: Ordenar os itens nos checkboxes
        if 'groups' in self.fields:
            # Certifique-se de que django.contrib.auth.models.Group está importado
            self.fields['groups'].queryset = Group.objects.order_by('name')
        if 'members' in self.fields:
            # Certifique-se de que django.contrib.auth.models.User está importado
            self.fields['members'].queryset = User.objects.order_by('username')

class PermsForm(forms.Form):
    """
    Baseado no CRUD é necessario a seleção dos campos que o usuário terá permissão de 
    visualizar (read), editar (update) e remover (delete).
    Cada campo do formulario estará relacionado a um campo do modelo.
    Cada campo é representado por um numero indo de 0 a 7 em binario representando uma 
    permissão que pode ser marcada ou desmarcada baseada no read-update-delete.
    
    Codigo:
        000: Sem permissão
        100: Permissão apenas de leitura (read)
        010: Permissão apenas de atualização (update)
        001: Permissão apenas de remoção (delete)
        110: Permissão de leitura e atualização (read e update)
        101: Permissão de leitura e remoção (read e delete)
        011: Permissão de atualização e remoção (update e delete)
        111: Permissão total (read, update e delete)
    """
    V_pessoa = forms.BooleanField(label='pessoa') 
    V_data_da_venda = forms.BooleanField(label='data_da_venda') 
    V_total_value = forms.BooleanField(label='total_value')
    V_discount_total = forms.BooleanField(label='discount_total')
    V_value_apply_credit = forms.BooleanField(label='value_apply_credit')
    V_product = forms.BooleanField(label='product') 
    V_quantidade = forms.BooleanField(label='quantidade') 
    V_preco_unitario = forms.BooleanField(label='preco_unitario') 
    V_discount = forms.BooleanField(label='discount') 
    V_price_total = forms.BooleanField(label='price_total') 
    V_status = forms.BooleanField(label='status')
    V_apply_credit = forms.BooleanField(label='apply_credit')
    V_product_total = forms.BooleanField(label='product_total') 
    V_forma_pagamento = forms.BooleanField(label='forma_pagamento') 
    V_expirationDate = forms.BooleanField(label='expirationDate') 
    V_valor = forms.BooleanField(label='valor')
    V_observacao_pessoas = forms.BooleanField(label='observacao_pessoas') 
    V_observacao_sistema = forms.BooleanField(label='observacao_sistema')


class PermsForm(forms.Form):
    """
    Formulário para selecionar permissões específicas.
    Cada campo booleano representa uma permissão que pode ser marcada ou desmarcada.
    
    Vendas:

        V_pessoa : Permissão relacionada a seleção da pessoa na venda.
        V_data : Permissão relacionada à data da venda.
        V_total_value : Permissão relacionada ao valor total da venda.
        V_discount_total : Permissão relacionada ao desconto total da venda.
        V_value_apply_credit : Permissão relacionada ao valor aplicado de crédito na venda.

    Compras:

        C_pessoa : Permissão relacionada a seleção da pessoa na compra.
        C_data : Permissão relacionada à data da compra.
        C_total_value : Permissão relacionada ao valor total da compra.
    
    Ordem de Serviço:
    
        OS_pessoa : Permissão relacionada a seleção da pessoa na ordem de serviço.
        OS_data : Permissão relacionada à data da ordem de serviço.
        OS_total_value : Permissão relacionada ao valor total da ordem de serviço.

    """
    V_pessoa = forms.BooleanField(label='Pessoa') 
    V_data_da_venda = forms.BooleanField(label='Data da Venda') 
    V_total_value = forms.BooleanField(label='Valor Total')
    V_discount_total = forms.BooleanField(label='Total de Desconto')
    V_value_apply_credit = forms.BooleanField(label='Valor Aplicado de Crédito')
    V_product = forms.BooleanField(label='Produto na Venda') 
    V_quantidade = forms.BooleanField(label='quantidade') 
    V_preco_unitario = forms.BooleanField(label='Preço Unitário na Venda') 
    V_discount = forms.BooleanField(label='Valor do Desconto na Venda') 
    V_price_total = forms.BooleanField(label='Preço Total na Venda') 
    V_apply_credit = forms.BooleanField(label='Aplicar Crédito na Venda')
    V_product_total = forms.BooleanField(label='Total de Produtos na Venda') 
    V_forma_pagamento = forms.BooleanField(label='Forma de Pagamento na Venda') 
    V_expirationDate = forms.BooleanField(label='Data de Vencimento na Venda') 
    V_valor = forms.BooleanField(label='Valor das Parcelas na Venda')
    V_observacao_pessoas = forms.BooleanField(label='Observação visiveis para Pessoas') 
    V_observacao_sistema = forms.BooleanField(label='Observação no Sistema')
    V_status = forms.BooleanField(label='status da Venda')

# class SituationModelForm(forms.ModelForm):
#     class Meta:
#         model = Situation
#         fields = ['name_Situation']
#         widgets = {
#             'name_Situation' : forms.TextInput(
#                 attrs = {
#                     'class':'form-control row'
#                 }
#             ),
#         }

#     def __init__(self, *args, **kwargs):
#         super(SituationModelForm, self).__init__(*args, **kwargs)
#         self.fields['name_Situation'].widget.attrs.update({'class': 'label-text'})