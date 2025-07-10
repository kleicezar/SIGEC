

from config.models import Situation
from finance.forms import PaymentMethodAccountsForm, PaymentMethodAccountsReadOnlyForm
from purchase.forms import CompraForm, CompraItemForm, CompraItemReadOnlyForm


class CompraService:

    @staticmethod
    def disabled_fields_based_on_situation(situation, compra):
        situation_object = Situation.objects.filter(id=int(situation)).first() if situation != "0" else compra.situacao

        form_map_compra = {
            f"{Situation.CLOSURE_LEVEL_OPTIONS[0][0]}": [CompraForm, True],
            f"{Situation.CLOSURE_LEVEL_OPTIONS[1][0]}": [CompraForm, True],
            f"{Situation.CLOSURE_LEVEL_OPTIONS[2][0]}": [CompraForm, True],
            f"{Situation.CLOSURE_LEVEL_OPTIONS[3][0]}": [CompraReadOnlyForm, False]
        }

        form_map_compraItem = {
            f"{Situation.CLOSURE_LEVEL_OPTIONS[0][0]}": [CompraItemForm, True],
            f"{Situation.CLOSURE_LEVEL_OPTIONS[1][0]}": [CompraItemReadOnlyForm, False],
            f"{Situation.CLOSURE_LEVEL_OPTIONS[2][0]}": [CompraItemForm, True],
            f"{Situation.CLOSURE_LEVEL_OPTIONS[3][0]}": [CompraItemReadOnlyForm, False]
        }
        
        

        form_map_payments = {
            f"{Situation.CLOSURE_LEVEL_OPTIONS[0][0]}": [PaymentMethodAccountsForm, True],
            f"{Situation.CLOSURE_LEVEL_OPTIONS[1][0]}": [PaymentMethodAccountsReadOnlyForm, False],
            f"{Situation.CLOSURE_LEVEL_OPTIONS[2][0]}": [PaymentMethodAccountsForm, True],
            f"{Situation.CLOSURE_LEVEL_OPTIONS[3][0]}": [PaymentMethodAccountsReadOnlyForm, False]
        }
        
    
        return (
            form_map_compra.get(situation_object.closure_level, [CompraForm, True]),
            form_map_compraItem.get(situation_object.closure_level, [CompraItemForm, True]),
            form_map_payments.get(situation_object.closure_level, [PaymentMethodAccountsForm, True])
        )

    # @staticmethod
    # def excluir_itens_venda_nao_submetidos(request, venda):
    #     ids_existentes = set(VendaItem.objects.filter(venda=venda).values_list('id', flat=True))
    #     ids_enviados = set(
    #         int(value)
    #         for key, value in request.POST.items()
    #         if key.startswith("vendaitem_set-") and key.endswith("-id") and value.isdigit()
    #     )
    #     ids_para_excluir = ids_existentes - ids_enviados
    #     if ids_para_excluir:
    #         VendaItem.objects.filter(id__in=ids_para_excluir).delete()

    # @staticmethod
    # def restaurar_credito_anterior(venda):
    #     credit = Credit.objects.filter(person=venda.pessoa).order_by('-id').first()
    #     if not credit:
    #         return

    #     pagamentos_ativos = PaymentMethod_Accounts.objects.filter(venda=venda.id, activeCredit=True)
    #     for pagamento in pagamentos_ativos:
    #         credit.credit_value += pagamento.value
    #     credit.save()

    # @staticmethod
    # def calculate_total_payment(request, new_formset, old_formset):
    #     value_new_form = str(request.POST.get('new_form', '')).lower()
    #     has_new_form = value_new_form in ['true', '1', 'on', 'yes']
    #     total = Decimal('0.00')

    #     target_formset = new_formset if has_new_form else old_formset
    #     for form in target_formset:
    #         if form.cleaned_data and not form.cleaned_data.get("DELETE"):
    #             total += form.cleaned_data.get('value', Decimal('0.00'))

    #     return total

    # @staticmethod
    # def descontar_credito_usado(request, venda, valor_usado, new_formset, old_formset):
    #     valor_usado = Decimal(valor_usado or '0.00')
    #     value_new_form = str(request.POST.get('new_form', '')).lower()
    #     has_new_form = value_new_form in ['true', '1', 'on', 'yes']
    #     target_formset = new_formset if has_new_form else old_formset

    #     for form in target_formset:
    #         if form.cleaned_data and form.cleaned_data.get("activeCredit"):
    #             creditos = Credit.objects.filter(person=venda.pessoa).order_by('id')
    #             restante = valor_usado

    #             for credito in creditos:
    #                 if restante <= 0:
    #                     break
    #                 if credito.credit_value >= restante:
    #                     credito.credit_value -= restante
    #                     restante = Decimal('0.00')
    #                 else:
    #                     restante -= credito.credit_value
    #                     credito.credit_value = Decimal('0.00')
    #                 credito.save()

    # @staticmethod
    # def sincronizar_pagamentos_antigos_e_novos(request, novos_formset, antigos_formset):
    #     value_new_form = str(request.POST.get('new_form', '')).lower()
    #     has_new_form = value_new_form in ['true', '1', 'on', 'yes']

    #     if has_new_form:
    #         for old_form, new_form in zip(antigos_formset, novos_formset):
    #             VendaService._copiar_dados_pagamento(old_form, new_form)
    #             new_form.cleaned_data["DELETE"] = True
    #         antigos_formset.save()
    #         novos_formset.save()
    #     else:
    #         for old_form, new_form in zip(antigos_formset, novos_formset):
    #             VendaService._copiar_dados_pagamento(old_form, new_form)

    #         for extra_form in antigos_formset[len(novos_formset):]:
    #             extra_form.instance.delete()
    #         antigos_formset.save()

    # @staticmethod
    # def _copiar_dados_pagamento(old_form, new_form):
    #     old = old_form.instance
    #     new = new_form.instance

    #     old.forma_pagamento = new.forma_pagamento
    #     old.expirationDate = new.expirationDate
    #     old.days = new.days
    #     old.value = new.value
    #     old.save()
