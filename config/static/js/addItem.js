document.addEventListener('DOMContentLoaded',()=>{
    const idSearch = document.getElementById("idSearch");
    const suggestions = document.getElementById("suggestions");

    if (!idSearch || !suggestions) return;
    // PESSOA
    window.addEventListener("click", function (event) {
        if (!suggestions.contains(event.target) && event.target !== idSearch && suggestions.style.display != "none") {
            suggestions.style.display = "none";
            idSearch.value = "";
        }
    });

    window.addEventListener("keydown", function (event) {
        if (event.key === "Tab" && suggestions.style.display != "none") {
            suggestions.style.display = "none";
            idSearch.value = "";
        }
    });

    // PRODUTOS
    attachSuggestionListeners();
});

const emptyFormTemplate = document.getElementById('empty-form-template');
const emptyServiceTemplate = document.getElementById("empty-service-template");
const emptyPaymentMethodTemplate = document.getElementById('empty-payment-method-form');

const itensIndex  = [0];

function addItem() {
    const formset = document.getElementById('itens-container');
    const formCountProduts = document.getElementById("id_compraitem_set-TOTAL_FORMS") || document.getElementById('id_vendaitem_set-TOTAL_FORMS');
    if(formCountProduts){
        const itens = formset.querySelector(".itens");
        const [formCount,newForm] = clone(formCountProduts,emptyFormTemplate);
        formCountProduts.value = parseInt(formCount) + 1;

        const statusNewForm = newForm.querySelector("select");
        statusNewForm.value = "Pendente";


        itens.appendChild(newForm);
    }
    // PRODUTO
    attachSuggestionListeners();
}

function addItemService(){
    const formsetService = document.getElementById('itens-container-service');
   
    const formCountService = document.getElementById("id_vendaitemservice_set-TOTAL_FORMS");

    if(formCountService){
        const itensService = formsetService.querySelector('.itens');
        const [formCount,newForm] = clone(formCountService,emptyServiceTemplate);
        formCountService.value = parseInt(formCount) + 1;

        itensService.appendChild(newForm);
        
    }
    // SERVICOS
    attachSuggestionListeners();
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
    const itens_container = button.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
    
    const TOTAL_FORMS = itens_container.querySelector('input[type="hidden"][name$="-TOTAL_FORMS"]')
    const itens = itens_container.querySelector(".itens");
    const row_item = button.parentElement.parentElement;
    let formCount = TOTAL_FORMS.value;

    let  deleteButton = button.parentElement.querySelector('input[type="hidden"][name$="-DELETE"]');
    //SE TIVER SÓ UM ITEM, AO INVÉS DE APAGAR, OS CAMPOS IRÃO SER SOMENTE LIMPOS
    if(deleteButton.id.includes("0") && formCount == 1){
        let deleteButtons = row_item.querySelectorAll('input[id*="0"]');
        deleteButtons.forEach(deleteButton=>{
            deleteButton.value = "";
        })
    }
    else if(deleteButton.id.includes("0")){
        formCount-=1;
        TOTAL_FORMS.value = formCount;
        updateId(deleteButton,itens);
        itens.removeChild(row_item);
    }
    else{
        updateId(deleteButton,itens);
        deleteButton.value = "on";
        formCount-=1;
        TOTAL_FORMS.value = formCount;
        itens.removeChild(row_item);
    }

    if (TOTAL_FORMS.id == "id_vendaitemservice_set-TOTAL_FORMS"){
         const itemsContainerService = document.getElementById("itens-container-service");
         const itemForms = itemsContainerService.querySelectorAll("table tbody tr");  
         atualizarTotal(itemForms);
    }
    const itensContainerProduct = document.getElementById("itens-container");
    const itemForms = itensContainerProduct.querySelectorAll("table tbody tr");
    atualizarTotalProduto(itemForms);
    attachSuggestionListeners();
}

function updateId(deleteButton, itensForms) {
    const regex = /(\d+)/;
    const match = deleteButton.id.match(regex);
    if (!match) return;

    const deletedIndex = parseInt(match[1]);
    const allInputs = itensForms.querySelectorAll("input, select");

    allInputs.forEach((input) => {
        const inputMatch = input.id.match(/\d+/);
        if (!inputMatch) return;

        const inputIndex = parseInt(inputMatch[0]);

        // Só atualiza se o índice do input for maior que o deletado
        if (inputIndex > deletedIndex) {
            const oldId = input.id;
            const oldName = input.name;
            console.log('novo nome')
            console.log(oldName)
            const newIndex = inputIndex - 1;

            const newId = oldId.replace(inputMatch[0], newIndex);
            const newName = oldName.replace(inputMatch[0], newIndex);

            // Atualiza o ID e name
            input.id = newId;
            input.name = newName;

            // Se for campo "-id", tenta recuperar o valor anterior
            if (oldName.endsWith("-id")) {
                const oldInput = document.querySelector(`input[name="${newName}"]`);
                if (oldInput) {
                    input.value = oldInput.value;
                } else if (input.value === "") {
                    input.value = -1;
                }
            }
        } else if (input.id.endsWith("-id") && input.value === "") {
            // Se for o campo "-id" do último (ainda não reindexado) e estiver vazio
            input.value = -1;
        }
    });
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

function attachSuggestionListeners() {
    const suggestionsProducts = document.querySelectorAll(".suggetions");
    suggestionsProducts.forEach((suggestionProduct) => {
        const td = suggestionProduct.closest("td");
        if (!td) return;
        const input = td.querySelector('input[type="text"]');

        // Evita múltiplos listeners
        if (input.dataset.listenerAttached === "true") return;
        input.dataset.listenerAttached = "true";

        window.addEventListener("click", function(event){
            const isVisible = window.getComputedStyle(suggestionProduct).display !== "none";
            if (isVisible && !suggestionProduct.contains(event.target)) {
                suggestionProduct.style.display = "none";
                input.value = "";
            }
        });

        input.addEventListener("keydown", function (event) {
            const isVisible = window.getComputedStyle(suggestionProduct).display !== "none";
            if (event.key === "Tab" && isVisible) {
                suggestionProduct.style.display = "none";
                input.value = "";
            }
        });
    });
}