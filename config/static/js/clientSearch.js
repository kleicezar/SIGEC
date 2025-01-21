
// TOTAL VALOR DE FORMULARIO DE ITENS;
const total = document.getElementById("id_total_value")
const totalProducts = document.getElementById("id_product_total");
const discountTotal = document.getElementById("id_discount_total");
const itens_container = document.getElementById("itens-container");
let p_2 = document.createElement("p");
let container_options_2 = document.getElementById("options-item-2")
let td_container_options_2 = container_options_2.parentElement;
td_container_options_2.style.display = "none";
// let container_options_item = document.getElementById("")
itens_container.addEventListener("input",(event)=>{
    if(event.target.tagName==='INPUT'){
        const item_forms = itens_container.querySelectorAll(".item-form");
        // const discounts = itens_container.querySelectorAll('input[type="text"][name$="-discount"]');
        let n_produtos = 0;
        let totalPrice = 0;
        let totalValue = 0;
        function item(){
            item_forms.forEach(item_form_array=>{
                let quanti = 0;
                let preco = 0;
                const inputs = item_form_array.querySelectorAll("input");
                // const divs = item_form_array.querySelectorAll("div");
                inputs.forEach(input=>{
                    if(input.id.endsWith("quantidade")){
                        n_produtos = Number(input.value) + n_produtos;
                        quanti = input.value;
                        totalValue = totalValue + preco*Number(quanti);
                    }
                    else if(input.id.endsWith("price_total")){
                        totalPrice = totalPrice + Number(input.value);
                        preco = input.value;
                    }
                    else if(input.id.endsWith("preco_unitario")){
                        preco = input.value;
                        totalValue = totalValue + Number(preco)*quanti;
                    }
                    console.log(totalValue)
                })
                valor_discontado = total - totalValue;
                percentual_disconto = (valor_discontado/total)*100;
                discountTotal.value = 11;
                totalProducts.value = n_produtos;
                total.value = totalPrice;
            })
        }
        item();
        const inputModificado = event.target;
        const item_form = inputModificado.closest(".item-form");
        const inputs_item_form = item_form.querySelectorAll("input");
        let product_value;
        let quantidade_value;
        let descont_value;
        let price_total_value;
        let price_unit_value ;
        let search_p;
        const list_products = item_form.querySelector("table tbody tr td .field-product");
        inputs_item_form.forEach((input)=>{
            const type_field = input.id;
            if(type_field.endsWith('product')){
                product_value = input;

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
            else if(type_field.startsWith("idProduct")){
                search_p = input;
            }
            
        })
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
                            price_unit_value.value = produto.selling_price;
                            list_products.innerHTML="";
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
        if(descont_value != undefined && quantidade_value!=undefined && price_unit_value!=undefined){
          
            if(descont_value.value != 0){
                price_total_value.value = ((price_unit_value.value - ((descont_value.value/100) * price_unit_value.value))*quantidade_value.value).toFixed(2);
            } else {
                price_total_value.value = (price_unit_value.value*quantidade_value.value).toFixed(2);
            }
            
        }
        
      
    }
})
const item_forms = document.querySelectorAll('.item-form');

let index = 0;


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



