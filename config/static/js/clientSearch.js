
// TOTAL VALOR DE FORMULARIO DE ITENS;

const item_forms = document.querySelectorAll('.item-form');
let allTrs = [];
let index = 0;
const payment_value = document.getElementById(`id_paymentmethod_venda_set-${index}-valor`);
const Value = document.querySelector('td .totalValue');
const discount = document.querySelector('td .descont');
const formCountElem = document.getElementById('id_vendaitem_set-TOTAL_FORMS');

const mount = document.getElementById(`id_vendaitem_set-${formCountElem.value - 1}-quantidade`);
let amount = document.getElementById(`id_vendaitem_set-${formCountElem.value - 1}-quantidade`);
let discount_product = document.getElementById(`id_vendaitem_set-${formCountElem.value - 1}-discount`);
let price = document.getElementById(`id_vendaitem_set-${formCountElem.value - 1}-preco_unitario`);
let value_product = document.getElementById(`id_vendaitem_set-${formCountElem.value - 1}-price_total`);



item_forms.forEach(itemForm=>{
    
    let delet = document.querySelector('.delete');
    let mount = document.getElementById(`id_vendaitem_set-${index}-quantidade`);
    let price = document.getElementById(`id_vendaitem_set-${index}-preco_unitario`);
    let discount = itemForm.querySelector('td .descont');
    let totalValue = itemForm.querySelector('td .totalValue');
    
    const product_0 = document.getElementById(`id_vendaitem_set-${index}-product`);
    const produtos_0 = document.getElementById(`products-${index}`);
    const idProduct = document.getElementById(`idProduct-${index}`);
    
    // MONITORAR A ALTERAÇÃO DE VALORES PARA MUDAR O VALOR TOTAL
    fieldProducts(produtos_0,idProduct,product_0,price);

    item = itemForm.querySelector("tbody tr");
    
    if (discount_product){
        discount_product.addEventListener("input",()=>{
            if(discount_product.value != 0){
                value_product.value = ((price.value - ((discount_product.value/100) * price.value))*mount.value).toFixed(2);
            } else {
                value_product.value = (price.value*mount.value).toFixed(2);
            }
        });
    }
    mount.addEventListener("input",()=>{
        if(discount_product.value != 0){
            value_product.value = ((price.value - ((discount_product.value/100) * price.value))*mount.value).toFixed(2);
        } else {
            value_product.value = (price.value*mount.value).toFixed(2);
        }
    });
    
    price.addEventListener("input",()=>{
        if(discount_product.value != 0){
            value_product.value = ((price.value - ((discount_product.value/100) * price.value))*mount.value).toFixed(2);
        } else {
            value_product.value = (price.value*mount.value).toFixed(2);
        }
    })
})

const itemButton = document.getElementById("item");
const itens = [];

itemButton.addEventListener('click',()=>{
// function click(()=>{
    // let index = 0;
    const new_item_forms = document.querySelectorAll('.item-form');
    new_item_forms.forEach(itemForm => {
        // MOSTRAS OS PRODUTOS REQUISITADOS
            const product = document.getElementById(`id_vendaitem_set-${formCountElem.value - 1}-product`);
            const produtos = document.getElementById(`products-${formCountElem.value - 1}`);
            const searchProduct = document.getElementById(`idProduct-${formCountElem.value - 1}`)
            // MONITORAR A ALTERAÇÃO DE VALORES PARA MUDAR O VALOR TOTAL
            let discount = itemForm.querySelector("td .descont");
            let totalValue = itemForm.querySelector("td .totalValue");
            let amount = document.getElementById(`id_vendaitem_set-${formCountElem.value - 1}-quantidade`);
            let discount_product = document.getElementById(`id_vendaitem_set-${formCountElem.value - 1}-quantidade`);
            let price = document.getElementById(`id_vendaitem_set-${formCountElem.value - 1}-preco_unitario`);
            
            index = index + 1 ;
         
            if (discount_product){
                discount_product.addEventListener("input",()=>{
                    console.log('OLHA O DESCONTO:',discount_product.value);
                    totalValue.value = ((price.value - (discount_product.value/100)*price.value)*amount.value).toFixed(2);
                })
            }
            if (amount){
                amount.addEventListener("input",()=>{
                    console.log('OLHA A QUANTIDADE',amount.value);
                    totalValue.value = ( (price.value - (discount.value/100)*price.value)*amount.value).toFixed(2);
                });
            }    
            if (price){
                price.addEventListener("input",()=>{
                    console.log('OLHA O PRECO',price.value);
                    totalValue.value = ( (price.value - (discount.value/100)*price.value)*amount.value).toFixed(2);
                })
            }
            fieldProducts(produtos,searchProduct,product,price,discount_product,amount);

            
            // DELETAR UM ITEM 
            // delet.addEventListener("click",()=>{
                // console.log(delet);
            //     item = itemForm.querySelector("tbody tr");
            //     item.innerHTML = ' ';
                // console.log(item)
            // })
            
            // }
            
        });
        
        
    })
     
function fieldProducts(produtos,inputSearch,product,price){
    inputSearch.addEventListener("input",()=>{
        let amount = document.getElementById(`id_vendaitem_set-${formCountElem.value - 1}-quantidade`);
        let discount_product = document.getElementById(`id_vendaitem_set-${formCountElem.value - 1}-discount`);
        let value_product = document.getElementById(`id_vendaitem_set-${formCountElem.value - 1}-price_total`);
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
                                inputSearch.value = button.textContent;
                                produtos.innerHTML = "";
                                price.value = produto.selling_price;
                                discount_product.value = 0;
                                amount.value = 1;
                                value_product.value = produto.selling_price
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
    })
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

// FILTRO IRÁ PREENCHER O CAMPO DE PESQUISA E COLOCAR NO VALOR DE PESSOA O SEU ID
input_client.addEventListener("input",()=>{

    let container_options = document.getElementById(`options-1`);
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
                if(data.clientes.length > 0){
                    data.clientes.forEach(cliente=>{
                        if (data.clientes.length <= query.length){
                            container_options = document.getElementById(`options-1`);

                            selectClient = document.createElement("button");
                            selectClient.className ="btn btn-outline-secondary form-control";
                            selectClient.id = `option-${id_options}`
                            selectClient.textContent= `${cliente.id} - ${cliente.name}`
                            container_options.appendChild(selectClient);
            
                            const button = document.getElementById(selectClient.id);
                            button.addEventListener("click",()=>{
                                input_client.value = button.textContent ;
                                id_pessoa.value = `${cliente.id}`;
                                // console.log(id_pessoa.value);
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
    // console.log(teste.value)
// })



// $(document).ready(function() {
//     $('#nome_pesquisa').on('keyup', function() {
//         let nome = $(this).val();
        // console.log(nome);

//         if (nome.length >= 2) {
//             $.ajax({
//                 url: "buscar_pessoas",
//                 data: { 'pessoa': nome },
//                 dataType: 'json',
//                 success: function(response) {
//                     const pessoas = response.pessoas;
                    // console.log(pessoas);
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
                    // console.error('Erro na requisição:', error);
//                     alert('Ocorreu um erro ao buscar os usuários.');
//                 }
//             });
//         } else {
//             $('#suggestions').hide();
//         }
//     });
// });

