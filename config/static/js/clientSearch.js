
// TOTAL VALOR DE FORMULARIO DE ITENS;
const itens_container = document.getElementById("itens-container");
itens_container.addEventListener("input",(event)=>{
    if(event.target.tagName==='INPUT'){
        const inputModificado = event.target;
        console.log(inputModificado)
        const item_form = inputModificado.closest(".item-form");
        const inputs_item_form = item_form.querySelectorAll("input");
        let product_value;
        let quantidade_value;
        let descont_value;
        let price_total_value;
        let price_unit_value ;
        
        let search_p;
        // search_p = item_form.
        const list_products = item_form.querySelector("table tbody tr td .field-product");
        if (inputModificado.id.startsWith("idProduct")){
            if(inputModificado.value.length>=1){
                let id_options = 0;
                const query = inputModificado.value;
                fetch(`/buscar_produtos/?query=${encodeURIComponent(query)}`)
                .then(response=>{
                if(response.ok && response.headers.get('Content-Type').includes('application/json')){
                    return response.json();
                }
                else {
                    throw new Error('Resposta não é JSON');
                }
            })
            .then(data=>{
                list_products.innerHTML = " ";
                console.log(data);
                if(data.produtos.length>0){    
                    data.produtos.forEach(produto=>{
                        let selectProduct = document.createElement("button");
                        selectProduct.className = "btn btn-outline-secondary form-control";
                        selectProduct.type="button";
                        selectProduct.id = `option-${id_options}`;

                        selectProduct.textContent = `${produto.product_code} - ${produto.description}`
                        list_products.appendChild(selectProduct);

                        const button = document.getElementById(selectProduct.id);
                        button.addEventListener("click",()=>{
                            product_value.value = produto.id;
                            search_p.value = button.textContent;
                            list_products.innerHTML="";
                            price_unit_value.value = produto.selling_price;
                
                        })
                    })
                }
                else if(data.produtos.length == query.length){
                    price_unit_value = produto.selling_price;
                }
            })
            } else {
                list_products.innerHTML = " ";
            }
            
        } 
        inputs_item_form.forEach((input)=>{
            const type_field = input.id;
            if(type_field.endsWith('product')){
                product_value = input;
                // console.log(product_value);

            }
            else if (type_field.endsWith('quantidade')){
                quantidade_value = input;
            }
            else if(type_field.endsWith('preco_unitario')){
                price_unit_value = input;
            }
            else if (type_field.endsWith('discount')){
                descont_value = input;
            }
            else if(type_field.endsWith('price_total')){
                price_total_value = input;
            }
            else{
                search_p = input;// id-product
            }
            
        })
      
    }
})
const item_forms = document.querySelectorAll('.item-form');

let index = 0;
// item_forms.forEach(itemForm=>{
//     let mount = document.getElementById(`id_vendaitem_set-${index}-quantidade`);
//     let price = document.getElementById(`id_vendaitem_set-${index}-preco_unitario`);
//     let discount = itemForm.querySelector('td .descont');
//     let totalValue = itemForm.querySelector('td .totalValue');

//     const product_0 = document.getElementById(`id_vendaitem_set-${index}-product`);
//     const produtos_0 = document.getElementById(`products-${index}`);
//     const idProduct = document.getElementById("idProduct-0");


//     // MONITORAR A ALTERAÇÃO DE VALORES PARA MUDAR O VALOR TOTAL
//     fieldProducts(produtos_0,idProduct,product_0,price);
    
    

//     item = itemForm.querySelector("tbody tr");
//     console.log(item);
            
    
//     discount.addEventListener("input",()=>{
//         if(discount.value != 0){
//             totalValue.value = ((price.value - ((discount.value/100) * price.value))*mount.value).toFixed(2);
//         } else {
//             totalValue.value = (price.value*mount.value).toFixed(2);
//         }
//     });

//     mount.addEventListener("input",()=>{
//         if(discount.value != 0){
//             totalValue.value = ((price.value - ((discount.value/100) * price.value))*mount.value).toFixed(2);
//         } else {
//             totalValue.value = (price.value*mount.value).toFixed(2);
//         }
//     });

//     price.addEventListener("input",()=>{
//         if(discount.value != 0){
//             totalValue.value = ((price.value - ((discount.value/100) * price.value))*mount.value).toFixed(2);
//         } else {
//             totalValue.value = (price.value*mount.value).toFixed(2);
//         }
//     })
// })

// const itemButton = document.getElementById("item");

// itemButton.addEventListener('click',()=>{
//     const new_item_forms = document.querySelectorAll('.item-form');
//     let index = 0;
//     new_item_forms.forEach(itemForm => {
//             // MOSTRAS OS PRODUTOS REQUISITADOS
//             const product = document.getElementById(`id_vendaitem_set-${index}-product`);
//             const produtos = document.getElementById(`products-${index}`);
//             const searchProduct = document.getElementById(`idProduct-${index}`);
//             // MONITORAR A ALTERAÇÃO DE VALORES PARA MUDAR O VALOR TOTAL
//             let discount = itemForm.querySelector("td .descont");
//             let totalValue = itemForm.querySelector("td .totalValue");
//             let amount = document.getElementById(`id_vendaitem_set-${index}-quantidade`);
//             let price = document.getElementById(`id_vendaitem_set-${index}-preco_unitario`);

//             index = index + 1;

//             discount.addEventListener("input",()=>{
//                 console.log('OLHA O DESCONTO:',discount.value);
//                 totalValue.value = ((price.value - (discount.value/100)*price.value)*amount.value).toFixed(2);
//             })

//             amount.addEventListener("input",()=>{
//                 console.log('OLHA A QUANTIDADE',amount.value);
//                 totalValue.value = ( (price.value - (discount.value/100)*price.value)*amount.value).toFixed(2);
//             });

//             price.addEventListener("input",()=>{
//                 console.log('OLHA O PRECO',price.value);
//                 totalValue.value = ( (price.value - (discount.value/100)*price.value)*amount.value).toFixed(2);
//             })


//             fieldProducts(produtos,searchProduct,product,price);

            
        
//         });
        
       
//     })


function fieldProducts(produtos,inputSearch,product,price){
    inputSearch.addEventListener("input",()=>{
        if(inputSearch.value.length >=1){
            let id_options = 0;
            const query = inputSearch.value;
            fetch(`/buscar_produtos/?query=${encodeURIComponent(query)}`)
            .then(response=>{
                if(response.ok && response.headers.get('Content-Type').includes('application/json')){
                    return response.json();
                }
                else {
                    throw new Error('Resposta não é JSON');
                }
            })
            .then(data=>{
                produtos.innerHTML = " ";
                if(data.produtos.length > 0){
                    data.produtos.forEach(produto=>{
                        if (data.produtos.length <= query.length){
                            selectProduct = document.createElement("button");
                            selectProduct.className = "btn btn-outline-secondary form-control";
                            selectProduct.id = `option-${id_options}`;
    
                            selectProduct.textContent = `${produto.product_code} - ${produto.description}`;

                            produtos.appendChild(selectProduct);
    
                            const button = document.getElementById(selectProduct.id);
                            button.addEventListener("click",()=>{
                                product.value = produto.id;
                                console.log(product.value);
                                inputSearch.value = button.textContent;
                                produtos.innerHTML = "";
                                price.value = produto.cost_of_product;
                                

                            })
                            id_options+=1;
                        }
                        else if (data.produtos.length == query.length){
                            price.value = produto.cost_of_product
                        }
                       
                    })
                
                }
            }) 
        } else {
            produtos.innerHTML = " ";
        }
    }
)
}


// EDIÇÃO DE VENDA, IRÁ INVERTER A LÓGICA - O VALOR DO INPUT DE PESSOA SERÁ USADO PARA PREENCHER O INPUT DE PESQUISA DE PESSOA;
let invertAutoComplete = false;
const id_pessoa = document.getElementById("id_pessoa") || document.getElementById("id_fornecedor");
const input_client = document.getElementById("idSearch");
// const input_mount = document.getElementById("idSearch");

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
            mount.value = '1'
            
        })
        
    })
    if (mount) {
        mount.value = '1';
    } else {
        // console.error('Elemento "mount" não encontrado.');
    }
}

let p = document.createElement("p");
let container_options = document.getElementById(`options-1`);

let td_container_options = container_options.parentElement;
td_container_options.style.display = "none";

// FILTRO IRÁ PREENCHER O CAMPO DE PESQUISA E COLOCAR NO VALOR DE PESSOA O SEU ID
input_client.addEventListener("input",()=>{
    td_container_options.style.display="none";
    if ((!invertAutoComplete) || (input_client.value.length >=1 && input_client.value != " ")){
            let id_options = 0;
            const query = input_client.value;
            // console.log(input_client.value)
            fetch(`/buscar_pessoas/?query=${encodeURIComponent(query)}`)
            .then(response=>{
                if (response.ok && response.headers.get('Content-Type').includes('application/json')) {
                    return response.json();
                } else {
                    throw new Error('Resposta não é JSON');
                }
            })
            .then(data=>{
                container_options.innerHTML = '';
                p.textContent = "ID - CLIENTE";
                p.id = "title-client";
                p.className= "text-center";
                container_options.style.width = "300px";
                container_options.appendChild(p);
                if(data.clientes.length > 0){
                    data.clientes.forEach(cliente=>{
                        if (data.clientes.length <= query.length){
                            td_container_options.style.display = "block";
                            container_options = document.getElementById(`options-1`);

                            selectClient = document.createElement("button");
                            selectClient.className ="btn btn-outline-secondary form-control mb-2";
                            selectClient.id = `option-${id_options}`
                            selectClient.textContent= `${cliente.id} - ${cliente.name}`

                            let title_client = document.getElementById("title-client")
                            title_client.insertAdjacentElement('afterend',selectClient)
            
                            const button = document.getElementById(selectClient.id);
                            button.addEventListener("click",()=>{
                                input_client.value = button.textContent ;
                                id_pessoa.value = `${cliente.id}`;
                                console.log(id_pessoa.value);
                                container_options.innerHTML = "";
                            })
                            id_options+=1;
                        }
                    })
                }
            })
        // }
    }else{
        container_options.innerHTML = ''
    }
    

    
    

})



// teste = document.getElementById("id_paymentmethod_venda_set-0-DELETE");
// console.log(teste.value)
// teste.addEventListener("click",()=>{
//     console.log(teste.value)
// })



// $(document).ready(function() {
//     $('#nome_pesquisa').on('keyup', function() {
//         let nome = $(this).val();
//         console.log(nome);

//         if (nome.length >= 2) {
//             $.ajax({
//                 url: "buscar_pessoas",
//                 data: { 'pessoa': nome },
//                 dataType: 'json',
//                 success: function(response) {
//                     const pessoas = response.pessoas;
//                     console.log(pessoas);
//                     const $resultados = $('#suggestions');
//                     $resultados.empty();

//                     if (pessoas.length > 0) {
//                         pessoas.forEach(pessoa => {
//                             $resultados.append(`<li>${pessoa.WorkPhone}</li>`);
//                         });
//                     } else {
//                         $resultados.append('<li>Nenhum usuário encontrado.</li>');
//                     }

//                     // Exibe as sugestões se houver resultados
//                     $resultados.show();
//                 },
//                 error: function(xhr, status, error) {
//                     console.error('Erro na requisição:', error);
//                     alert('Ocorreu um erro ao buscar os usuários.');
//                 }
//             });
//         } else {
//             $('#suggestions').hide();
//         }
//     });
// });

