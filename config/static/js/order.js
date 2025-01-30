
// TOTAL VALOR DE FORMULARIO DE ITENS;
const id_total_value = document.getElementById("id_total_value");
const id_total_products = document.getElementById("id_service_total");
const id_discount_total = document.getElementById("id_discount_total");
const itens_container = document.getElementById("itens-container");



let container_options_products = document.getElementById("options_services-0")
let td_container_options_products = container_options_products.parentElement;
td_container_options_products.style.display = "none";  
const p_product = document.createElement("p");


document.querySelectorAll(".suggest").forEach(el=>el.style.display="none");
// let container_options_item = document.getElementById("")
document.addEventListener("focusin",(event)=>{
    // pra uma caixa de sugestões nao sobrepor a outra
    if(event.target.tagName ==="INPUT" ){
        // const inputFocus = event.target.id;
            document.querySelectorAll(".suggest").forEach(el=>el.style.display="none");
    }
})

// ATUALIZA O TOTAL DO DESCONTO, VALOR TOTAL, E TOTAL DE PRODUTOS  AO CLICAR NO BOTÃO DELETAR
itens_container.addEventListener("click",(event)=>{
    if(event.target.tagName === 'BUTTON'){
        const item_forms = itens_container.querySelectorAll(".item-form");
        total(item_forms);
    }
})


itens_container.addEventListener("input",(event)=>{
    if(event.target.tagName==='INPUT'){

        const item_forms = itens_container.querySelectorAll(".item-form");
        const inputModificado = event.target;
        const item_form = inputModificado.closest(".item-form");
        const inputs_item_form = item_form.querySelectorAll("input");


        //MONITORA O CAMPO ID_PRODUCT
        if (inputModificado.id.startsWith("idService")){
            let tbody = inputModificado.parentElement.parentElement.parentElement;
    

            let td = tbody.querySelector(".tre").querySelector("td");
    

            let products = td.querySelector("div");


            let product_value;
            let search_p;

            inputs_item_form.forEach((input)=>{
                const type_field = input.id;
                if(type_field.endsWith('service')){
                    product_value = input;
                }
                else if(type_field.startsWith("idService")){
                    search_p = input;
                }
                else if(type_field.endsWith('preco')){
                    price_unit_value = input;
                    
                    console.log('opa')
                }
            })
            if(inputModificado.value.length>=1){
                let idoptions = 0;


                const query = inputModificado.value;
                fetch(`/buscar_servicos/?query=${encodeURIComponent(query)}`)
                .then(response=>{
                if(response.ok && response.headers.get('Content-Type').includes('application/json')){
                    return response.json();
                }
                else {
                    throw new Error('Resposta não é JSON');
                }
                
            })
            .then(data=>{
                products.innerHTML="";
                p_product.textContent = "ID - NOME"
                p_product.className="title-service text-center"
                products.style.width = "300px";
                products.appendChild(p_product)

                if(data.servicos.length>0){
                    data.servicos.forEach(servico=>{
                

                        td.style.display="block";
                        let selectProduct = document.createElement("button");
                        console.log(selectProduct)
                        selectProduct.className = "btn btn-outline-secondary form-control x mb-2";
                        selectProduct.type="button";
                        selectProduct.id = `option-service-${idoptions}`;

                        selectProduct.textContent = `${servico.id} - ${servico.name_Service}`;
                        let title_product = td.querySelector('.title-service');
                        

                        title_product.insertAdjacentElement('afterend',selectProduct);
                        
                        const button = td.querySelector(".x")


                        button.addEventListener("click",()=>{
                            product_value.value = servico.id;
                            search_p.value = button.textContent;
                            console.log(price_unit_value.value)
                            price_unit_value.value = servico.price;

                            td.style.display = "none";
                        })
                        idoptions+=1;
                    })
                }
            })
    
            } else {
                td.style.display ="none";
            }
            
        } 
        
        total(item_forms);
      
    }
})


function total(item_forms,n_servicos=0,totalPrice=0,totalValue=0){
    item_forms.forEach(item_form=>{
        const style = window.getComputedStyle(item_form);
        let quanti = 0;
        let preco = 0;
        inpt = item_form.querySelectorAll("input");
        if (style.display !== 'none') {
            // Só execute o código se o elemento não estiver com display: none
            // Sua lógica aqui
            inpt.forEach(input=>{
                if(input.id.endsWith("quantidade")){
                    n_servicos = Number(input.value) + n_servicos;
                    quanti = input.value;
                    totalValue = totalValue + preco*Number(quanti);
                }
                else if(input.id.endsWith("preco")){
                    preco = input.value;
                    totalValue = totalValue + Number(preco)*quanti;
                }
            })
        }
       
        // valor_discontado = total - totalValue;
        id_discount_total.value = 11;
        id_total_products.value = n_servicos;
        id_total_value.value = totalPrice;
    })

}
const item_forms = document.querySelectorAll('.item-form');

let index = 0;


// EDIÇÃO DE VENDA, IRÁ INVERTER A LÓGICA - O VALOR DO INPUT DE PESSOA SERÁ USADO PARA PREENCHER O INPUT DE PESQUISA DE PESSOA;
let invertAutoComplete = false;
const id_pessoa = document.getElementById("id_pessoa") || document.getElementById("id_fornecedor");
const input_products = document.querySelectorAll('input[type="hidden"][name$="-product"]');

input_products.forEach(input_product=>{
    let x = input_product.parentElement;
    console.log('uepad')
    let input_text = x.querySelector('input[type="text"]')

    // let d = document.getElementById(input_text);
    if(input_product.value!==''){
       
        const query = input_product.value;
        fetch(`/get_product_id/?query=${encodeURIComponent(query)}`)
        .then(response=>{
            if (response.ok && response.headers.get('Content-Type').includes('application/json')) {
                return response.json();
            } else {
                throw new Error('Resposta não é JSON');
            }
        })
        .then(data=>{
            console.log(data)
            input_text.value =`${data.produto[0].product_code} - ${data.produto[0].description}`
            console.log(data.produto[0].description)
            
           
        })    
    }
})

const input_client = document.getElementById("idSearch");


if(id_pessoa.value!=""){

    invertAutoComplete = !invertAutoComplete;
}

if(invertAutoComplete){
    anotherQuery = id_pessoa.value;
    //MUDAR ISSO PARA BUSCA POR ID;
    fetch(`/buscar_pessoas/?query=${encodeURIComponent(anotherQuery)}`)
    .then(response=>{
        if (response.ok && response.headers.get('Content-Type').includes('application/json')) {
            return response.json();
        } else {
            throw new Error('Resposta não é JSON');
        }
    })
    .then(data=>{
        data.clientes.forEach(cliente=>{
            input_client.value = `${cliente.id} - ${cliente.name}`
        })
        
        
    })
    
}

let p = document.createElement("p");
let container_options_client = document.getElementById(`options-1`);

let td_container_options_client = container_options_client.parentElement;
td_container_options_client.style.display = "none";

// FILTRO IRÁ PREENCHER O CAMPO DE PESQUISA E COLOCAR NO VALOR DE PESSOA O SEU ID
input_client.addEventListener("input",()=>{
    td_container_options_client.style.display="none";

    if ( (input_client.value.length >=1 && input_client.value != " ")){
            let id_options = 0;
            const query = input_client.value;
            fetch(`/buscar_pessoas/?query=${encodeURIComponent(query)}`)
            .then(response=>{
                if (response.ok && response.headers.get('Content-Type').includes('application/json')) {
                    return response.json();
                } else {
                    throw new Error('Resposta não é JSON');
                }
            })
            .then(data=>{
                container_options_client.innerHTML = '';
                p.textContent = "ID - CLIENTE";
                p.id = "title-client";
                p.className= "text-center";
                container_options_client.style.width = "300px";
                container_options_client.appendChild(p);
                if(data.clientes.length > 0){
                    data.clientes.forEach(cliente=>{
                        if (data.clientes.length <= query.length){
                            td_container_options_client.style.display = "block";
                            container_options_client = document.getElementById(`options-1`);

                            selectClient = document.createElement("button");
                            selectClient.className ="btn btn-outline-secondary form-control mb-2";
                            selectClient.id = `option-${id_options}`
                            selectClient.textContent= `${cliente.id} - ${cliente.name}`
                            selectClient.type="button";

                            let title_client = document.getElementById("title-client")
                            title_client.insertAdjacentElement('afterend',selectClient)
            
                            const button = document.getElementById(selectClient.id);
                            button.addEventListener("click",()=>{

                                input_client.value = button.textContent ;
                                id_pessoa.value = `${cliente.id}`;
                                td_container_options_client.style.display="none";
                            })

                            id_options+=1;
                        }
                    })
                }
            })
        // }
    }else{
        td_container_options_client.style.display="none";
    }
})









// document.addEventListener("DOMContentLoaded", function () {
//     let container = document.querySelector("#itens-container"); // O container que contém todos os item-form
//     if (container) {
//         // Monitorar mudanças nos selects dentro do container
//         container.addEventListener("change", function (event) {
//             if (event.target.matches("[id^='id_vendaitemservice_set-'][id$='-service']")) {
//                 let selectElement = event.target;
//                 let formContainer = selectElement.closest(".item-form"); // Encontra o item-form mais próximo
                
//                 if (formContainer) {
//                     let precoInput = formContainer.querySelector("[id^='id_vendaitemservice_set-'][id$='-preco']");
//                     let serviceInput = formContainer.querySelector("[id^='id_vendaitemservice_set-'][id$='-service']")
//                     const teste = serviceInput.textContent;
//                     console.log(serviceInput.textContent)
//                     fetch(`/buscar_servicos/?query=${encodeURIComponent(teste)}`)
//                     .then(response=>{
//                         if (response.ok && response.headers.get('Content-Type').includes('application/json')) {
                            
//                             return response.json();
                            
//                         } else {
//                             throw new Error('Resposta não é JSON');
//                         }
                        
//                     })
//                     .then(data=>{
//                         if (precoInput) {
//                             precoInput.value = data.servico[0].value_Service // Define ou limpa o valor
//                         }
//                     })
                    
//                 }
//             }
//         });

//         // Monitorar cliques nos botões de deletar dentro do container
//         container.addEventListener("click", function (event) {
//             if (event.target.matches(".delete")) {
//                 let button = event.target;
//                 let formContainer = button.closest(".item-form"); // Encontra o item-form mais próximo
                
//                 if (formContainer) {
//                     console.log('uep')
//                     let precoInput = formContainer.querySelector("[id^='id_vendaitemservice_set-'][id$='-DELETE']");
//                     console.log(precoInput)
//                     if (precoInput) {
//                         precoInput.value = "on"; // Altera o preço para "urro" ao deletar
//                         console.log(precoInput.value)
//                     }
//                 }
//             }
//         });
//     }
// });

