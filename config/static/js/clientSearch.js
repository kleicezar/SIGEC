
// TOTAL VALOR DE FORMULARIO DE ITENS;
const total = document.getElementById("id_total_value");
const totalProducts = document.getElementById("id_product_total");
const discountTotal = document.getElementById("id_discount_total");
const itens_container = document.getElementById("itens-container");
let p_2 = document.createElement("p");
let container_options_2 = document.getElementById("options_products-0")
let td_container_options_2 = container_options_2.parentElement;
td_container_options_2.style.display = "none";  
const p_product = document.createElement("p");

// let container_options_item = document.getElementById("")
document.addEventListener("focusin",(event)=>{
    // pra uma caixa de sugestões nao sobrepor a outra
    if(event.target.tagName ==="INPUT" ){
        // const inputFocus = event.target.id;
        // if(inputFocus.startsWith("idProduct")){
            document.querySelectorAll(".suggest").forEach(el=>el.style.display="none");
        // }
    }
})


itens_container.addEventListener("click",(event)=>{
    if(event.target.tagName === 'BUTTON'){
        const item_forms = itens_container.querySelectorAll(".item-form");
        Total(item_forms);
    }
})
itens_container.addEventListener("input",(event)=>{
    if(event.target.tagName==='INPUT'){
        const item_forms = itens_container.querySelectorAll(".item-form");
        const inputModificado = event.target;
        const item_form = inputModificado.closest(".item-form");
        const inputs_item_form = item_form.querySelectorAll("input");
        let product_value;
        let quantidade_value;
        let descont_value;
        let price_total_value;
        let price_unit_value ;
        let search_p;
        inputs_item_form.forEach((input)=>{
            const type_field = input.id;            
            if(type_field.endsWith('product') || type_field.endsWith('produto')){
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
            let tbody = inputModificado.parentElement.parentElement.parentElement;
            let td = tbody.querySelector(".tre").querySelector("td");
    
            let products = td.querySelector("div");
          
            if(inputModificado.value.length>=1){
                let idoptions = 0;
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
                products.innerHTML="";
                p_product.textContent = "COD - DESC";
                p_product.className="title-product text-center";
                products.style.width = "300px";
                products.appendChild(p_product)


                if(data.produtos.length>0){    
                    data.produtos.forEach(produto=>{
                        td.style.display="block";
                        let selectProduct = document.createElement("button");
                        selectProduct.className = "btn btn-outline-secondary form-control x mb-2";
                        selectProduct.type="button";
                        selectProduct.id = `option-product-${idoptions}`;

                        selectProduct.textContent = `${produto.product_code} - ${produto.description}`
                        let title_product = td.querySelector(".title-product");

                        title_product.insertAdjacentElement('afterend',selectProduct);
                    const button = td.querySelector(".x")
                
                        button.addEventListener("click",()=>{
                            product_value.value = produto.id;
                            search_p.value = button.textContent;
                            price_unit_value.value = produto.selling_price;
                            td.style.display = "none";  
                        })
                        idoptions+=1;
                    })
                }
                else if(data.produtos.length == query.length){
                    price_unit_value = produto.selling_price;
                }
            })
            } else {
                td.style.display ="none";
            }
            
        } 
        if(descont_value != undefined && quantidade_value!=undefined && price_unit_value!=undefined){
          
            if(descont_value.value != 0){
                price_total_value.value = ((price_unit_value.value - ((descont_value.value/100) * price_unit_value.value))*quantidade_value.value).toFixed(2);
            } else {
                price_total_value.value = (price_unit_value.value*quantidade_value.value).toFixed(2);
            }
            
        }
        let n_produtos = 0;
        let totalPrice = 0;
        let totalValue = 0;
        // function item(){
        // item_forms.forEach(item_form_array=>{
        //     let quanti = 0;
        //     let preco = 0;
        //     const inputs = item_form_array.querySelectorAll("input");
        //     // const divs = item_form_array.querySelectorAll("div");
        //     inputs.forEach(input=>{
        //         if(input.id.endsWith("quantidade")){
        //             n_produtos = Number(input.value) + n_produtos;
        //             quanti = input.value;
        //             totalValue = totalValue + preco*Number(quanti);
        //         }
        //         else if(input.id.endsWith("price_total")){
        //             totalPrice = totalPrice + Number(input.value);
        //         }
        //         else if(input.id.endsWith("preco_unitario")){
        //             preco = input.value;
        //             totalValue = totalValue + Number(preco)*quanti;
        //         }

        //     })
        //     valor_discontado = total - totalValue;
        //     percentual_disconto = (valor_discontado/total)*100;
        //     discountTotal.value = 11;
        //     totalProducts.value = n_produtos;
        //     total.value = totalPrice;
        // })
        Total(item_forms);
      
    }
})

function Total(item_forms,n_produtos=0,totalPrice=0,totalValue=0){
    item_forms.forEach(item_form_array=>{
        let quanti = 0;
        let preco = 0;
        inpt = item_form_array.querySelectorAll("input");

        inpt.forEach(input=>{
            if(input.id.endsWith("quantidade")){
                n_produtos = Number(input.value) + n_produtos;
                quanti = input.value;
                totalValue = totalValue + preco*Number(quanti);
            }
            else if(input.id.endsWith("price_total")){
                totalPrice = totalPrice + Number(input.value);
            }
            else if(input.id.endsWith("preco_unitario")){
                preco = input.value;
                totalValue = totalValue + Number(preco)*quanti;
            }
        })
        valor_discontado = total - totalValue;
        discountTotal.value = 11;
        totalProducts.value = n_produtos;
        total.value = totalPrice;
    })

}
const item_forms = document.querySelectorAll('.item-form');

let index = 0;


// EDIÇÃO DE VENDA, IRÁ INVERTER A LÓGICA - O VALOR DO INPUT DE PESSOA SERÁ USADO PARA PREENCHER O INPUT DE PESQUISA DE PESSOA;
let invertAutoComplete = false;
const id_pessoa = document.getElementById("id_pessoa") || document.getElementById("id_fornecedor");

const input_client = document.getElementById("idSearch");
// const input_mount = document.getElementById("idSearch");

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
            
            mount.value = '1'
            
        })
        
        
    })
    if (mount) {
        mount.value = '1';
    } else {
        // console.error('Elemento "mount" não encontrado.');
    }
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

    console.log(td_container_options)
    if ((!invertAutoComplete) || (input_client.value.length >=1 && input_client.value != " ")){
            let id_options = 0;
            const query = input_client.value;
            // console.log(input_client.value)
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
                            selectClient.type="button";

                            let title_client = document.getElementById("title-client")
                            title_client.insertAdjacentElement('afterend',selectClient)
            
                            const button = document.getElementById(selectClient.id);
                            button.addEventListener("click",()=>{
                                input_client.value = button.textContent ;
                                console.log('--')
                                console.log(input_client)
                                id_pessoa.value = `${cliente.id}`;
                                td_container_options.style.display="none";
                            })
                            id_options+=1;
                        }
                    })
                }
            })
        // }
    }else{
        td_container_options.style.display="none";
    }
    

    
    

})



