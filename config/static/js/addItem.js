function addItem() {
    const formset = document.getElementById('itens-container');
    const formCountElem = document.getElementById('id_vendaitem_set-TOTAL_FORMS');
    
    if (!formCountElem) {
        console.error("Elemento TOTAL_FORMS de VendaItem não encontrado!");
        return;
    }

    const formCount = formCountElem.value;
    const emptyFormTemplate = document.getElementById('empty-form-template');

    if (!emptyFormTemplate) {
        console.error("Template de formulário vazio (empty-form-template) não encontrado!");
        return;
    }

    const newForm = emptyFormTemplate.content.cloneNode(true);

    newForm.querySelectorAll('input, select').forEach(input => {
        input.name = input.name.replace('__prefix__', formCount);
        input.id = input.id.replace('__prefix__', formCount);
        input.value = ''; // Limpa os valores dos campos
    });

    formCountElem.value = parseInt(formCount) + 1;
    formset.appendChild(newForm);
}

function addPaymentMethod() {
    const container = document.getElementById('payment-method-container');
    const formCountElem = document.getElementById('id_paymentmethod_venda_set-TOTAL_FORMS');
    
    if (!formCountElem) {
        console.error("Elemento TOTAL_FORMS de PaymentMethod_Venda não encontrado!");
        return;
    }

    const formCount = formCountElem.value;
    const emptyPaymentMethodTemplate = document.getElementById('empty-payment-method-form');

    if (!emptyPaymentMethodTemplate) {
        console.error("Template de formulário vazio (empty-payment-method-form) não encontrado!");
        return;
    }

    const newForm = emptyPaymentMethodTemplate.content.cloneNode(true);

    newForm.querySelectorAll('input, select').forEach(input => {
        input.name = input.name.replace('__prefix__', formCount);
        input.id = input.id.replace('__prefix__', formCount);
    });

    formCountElem.value = parseInt(formCount) + 1;
    container.appendChild(newForm);
}
