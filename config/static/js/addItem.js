const emptyFormTemplate = document.getElementById('empty-form-template');
const emptyServiceTemplate = document.getElementById("empty-service-template");
const emptyPaymentMethodTemplate = document.getElementById('empty-payment-method-form');

const itensIndex  = [0];

function addItem() {
    const formset = document.getElementById('itens-container');
    const formCountSale = document.getElementById('id_vendaitem_set-TOTAL_FORMS');
    const formCountService = document.getElementById("id_vendaitemproductservice_set-TOTAL_FORMS");

    if(formCountService){
        const [formCount,newForm] = clone(formCountService,emptyFormTemplate);
        formCountService.value = parseInt(formCount) + 1;

        const statusNewForm = newForm.querySelector("select");
        statusNewForm.value = 'Pendente';

        formset.appendChild(newForm);
        
    }
    const formCountCompra = document.getElementById("id_compraitem_set-TOTAL_FORMS");
    if(formCountSale){
        const [formCount,newForm] = clone(formCountSale,emptyFormTemplate);
        formCountSale.value = parseInt(formCount) + 1;

        const statusNewForm = newForm.querySelector("select");
        statusNewForm.value = "Pendente";


        formset.appendChild(newForm);
    }
    if(formCountCompra){
        console.log(formCountCompra)
        const [formCount,newForm] = clone(formCountCompra,emptyFormTemplate);
        formCountCompra.value = parseInt(formCount) + 1 ;
        console.log(formCountCompra.value)
        input_product = newForm.querySelector(".inputProduct");

        const statusNewForm = newForm.querySelector("select");
        statusNewForm.value = "Pendente";
       
        formset.appendChild(newForm)
        
    }
    // Cria ids para identificação da area em que sera requisitado os produtos pelo filtro do campo product
   
}

function addItemService(){
    const formset = document.getElementById('itens-container-service');
    const formCountService = document.getElementById("id_vendaitemservice_set-TOTAL_FORMS");

    if(formCountService){
        const [formCount,newForm] = clone(formCountService,emptyServiceTemplate);
        formCountService.value = parseInt(formCount) + 1;
        
        formset.appendChild(newForm);
    }
}

function clone(formCountElem,template){
    const formCount = parseInt(formCountElem.value);
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
    const itens_container = document.getElementById("itens-container");
    const TOTAL_FORMS = document.getElementById("id_vendaitem_set-TOTAL_FORMS") || document.getElementById("id_compraitem_set-TOTAL_FORMS") || document.getElementById("id_vendaitemservice_set-TOTAL_FORMS") || document.getElementById("id_vendaitemproductservice_set-TOTAL_FORMS");
    let formCount = TOTAL_FORMS.value;
    let  parent_button =  button.parentElement.parentElement.parentElement.parentElement;
    let  parent_button_2 =  button.parentElement.parentElement.parentElement.parentElement.parentElement;
    let  deleteButton = button.parentElement.parentElement.querySelector('input[type="hidden"][name$="-DELETE"]');
    let itensForms = itens_container;

    //SE TIVER SÓ UM ITEM, AO INVÉS DE APAGAR, OS CAMPOS IRÃO SER SOMENTE LIMPOS
    if(deleteButton.id.includes("0") && formCount == 1){
        let deleteButtons = parent_button.querySelectorAll('input[id*="0"]');
        deleteButtons.forEach(deleteButton=>{
            deleteButton.value = "";
        })
    }
    else if(deleteButton.id.includes("0")){
        formCount-=1;
        TOTAL_FORMS.value = formCount;
        updateId(deleteButton,itensForms);
        parent_button_2.removeChild(parent_button);

        const next_tr = parent_button_2.parentElement.querySelector("table thead tr");
        next_tr.style.display = "table-row";
    }
    else{
        updateId(deleteButton,itensForms);
        deleteButton.value = "on";
        formCount-=1;
        TOTAL_FORMS.value = formCount;
        parent_button_2.removeChild(parent_button);
    }

    const formCountService = document.getElementById("id_vendaitemproductservice_set-TOTAL_FORMS");
    if (formCountService){
         const itemsContainerService = document.getElementById("itens-container-service");
         const itemForms = itemsContainerService.querySelectorAll(".item-form");  
         atualizarTotal(itemForms);
    }
    // else{
    //     const itemForms = itens_container.querySelectorAll(".item-form");
    //     atualizarTotal(itemForms);
    // }
    const itemForms = itens_container.querySelectorAll(".item-form");
    atualizarTotalProduto(itemForms);
}
function updateId(deleteButton, itensForms) {
    let regex = /(\d+)/; // Captura qualquer número dentro do ID
    let match = deleteButton.id.match(regex);
    let matchName = deleteButton.name.match(regex)
    if (!match) return; // Se não encontrar número no ID do botão, sai da função

    let number = parseInt(match[1]); // Número extraído do ID
    let allInputs = itensForms.querySelectorAll("input,select");

    // Atualiza IDs dos inputs
    allInputs.forEach(input => {
        if (input.id.endsWith("-id")){
            if (input.value == ""){
                input.value = -1;
            }
        }
            let inputMatch = input.id.match(/\d+/); // Captura número do input
            if (!inputMatch) return; // Evita erro se o ID não tiver número

            let inputNumber = parseInt(inputMatch[0]); // Converte para número
            // ASSIM, OS IDS SAO TROCADOS SÓ SE FOREM MAIORES QUE O DELETADO;
            if (inputNumber - 1 >= number) {
        
                inputNumber = inputNumber - 1;
                let onInput  = input.value;

                let novoName = input.name.replace(inputMatch[0],inputNumber);
                let novoId = input.id.replace(inputMatch[0], inputNumber);
                
                if (input.name.endsWith("-id")){
                    oldInputValue = document.querySelector(`input[name="${novoName}"]`).value;
                    input.value = oldInputValue;
                    input.id = novoId; // Atribui novo ID     
                    input.name = novoName
                   
                }
                else{
                    input.value = onInput;
                    input.id = novoId; // Atribui novo ID     
                    input.name = novoName
                }
                
            }
        
    });

}


function removeItemUpdate(button){
    const itens_container = document.getElementById("itens-container");
    let containerItems = button.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
    const TOTAL_FORMS = containerItems.querySelector("#id_vendaitem_set-TOTAL_FORMS") ||
                    containerItems.querySelector("#id_compraitem_set-TOTAL_FORMS") ||
                    containerItems.querySelector("#id_vendaitemservice_set-TOTAL_FORMS") ||
                    containerItems.querySelector("#id_vendaitemproductservice_set-TOTAL_FORMS");

    let formCount = TOTAL_FORMS.value;
    let itensForms = itens_container;
    let parent_button =  button.parentElement.parentElement.parentElement.parentElement;
    let parent_button_2 =  button.parentElement.parentElement.parentElement.parentElement.parentElement;

    let deleteButton = button.parentElement.parentElement.querySelector('input[type="hidden"][name$="-DELETE"]')

    if(deleteButton.id.includes("0") && formCount == 1){

        let deleteButtons = parent_button_2.querySelectorAll('input[id*="0"]');
        deleteButtons.forEach(deleteButton=>{
            deleteButton.value = "";
        })

    }
    else if(deleteButton.id.includes("0")){
        formCount-=1;
        TOTAL_FORMS.value = formCount;
        updateId(deleteButton,itensForms);

        parent_button_2.removeChild(parent_button);
        const next_tr = parent_button_2.parentElement.querySelector(".item-form table thead tr");

        next_tr.style.display = "table-row";
    }
    else{

        updateId(deleteButton,itensForms);
        deleteButton.value="on";
        console.log(formCount)
        formCount-=1;
        TOTAL_FORMS.value = formCount;
        parent_button_2.removeChild(parent_button);
        
    }
    const formCountService = document.getElementById("id_vendaitemproductservice_set-TOTAL_FORMS");
    if (formCountService){
         const itemsContainerService = document.getElementById("itens-container-service");
         const itemForms = itemsContainerService.querySelectorAll(".item-form");  
         atualizarTotal(itemForms);
    }
    const itemForms = itens_container.querySelectorAll(".item-form");
    atualizarTotalProduto(itemForms);
   
}

function addPaymentMethod() {
    const container = document.getElementById('payment-method-container');
    const formCountCompra = document.getElementById('id_paymentmethod_compra_set-TOTAL_FORMS');
    const formCountSale = document.getElementById('id_paymentmethod_venda_set-TOTAL_FORMS');
    const formCountAccountPayable = document.getElementById('id_paymentmethod_accountspayable_set-TOTAL_FORMS');
    const formCountService = document.getElementById("id_paymentmethod_vendaservice_set-TOTAL_FORMS");
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
    if(formCountService){
        const [formCount,newForm] = clone(formCountService,emptyPaymentMethodTemplate);
        formCountService.value = parseInt(formCount)+1;
        container.appendChild(newForm);
    }
}

function removePayment(button){
    let parent_button_payment = button.parentElement.parentElement.querySelector('input[type="hidden"][name$="-DELETE"]');
    parent_button_payment.value="on";
    let parent_button_payment_2 = button.parentElement.parentElement.parentElement.parentElement;
    let parent_button_payment_3 = button.parentElement.parentElement.parentElement.parentElement.parentElement;
    parent_button_payment_3.removeChild(parent_button_payment_2);
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



function atualizarTotalProduto(itemForms){
    let totalSemDesconto = 0;
    let totalComDesconto = 0;
    let totalProdutos = 0;
    const totalValueInput = document.getElementById("id_total_value");
    totalValueInput.value = 0;
    itemForms.forEach(itemForm => {
        if (window.getComputedStyle(itemForm).display !== 'none') {
            const inputs = itemForm.querySelectorAll("input");
            let quantidade = 0, precoUnitario = 0, desconto = 0, totalItem = 0;

            inputs.forEach(input => {
                if (input.id.endsWith("quantidade")) {
                    quantidade = Number(input.value) || 0;
                } else if (input.id.endsWith("preco_unitario")) {
                    precoUnitario = Number(input.value) || 0;
                } else if (input.id.endsWith("discount")) {
                    desconto = Number(input.value) || 0;
                } else if (input.id.endsWith("price_total")) {
                    totalItem = Number(input.value) || 0;
                }
            });

            let subtotalSemDesconto = precoUnitario * quantidade;
            let subtotalComDesconto = subtotalSemDesconto * (1 - desconto / 100);

            totalSemDesconto += subtotalSemDesconto;
            totalComDesconto += subtotalComDesconto;
            totalProdutos += quantidade;
        }
        // totalValue.value = totalComDesconto.toFixed(2);
    });

    let percentualDesconto = totalSemDesconto > 0
        ? ((1 - totalComDesconto / totalSemDesconto) * 100).toFixed(2)
        : 0;

    totalDiscountInput.value = percentualDesconto;
    totalProductsInput.value = totalProdutos;
    totalValueInput.value = totalComDesconto.toFixed(2);

    if (totalValueField){
        totalValue.value = Number(totalValueField.value) + Number(totalValueInput.value);
    }
    else{
        totalValue.value = Number(totalValueInput.value);
    }
   
}

function atualizarTotal(itemForms) {
    let totalSemDesconto = 0;
    let totalComDesconto = 0;
    let totalServicos = 0;
    const totalValueField = document.getElementById("id_total_value_service");
    totalValueField.value = 0;
    itemForms.forEach(itemForm=>{
        if(window.getComputedStyle(itemForm).display != 'none'){
            const inputs = itemForm.querySelectorAll("input");

            let quantidade = 0, precoUnitario = 0, desconto = 0, totalItem = 0;

            inputs.forEach(input=>{

                if(input.id.endsWith("discount")){
                    desconto = Number(input.value) || 0;
                }
                else if(input.id.endsWith("preco")){
                    precoUnitario = Number(input.value) || 0;               
                }
                
            })
           
            let subtotalComDesconto = precoUnitario;
            let subtotalSemDesconto = precoUnitario + precoUnitario*(desconto/100);
            
            totalSemDesconto += subtotalSemDesconto;
            totalComDesconto += subtotalComDesconto
        }
        totalServicos+=1;
    })

    let percentualDesconto = totalSemDesconto > 0
    ? ((1 - totalComDesconto / totalSemDesconto)*100).toFixed(2)
    : 0;

    discountTotalField.value = percentualDesconto;
    totalServicesField.value = totalServicos;
    totalValueField.value = totalComDesconto.toFixed(2);


    totalValue.value = Number(totalValueField.value) + Number(totalValueInput.value);
}