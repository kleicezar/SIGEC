// function addItem() {
//     const formset = document.getElementById('itens-container');
//     const formCountElem = document.getElementById('id_vendaitem_set-TOTAL_FORMS');
    
//     if (!formCountElem) {
//         console.error("Elemento TOTAL_FORMS de VendaItem não encontrado!");
//         return;
//     }

//     const formCount = formCountElem.value;
//     const emptyFormTemplate = document.getElementById('empty-form-template');

//     if (!emptyFormTemplate) {
//         console.error("Template de formulário vazio (empty-form-template) não encontrado!");
//         return;
//     }

//     const newForm = emptyFormTemplate.content.cloneNode(true);

//     newForm.querySelectorAll('input, select').forEach(input => {
//         input.name = input.name.replace('__prefix__', formCount);
//         input.id = input.id.replace('__prefix__', formCount);
//         input.value = ''; // Limpa os valores dos c ampos
//     });

//     formCountElem.value = parseInt(formCount) + 1;
//     formset.appendChild(newForm);
// }
const itensIndex  = [0];
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
        // console.log(input)
    });



    // Cria ids para identificação da area em que sera requisitado os produtos pelo filtro do campo product
    formCountElem.value = parseInt(formCount) + 1;
    field_product=  newForm.querySelector(".field-product ");
    input_product = newForm.querySelector(".inputProduct");
    field_product.id = `products-${formCount}`;
    input_product.id = `idProduct-${formCount}`
    // console.log(field_product)
    formset.appendChild(newForm);

    const itens = formset.querySelectorAll(".item-form");



    

    itensIndex.push(formCount);
    


    
    // btnDeletar.addEventListener('click',()=>{
    //     formset.removeChild(newForm)
    // })
}


function removeItem(button){
    let  parent_button_3 = button.parentElement.parentElement.querySelector('input[type="hidden"][name$="-DELETE"]');
    parent_button_3.value = "on";
    let  parent_button_5 =  button.parentElement.parentElement.parentElement.parentElement;
    let  parent_button_6 =  button.parentElement.parentElement.parentElement.parentElement.parentElement;
    parent_button_6.removeChild(parent_button_5);
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

    const payments = container.querySelectorAll(".form-row");

    payments.forEach(payment=>{
        const table_payment = payment.querySelector("table");
        console.log(table_payment);
        const tbody_payment = table_payment.querySelector("tbody");
        const tr_payment = tbody_payment.querySelector("tr");
        const delet_payment = tr_payment.querySelector(".delete");

        delet_payment.addEventListener("click",()=>{
            tbody_payment.style.display = "none";
            const deleteFieldPayment = tr_payment.querySelector('input[type="hidden"][name$="-DELETE"]');
            deleteFieldPayment.value="on";
            console.log(deleteFieldPayment);
            console.log(deleteFieldPayment.value);
        })
    })
}



function addItemCompra() {
    const formset = document.getElementById('itens-container');
    const formCountElem = document.getElementById('id_compraitem_set-TOTAL_FORMS');
    
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

function addPaymentMethodCompra() {
    const container = document.getElementById('payment-method-container');
    const formCountElem = document.getElementById('id_paymentmethod_compra_set-TOTAL_FORMS');
    
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
