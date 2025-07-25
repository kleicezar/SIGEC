# Generated by Django 5.1.2 on 2025-07-23 23:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('config', '0001_initial'),
        ('registry', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NomeGrupoPessoas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_group', models.CharField(max_length=255, verbose_name='Nome do Grupo')),
            ],
        ),
        migrations.CreateModel(
            name='ProductGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_group', models.CharField(max_length=255, verbose_name='Nome do Grupo')),
            ],
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_da_compra', models.DateTimeField(verbose_name='Data da Compra')),
                ('total_value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Total')),
                ('product_total', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total de Produtos')),
                ('discount_total', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total de Descontos')),
                ('is_active', models.BooleanField(default=True, verbose_name='Está Ativo')),
                ('observation_product', models.TextField(blank=True, null=True, verbose_name='Observação sobre Produtos')),
                ('rmnExists', models.BooleanField(default=False, verbose_name='Romaneio')),
                ('freightExists', models.BooleanField(default=False, verbose_name='Frete')),
                ('taxExists', models.BooleanField(default=False, verbose_name='Imposto')),
                ('fornecedor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='registry.person', verbose_name='Fornecedor')),
                ('situacao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='config.situation', verbose_name='Situação')),
            ],
        ),
        migrations.CreateModel(
            name='Frete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('freight_type', models.CharField(blank=True, choices=[('FOB', 'FOB'), ('CIF', 'CIF')], max_length=3, null=True, verbose_name='Tipo de Frete')),
                ('valueFreight', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Valor do Frete')),
                ('numberOfInstallmentsFreight', models.IntegerField(blank=True, null=True, verbose_name='Número de Parcelas')),
                ('observation_freight', models.TextField(blank=True, null=True, verbose_name='Observação sobre Frete')),
                ('compra', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='purchase.compra')),
            ],
        ),
        migrations.CreateModel(
            name='NomeGrupoPessoasQuantidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.nomegrupopessoas', verbose_name='NomeGrupoPessoasQuantidades')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registry.person', verbose_name='Pessoa')),
            ],
        ),
        migrations.CreateModel(
            name='PickingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valuePickingList', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Valor do RMN')),
                ('numberOfInstallmentsRMN', models.IntegerField(verbose_name='Número de Parcelas')),
                ('observation_picking_list', models.TextField(blank=True, null=True, verbose_name='Observação sobre Romaneio')),
                ('compra', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='purchase.compra')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255, verbose_name='Descrição')),
                ('product_code', models.CharField(max_length=100, verbose_name='Código do Produto')),
                ('barcode', models.CharField(max_length=100, verbose_name='Código de Barras')),
                ('unit_of_measure', models.CharField(max_length=50, verbose_name='Unidade de Medida')),
                ('brand', models.CharField(max_length=100, verbose_name='Marca')),
                ('cost_of_product', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Custo do Produto')),
                ('selling_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço de Venda')),
                ('ncm', models.CharField(max_length=10, verbose_name='NCM')),
                ('csosn', models.CharField(max_length=5, verbose_name='CSOSN')),
                ('cfop', models.CharField(max_length=7, verbose_name='CFOP')),
                ('current_quantity', models.IntegerField(verbose_name='Quantidade Atual')),
                ('maximum_quantity', models.IntegerField(verbose_name='Quantidade Máxima')),
                ('minimum_quantity', models.IntegerField(verbose_name='Quantidade Mínima')),
                ('is_active', models.BooleanField(default=True, verbose_name='Está Ativo')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registry.person', verbose_name='Fornecedor')),
            ],
        ),
        migrations.CreateModel(
            name='CompraItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField(verbose_name='Quantidade do Produto')),
                ('preco_unitario', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço Unitário')),
                ('discount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('price_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(default='Pendente', max_length=50)),
                ('compra', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='purchase.compra', verbose_name='Compra')),
                ('produto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='purchase.product', verbose_name='Produto')),
            ],
        ),
        migrations.CreateModel(
            name='AllProductGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customized_price', models.IntegerField(verbose_name='Preço Customizado')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.product', verbose_name='Produtos')),
                ('group_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.productgroup', verbose_name='NomeGrupoPessoasQuantidades')),
            ],
        ),
        migrations.CreateModel(
            name='ProductPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='purchase.nomegrupopessoasquantidade', verbose_name='Pessoa')),
                ('product_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.allproductgroup', verbose_name='Produtos')),
            ],
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valueTax', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Valor do Imposto')),
                ('numberOfInstallmentsTax', models.IntegerField(verbose_name='Número de Parcelas')),
                ('observation_tax', models.TextField(blank=True, null=True, verbose_name='Observação sobre Imposto')),
                ('compra', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='purchase.compra')),
            ],
        ),
    ]
