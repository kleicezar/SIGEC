// TOTAL VALOR DE FORMULARIO DE ITENS;
const totalValueField = document.getElementById("id_total_value_service");
const totalServicesField = document.getElementById("id_service_total");
// totalServicesField.value = 5;
const discountTotalField = document.getElementById("id_discount_total_service");
const itemsContainerService = document.getElementById("itens-container-service");

// Atualiza o total do desconto, valor total e total de produtos ao clicar no botão de deletar
itemsContainerService.addEventListener("click", (event) => {
    if (event.target.tagName === 'BUTTON') {
        const itemForms = itemsContainerService.querySelectorAll(".item-form");
        updateTotal(itemForms);
    }
});

itemsContainerService.addEventListener("input", (event) => {
    if (event.target.tagName === 'INPUT') {
        const itemForms = itemsContainerService.querySelectorAll(".item-form");
        const modifiedInput = event.target;
        const itemForm = modifiedInput.closest(".item-form");
        const itemFormInputs = itemForm.querySelectorAll("input");
        let productInput,discountInput,unitPriceInput,searchProductInput;

        
        
        updateTotal(itemForms);
    }
});

const serviceInputs = document.querySelectorAll('input[type="hidden"][name$="-service"]')
serviceInputs.forEach(serviceInput=>{
    const parentElement = serviceInput.parentElement;
    const textInput = parentElement.querySelector('input[type="text"]');

    if(serviceInput.value != ''){
        console.log('Fetching service data');
        const query = serviceInput.value;
        console.log(query);
        fetch(`/get_service_id/?query=${encodeURIComponent(query)}`)
        .then(response => {
            if (response.ok && response.headers.get('Content-Type').includes('application/json')) {
                return response.json();
            } else {
                throw new Error('Response is not JSON');
            }
        })
        .then(data=>{
            textInput.value = `${data.servico[0].id} - ${data.servico[0].name_Service}`;
        });

    }
    
})
function updateTotal(itemForms) {
    let totalSemDesconto = 0;
    let totalComDesconto = 0;
    let totalServicos = 0;

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
            console.log('------')
            console.log(subtotalSemDesconto);

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
}

const productInputFields = document.querySelectorAll('input[type="hidden"][name$="-product"]');

productInputFields.forEach(inputProduct => {
    let container = inputProduct.parentElement;
    let inputText = container.querySelector('input[type="text"]');

    if (inputProduct.value !== '') {
        const query = inputProduct.value;
        fetch(`/get_product_id/?query=${encodeURIComponent(query)}`)
            .then(response => {
                if (response.ok && response.headers.get('Content-Type').includes('application/json')) {
                    return response.json();
                } else {
                    throw new Error('Resposta não é JSON');
                }
            })
            .then(data => {
                inputText.value = `${data.produto[0].product_code} - ${data.produto[0].description}`;
            });
    }
});




let productInputs = document.querySelectorAll('input[type="hidden"][name$="-product"]');
if (productInputs.length === 0) {
    productInputs = document.querySelectorAll('input[type="hidden"][name$="-produto"]');
}

productInputs.forEach(productInput => {
    const parentElement = productInput.parentElement;
    const textInput = parentElement.querySelector('input[type="text"]');

    if (productInput.value !== '') {
        console.log('Fetching product data');
        const query = productInput.value;
        fetch(`/get_product_id/?query=${encodeURIComponent(query)}`)
            .then(response => {
                if (response.ok && response.headers.get('Content-Type').includes('application/json')) {
                    return response.json();
                } else {
                    throw new Error('Response is not JSON');
                }
            })
            .then(data => {
                textInput.value = `${data.produto[0].product_code} - ${data.produto[0].description}`;
               
            });
    }
});