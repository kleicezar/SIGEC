
// TOTAL VALOR DE FORMULARIO DE ITENS;

const item_forms = document.querySelectorAll('.item-form');

let index = 0;
item_forms.forEach(itemForm=>{
    let mount = document.getElementById(`id_vendaitem_set-${index}-quantidade`);
    let price = document.getElementById(`id_vendaitem_set-${index}-preco_unitario`);
    let discount = itemForm.querySelector('td .descont');
    let totalValue = itemForm.querySelector('td .totalValue');

    const product_0 = document.getElementById(`id_vendaitem_set-${index}-product`);
    const produtos_0 = document.getElementById(`products-${index}`);
    const idProduct = document.getElementById("idProduct-0");


    // MONITORAR A ALTERAÇÃO DE VALORES PARA MUDAR O VALOR TOTAL
    fieldProducts(produtos_0,idProduct,product_0,price);
    
    

    item = itemForm.querySelector("tbody tr");
    console.log(item);
            
    
    discount.addEventListener("input",()=>{
        if(discount.value != 0){
            totalValue.value = ((price.value - ((discount.value/100) * price.value))*mount.value).toFixed(2);
        } else {
            totalValue.value = (price.value*mount.value).toFixed(2);
        }
    });

    mount.addEventListener("input",()=>{
        if(discount.value != 0){
            totalValue.value = ((price.value - ((discount.value/100) * price.value))*mount.value).toFixed(2);
        } else {
            totalValue.value = (price.value*mount.value).toFixed(2);
        }
    });

    price.addEventListener("input",()=>{
        if(discount.value != 0){
            totalValue.value = ((price.value - ((discount.value/100) * price.value))*mount.value).toFixed(2);
        } else {
            totalValue.value = (price.value*mount.value).toFixed(2);
        }
    })
})

const itemButton = document.getElementById("item");
const itens = [];
itemButton.addEventListener('click',()=>{
    const new_item_forms = document.querySelectorAll('.item-form');
    let index = 0;
    new_item_forms.forEach(itemForm => {
            // MOSTRAS OS PRODUTOS REQUISITADOS
            const product = document.getElementById(`id_vendaitem_set-${index}-product`);
            const produtos = document.getElementById(`products-${index}`);
            const searchProduct = document.getElementById(`idProduct-${index}`)
            // MONITORAR A ALTERAÇÃO DE VALORES PARA MUDAR O VALOR TOTAL
            let discount = itemForm.querySelector("td .descont");
            let totalValue = itemForm.querySelector("td .totalValue");
            let amount = document.getElementById(`id_vendaitem_set-${index}-quantidade`);
            let price = document.getElementById(`id_vendaitem_set-${index}-preco_unitario`);

            index = index + 1;

            discount.addEventListener("input",()=>{
                console.log('OLHA O DESCONTO:',discount.value);
                totalValue.value = ((price.value - (discount.value/100)*price.value)*amount.value).toFixed(2);
            })

            amount.addEventListener("input",()=>{
                console.log('OLHA A QUANTIDADE',amount.value);
                totalValue.value = ( (price.value - (discount.value/100)*price.value)*amount.value).toFixed(2);
            });

            price.addEventListener("input",()=>{
                console.log('OLHA O PRECO',price.value);
                totalValue.value = ( (price.value - (discount.value/100)*price.value)*amount.value).toFixed(2);
            })


            fieldProducts(produtos,searchProduct,product,price);

            
        
        });
        
       
    })


function fieldProducts(produtos,inputSearch,product,price){
    inputSearch.addEventListener("input",()=>{
        if(inputSearch.value.length >=1){
            let id_options = 0;
            const query = inputSearch.value;
            console.log(query);
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
    })
}


// EDIÇÃO DE VENDA, IRÁ INVERTER A LÓGICA - O VALOR DO INPUT DE PESSOA SERÁ USADO PARA PREENCHER O INPUT DE PESQUISA DE PESSOA;
let invertAutoComplete = false;
const id_pessoa = document.getElementById("id_pessoa");
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
let container_options = document.getElementById(`options-1`);

let td_container_options = container_options.parentElement;
td_container_options.style.display = "none";
// FILTRO IRÁ PREENCHER O CAMPO DE PESQUISA E COLOCAR NO VALOR DE PESSOA O SEU ID
input_client.addEventListener("input",()=>{
    td_container_options.style.display="none";
    if ((!invertAutoComplete) || (input_client.value.length >=1 && input_client.value != " ")){
            let id_options = 0;
            const query = input_client.value;
            console.log(input_client.value)
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
                container_options.appendChild(p);
                if(data.clientes.length > 0){
                    data.clientes.forEach(cliente=>{
                        if (data.clientes.length <= query.length){
                            // container_options.style.display="block";
                            td_container_options.style.display = "block"
                            container_options = document.getElementById(`options-1`);

                            selectClient = document.createElement("button");
                            selectClient.className ="btn btn-outline-secondary form-control m-2";
                            selectClient.id = `option-${id_options}`
                            selectClient.textContent= `${cliente.id} - ${cliente.name}`

                            let title_client = document.getElementById("title-client")
                            // container_options.appendChild(selectClient);
                            title_client.insertAdjacentElement('afterend',selectClient)
            
                            const button = document.getElementById(selectClient.id);
                            button.addEventListener("click",()=>{
                                input_client.value = button.textContent ;
                                id_pessoa.value = `${cliente.id}`;
                                console.log(id_pessoa.value);
                                td_container_options.style.display = "none";
                                container_options.innerHTML = "";
                            })
                            id_options+=1;
                        }
                    
                    })
                }
            })
        // }
    }else{
        container_options.innerHTML = '';
        // container_options.style.display="none"
        td_container_options.style.display = "none";
        p.className= "text-center";
        p.textContent = "ID - CLIENTE";
        p.id = "title-client";
        container_options.appendChild(p);
    }
    

    
    

})


