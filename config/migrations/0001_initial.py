from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChartOfAccounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_ChartOfAccounts', models.CharField(max_length=50, verbose_name='Nome do Plano de Contas')),
                ('is_Active', models.BooleanField(default=True, verbose_name='ativo')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_paymentMethod', models.CharField(max_length=50, verbose_name='Nome da Forma de Pagamento')),
                ('creditPermission', models.BooleanField(default=False, verbose_name='creditPermission')),
                ('considerInCash', models.BooleanField(blank=True, default=False, null=True, verbose_name='considerar em caixa')),
                ('is_Active', models.BooleanField(default=True, verbose_name='ativo')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_position', models.CharField(max_length=25, verbose_name='Nome do Cargo')),
                ('is_Active', models.BooleanField(default=True, verbose_name='ativo')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_Service', models.CharField(max_length=500, verbose_name='Nome do Serviço')),
                ('is_Active', models.BooleanField(default=True, verbose_name='ativo')),
                ('value_Service', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Valor do Serviço')),
            ],
        ),
        migrations.CreateModel(
            name='Situation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_Situation', models.CharField(max_length=50, verbose_name='Nome da Situação')),
                ('is_Active', models.BooleanField(default=True, verbose_name='ativo')),
            ],
        ),
    ]
