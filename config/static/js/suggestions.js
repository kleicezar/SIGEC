
function showSuggetions(input){
    let container_td = input.closest('td');
    let suggetionsBox = container_td.querySelector('.suggetions');
    let id_client = container_td.querySelector('[name="pessoa"]')
    id_supplier = container_td.querySelector('[name="fornecedor"]');
    suggetionsBox.style.display= "block";

    const credit = document.getElementById('credit');
    const credit_value = document.getElementById("id_value_apply_credit");
    const checkbox_credit = document.getElementById('id_apply_credit');
    if(input.value.length >=1 && input.value.trim() !==""){
        const query = input.value;

        if(credit){
            credit_value.value = 0;
            credit.style.display = "none";
        }

        if (id_client){
            fetch(`/buscar_pessoas/?query=${encodeURIComponent(query)}`)
                .then(response => {
                    if (response.ok && response.headers.get('Content-Type').includes('application/json')) {
                        return response.json();
                    } else {
                        throw new Error('Response is not JSON');
                    }
                })
                .then(data => {
                    suggetionsBox.innerHTML = "";
                    data.clientes.forEach(cliente => {
                        let newSuggest = document.createElement("div");
                        newSuggest.innerHTML = `${cliente.id} - ${cliente.name}`
                        suggetionsBox.appendChild(newSuggest);
                        newSuggest.onclick = function(){
                            id_client.value = cliente.id;
                            input.value = `${cliente.id} - ${cliente.name}`
                            suggetionsBox.style.display = "none";

                            if (credit){
                                const query = cliente.id;
                                fetch(`/credit_total/?query=${encodeURIComponent(query)}`)
                                .then(response=>{
                                    if(response.ok && response.headers.get('Content-Type').includes('application/json')){
                                        return response.json();
                                    } else{
                                        throw new Error('Resposta não é JSON')
                                    }
                                })
                                .then(data=>{
                                    checkbox_credit.onclick = null;
                                    credit_value.disabled = false;
                                    credit_value.value = data.credit_total;
                                    credit_value.max = data.credit_total;
                                    credit_value.min = 0;
                                })
                                .catch(error => console.error("Erro ao buscar vendas:",error));
                            }
                            
                            }
                        });
                    });
                                
        }
        else{
            fetch(`/buscar_fornecedores/?query=${encodeURIComponent(query)}`)
                .then(response => {
                    if (response.ok && response.headers.get('Content-Type').includes('application/json')) {
                        return response.json();
                    } else {
                        throw new Error('Response is not JSON');
                    }
                })
                .then(data => {
                    suggetionsBox.innerHTML = "";
                    data.fornecedores.forEach(fornecedor => {
                        let newSuggest = document.createElement("div");
                        newSuggest.innerHTML = `${fornecedor.id} - ${fornecedor.name}`
                        suggetionsBox.appendChild(newSuggest);
                        newSuggest.onclick = function(){
                            id_supplier.value = fornecedor.id;
                            input.value = `${fornecedor.id} - ${fornecedor.name}`
                            suggetionsBox.style.display = "none";
                        }
                    });
                });
        }
      
    }
    else{
        suggetionsBox.style.display = "none";
        if(credit){
            credit_value.value = 0;
            credit.style.display = "none";
        }
    }
}

function showSuggetionsPerson(input) {
  const container_td = input.closest('div'); // container do input atual
  let id_client = container_td.querySelector("[name$='person']"); // input hidden que armazena id da pessoa
  let suggestionsBox = container_td.querySelector('.suggetions'); // container para mostrar as sugestões

  // Limpa sugestões e oculta caso input vazio ou muito curto
  if (!input.value || input.value.trim().length < 1) {
    suggestionsBox.innerHTML = "";
    suggestionsBox.style.display = "none";
    return;
  }

  const query = input.value.trim();

  fetch(`/buscar_pessoas/?query=${encodeURIComponent(query)}`)
    .then(response => {
      // Verifica se a resposta é JSON
      const contentType = response.headers.get('Content-Type');
      if (response.ok && contentType && contentType.includes('application/json')) {
        return response.json();
      } else {
        throw new Error('Response is not JSON');
      }
    })
    .then(data => {
      suggestionsBox.innerHTML = "";
      suggestionsBox.style.display = "block"; // mostra sugestões

      if (!data.clientes || data.clientes.length === 0) {
        suggestionsBox.innerHTML = "<div>Nenhum resultado encontrado</div>";
        return;
      }

      data.clientes.forEach(cliente => {
        let newSuggest = document.createElement("div");
        newSuggest.classList.add("suggestion-item"); // opcional para estilizar

        newSuggest.textContent = `${cliente.id} - ${cliente.name}`;

        newSuggest.onclick = function () {
          id_client.value = cliente.id;
          input.value = `${cliente.id} - ${cliente.name}`;
          suggestionsBox.style.display = "none";
        };

        suggestionsBox.appendChild(newSuggest);
      });
    })
    .catch(err => {
      console.error("Erro ao buscar pessoas:", err);
      suggestionsBox.innerHTML = "<div>Erro ao carregar sugestões</div>";
      suggestionsBox.style.display = "block";
    });
}

let preco_data;
function showSuggetionsProducts(input){

    let row = input.closest('tr');
    let container_td = input.closest('td');
    let price = row.cells[2].querySelector('input');
    let discount = row.cells[3].querySelector('input');
    let suggetionsBox = container_td.querySelector('.suggetions');
    let id_product = container_td.querySelector("[name$=product]") || container_td.querySelector("[name$=produto]");
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
                suggetionsBox.innerHTML = "";
                data.produtos.forEach(produto => {
                    let newSuggest = document.createElement("div");
                    newSuggest.innerHTML = `${produto.product_code} - ${produto.description}`;
                    suggetionsBox.appendChild(newSuggest);
                    newSuggest.onclick = function(){
                            id_product.value = produto.id;
                            serviceInput = `${produto.id}`;
                            input.value = `${produto.product_code} - ${produto.description}`;
                            price.value = produto.selling_price;
                            suggetionsBox.style.display = "none";
                            discount.value = 0;
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
    let price = row.cells[3].querySelector('input');
    let suggetionsBox = container_td.querySelector('.suggetions');
    suggetionsBox.innerHTML="";
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
                suggetionsBox.innerHTML = "";
                data.servicos.forEach(servico => {           
                    let newSuggest = document.createElement("div");
                    newSuggest.innerHTML = `${servico.id} - ${servico.name_service}`
                    suggetionsBox.appendChild(newSuggest);
                    console.log("novo servico")
                    console.log(servico)
                    newSuggest.onclick = function(){
                            id_service.value = servico.id;
                            input.value = `${servico.id} - ${servico.name_service}`
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





const totalServicesField = document.getElementById("id_service_total");
const discountTotalField = document.getElementById("id_discount_total_service");
const itemsContainerService = document.getElementById("itens-container-service");

function calcularPreco(input) {
    let row = input.closest("tr"); 
    const itemForms = itemsContainerService.querySelectorAll("table .itens tr");

    let desconto = row.cells[2].querySelector("input").value || 0;

    let precoFinal = preco_data - (preco_data*(desconto/100))
    row.cells[3].querySelector("input").value = precoFinal.toFixed(2);
    
    atualizarTotal(itemForms);
}

const totalValue = document.getElementById("id_totalValue");
const totalValueInput = document.getElementById("id_total_value");
const totalValueField = document.getElementById("id_total_value_service");
document.addEventListener('DOMContentLoaded',()=>{
   
    if(totalValueInput){
        if(!totalValueInput.value){
            totalValueInput.value = 0;
        }
    }
    
    
    if (totalValueField){
        if(!totalValueField.value){
            totalValueField.value = 0;
        }
    }
    
})

function atualizarTotal(itemForms) {
    let totalSemDesconto = 0;
    let totalComDesconto = 0;
    let totalServicos = 0;
    totalValueField.value = 0;
    console.log('entrei aqui senhor')
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



const totalProductsInput = document.getElementById("id_product_total");
const totalDiscountInput = document.getElementById("id_discount_total");
const itemsContainer = document.getElementById("itens-container");

function calcularPrecoProduto(input){

    let row = input.closest("tr");
    const itemForms = itemsContainer.querySelectorAll("table .itens tr");

    let quantidade = row.cells[1].querySelector("input").value || 0;
    let preco = row.cells[2].querySelector("input").value || 0;
    let desconto = row.cells[3].querySelector("input").value || 0;
    let precoFinal = row.cells[4].querySelector("input").value;
    precoFinal = (preco - (desconto/100)*preco)*quantidade;
    row.cells[4].querySelector("input").value = precoFinal;

    atualizarTotalProduto(itemForms);

}



function atualizarTotalProduto(itemForms){
    let totalSemDesconto = 0;
    let totalComDesconto = 0;
    let totalProdutos = 0;
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


function Person(input){
    let container_td = input.closest('td');
    const container = document.getElementById('form-client'); // Onde os forms são inseridos
    let select =  document.getElementById('id_persongroupNomeGrupoPessoasQuantidade_set-__prefix__-person')
    let suggetionsBox = container_td.querySelector('.suggetions');
    let id_client = container_td.querySelector('[name="pessoa"]')
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
            suggetionsBox.innerHTML = "";
            data.clientes.forEach(cliente => {
                let newSuggest = document.createElement("div");
                newSuggest.innerHTML = `${cliente.id} - ${cliente.name}`
                suggetionsBox.appendChild(newSuggest);
                newSuggest.onclick = function(){
                    id_client.value = cliente.id;
                    input.value = `${cliente.id} - ${cliente.name}`
                    suggetionsBox.style.display = "none";
                }
            })
        })
    }
}