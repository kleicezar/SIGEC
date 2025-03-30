function showSuggetions(input){
    let container_td = input.closest('td');
    let suggetionsBox = container_td.querySelector('.suggetions');
    let id_person = container_td.querySelector('[name="pessoa"]');
    suggetionsBox.style.display= "block";
    if(input.value.length >=1 && input.value.trim() !==""){
        const query = input.value;
        fetch(`/buscar_pessoas/?query=${encodeURIComponent(query)}`)
            .then(response => {
                if (response.ok && response.headers.get('Content-Type').includes('application/json')) {
                    return response.json();
                } else {
                    throw new Error('Response is not JSON');
                }
            })
            .then(data => {
                data.clientes.forEach(cliente => {
                    let newSuggest = document.createElement("div");
                    newSuggest.innerHTML = `${cliente.id} - ${cliente.name}`
                    suggetionsBox.appendChild(newSuggest);
                    newSuggest.onclick = function(){
                        id_person.value = cliente.id;
                        input.value = `${cliente.id} - ${cliente.name}`
                        suggetionsBox.style.display = "none";
                    }
                });
            });
    }
    else{
        suggetionsBox.style.display = "none";
    }
}

let preco_data;
function showSuggetionsProducts(input){

    let row = input.closest('tr');
    let container_td = input.closest('td');
    let price = row.cells[2].querySelector('input');
    let suggetionsBox = container_td.querySelector('.suggetions');
    let id_product = container_td.querySelector("[name$=product]");
    suggetionsBox.style.display= "block";
    if(input.value.length >=1 && input.value.trim() !==""){
        const query = input.value;
        fetch(`/buscar_produtos/?query=${encodeURIComponent(query)}`)
            .then(response => {
                if (response.ok && response.headers.get('Content-Type').includes('application/json')) {
                    return response.json();
                } else {
                    throw new Error('Response is not JSON');
                }
            })
            .then(data => {
                data.produtos.forEach(produto => {
                    suggetionsBox.innerHTML = ""
                    let newSuggest = document.createElement("div");
                    newSuggest.innerHTML = `${produto.product_code} - ${produto.description}`;
                    suggetionsBox.appendChild(newSuggest);
                    newSuggest.onclick = function(){
                            id_product.value = produto.id;
                            serviceInput = `${produto.id}`;
                            input.value = `${produto.product_code} - ${produto.description}`;
                            price.value = produto.selling_price;
                            suggetionsBox.style.display = "none";
                    }
                });
            });
    }
    else{
        suggetionsBox.style.display = "none";
    }
}


function showSuggetionsServices(input){
    let row = input.closest('tr');
    let container_td = input.closest('td');
    let price = row.cells[2].querySelector('input');
    let suggetionsBox = container_td.querySelector('.suggetions');
    let id_service = container_td.querySelector("[name$=service]");
    suggetionsBox.style.display= "block";
    if(input.value.length >=1 && input.value.trim() !==""){
        const query = input.value;
        fetch(`/buscar_servicos/?query=${encodeURIComponent(query)}`)
            .then(response => {
                if (response.ok && response.headers.get('Content-Type').includes('application/json')) {
                    return response.json();
                } else {
                    throw new Error('Response is not JSON');
                }
            })
            .then(data => {
                data.servicos.forEach(servico => {
                    suggetionsBox.innerHTML = "";
                    let newSuggest = document.createElement("div");
                    newSuggest.innerHTML = `${servico.id} - ${servico.name_Service}`
                    suggetionsBox.appendChild(newSuggest);
                    newSuggest.onclick = function(){
                            id_service.value = servico.id;
                            serviceInput = `${servico.id}`
                            input.value = `${servico.id} - ${servico.name_Service}`
                            price.value = servico.price;
                            preco_data = price.value;
                            suggetionsBox.style.display = "none";
                    }
                });
            });
    }
    else{
        suggetionsBox.style.display = "none";
    }
}




const totalValueField = document.getElementById("id_total_value_service");
const totalServicesField = document.getElementById("id_service_total");
const discountTotalField = document.getElementById("id_discount_total_service");
const itemsContainerService = document.getElementById("itens-container-service");

function calcularPreco(input) {
    let row = input.closest("tr"); 
    const itemForms = itemsContainerService.querySelectorAll(".item-form");

    let desconto = row.cells[1].querySelector("input").value || 0;
    // let preco = row.cells[2].querySelector("input").value || 0;

    let precoFinal = preco_data - (preco_data*(desconto/100))
    row.cells[2].querySelector("input").value = precoFinal.toFixed(2);
    
    atualizarTotal(itemForms);
}

function atualizarTotal(itemForms) {
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


const totalValueInput = document.getElementById("id_total_value");
const totalProductsInput = document.getElementById("id_product_total");
const totalDiscountInput = document.getElementById("id_discount_total");
const itemsContainer = document.getElementById("itens-container");

function calcularPrecoProduto(input){
    let row = input.closest("tr");
    const itemForms = itemsContainer.querySelectorAll(".item-form");

    let quantidade = row.cells[1].querySelector("input").value || 0;
    let preco = row.cells[2].querySelector("input").value || 0;
    let desconto = row.cells[3].querySelector("input").value || 0;
    let precoFinal = row.cells[4].querySelector("input").value;
    precoFinal = (preco - (desconto/100)*preco)*quantidade;
    row.cells[4].querySelector("input").value = precoFinal;

    atualizarTotalProduto(itemForms);

}

totalValue = document.getElementById("id_totalValue");
function atualizarTotalProduto(itemForms){
    let totalSemDesconto = 0;
    let totalComDesconto = 0;
    let totalProdutos = 0;

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
        totalValue.value = totalComDesconto.toFixed(2);
    });

    let percentualDesconto = totalSemDesconto > 0
        ? ((1 - totalComDesconto / totalSemDesconto) * 100).toFixed(2)
        : 0;

    totalDiscountInput.value = percentualDesconto;
    totalProductsInput.value = totalProdutos;
    totalValueInput.value = totalComDesconto.toFixed(2);
}

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

