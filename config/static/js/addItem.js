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
const emptyFormTemplate = document.getElementById('empty-form-template');
const emptyPaymentMethodTemplate = document.getElementById('empty-payment-method-form');

const itensIndex  = [0];
function addItem() {
    const formset = document.getElementById('itens-container');
    const formCountSale = document.getElementById('id_vendaitem_set-TOTAL_FORMS');


    // const formCountElem = document.getElementById('id_vendaitem_set-TOTAL_FORMS');
    const formCountCompra = document.getElementById("id_compraitem_set-TOTAL_FORMS");
    if(formCountSale){
        const [formCount,newForm] = clone(formCountSale,emptyFormTemplate);
        formCountSale.value = parseInt(formCount) + 1;

        // field_product=  newForm.querySelector(".field-product ");
        input_product = newForm.querySelector(".inputProduct");

        // field_product.id = `products-${formCount}`;
        input_product.id = `idProduct-${formCount}`

        field_list_products = newForm.querySelector(".v");
        field_list_products.parentElement.style.display = "none";
        field_list_products.id = `options_products-${formCount}`;

        formset.appendChild(newForm);
    }
    if(formCountCompra){
        console.log('opo')
        // const emptyFormTemplate = document.getElementById('empty-form-template');
        const [formCount,newForm] = clone(formCountCompra,emptyFormTemplate);
        formCount.value = parseInt(formCount) + 1;

        input_product = newForm.querySelector(".inputProduct");

        // field_product.id = `products-${formCount}`;
        input_product.id = `idProduct-${formCount}`

        field_list_products = newForm.querySelector(".v");
        field_list_products.parentElement.style.display = "none";
        field_list_products.id = `options_products-${formCount}`;
        formset.appendChild(newForm)
        
    }
    


  



    // Cria ids para identificação da area em que sera requisitado os produtos pelo filtro do campo product
   



    
    // btnDeletar.addEventListener('click',()=>{
    //     formset.removeChild(newForm)
    // })
}

function clone(formCountElem,template){
    const formCount = formCountElem.value;
    // const emptyFormTemplate = document.getElementById('empty-form-template');

    if (!template) {
        console.error("Template de formulário vazio (empty-form-template) não encontrado!");
        return;
    }

    const newForm = template.content.cloneNode(true);

    newForm.querySelectorAll('input, select').forEach(input => {
        input.name = input.name.replace('__prefix__', formCount);
        input.id = input.id.replace('__prefix__', formCount);
        input.value = ''; // Limpa os valores dos campos
    });

    return [formCount,newForm];
}

function removeItem(button){
    let  parent_button_3 = button.parentElement.parentElement.querySelector('input[type="hidden"][name$="-DELETE"]');
    parent_button_3.value = "on";
    let  parent_button_5 =  button.parentElement.parentElement.parentElement.parentElement;
    let  parent_button_6 =  button.parentElement.parentElement.parentElement.parentElement.parentElement;
    console.log(parent_button_6)
    console.log(parent_button_5)
    parent_button_6.removeChild(parent_button_5);

}






function addPaymentMethod() {
    const container = document.getElementById('payment-method-container');
    const formCountCompra = document.getElementById('id_paymentmethod_compra_set-TOTAL_FORMS');
    const formCountSale = document.getElementById('id_paymentmethod_venda_set-TOTAL_FORMS');
    const formCountAccountPayable = document.getElementById('id_paymentmethod_accountspayable_set-TOTAL_FORMS');
    if(formCountSale){
        const [formCount,newForm] = clone(formCountSale,emptyPaymentMethodTemplate);
        formCountSale.value = parseInt(formCount)+1;
        container.appendChild(newForm);
    }
    if(formCountCompra){
        const [formCount,newForm] = clone(formCountCompra,emptyPaymentMethodTemplate);
        formCountCompra.value = parseInt(formCount)+1;
        container.appendChild(newForm);
    }
    if(formCountAccountPayable){
        const [formCount,newForm] = clone(formCountAccountPayable,emptyPaymentMethodTemplate);
        formCountAccountPayable.value = parseInt(formCount) + 1;
        container.appendChild(newForm);
    }

    // const formCount = formCountElem.value;
    


}


function removePayment(button){
    let parent_button_payment_3 = button.parentElement.parentElement.querySelector('input[type="hidden"][name$="-DELETE"]');
    parent_button_payment_3.value="on";
    let parent_button_payment_5 = button.parentElement.parentElement.parentElement.parentElement;
    let parent_button_payment_6 = button.parentElement.parentElement.parentElement.parentElement.parentElement;
    parent_button_payment_6.removeChild(parent_button_payment_5);
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