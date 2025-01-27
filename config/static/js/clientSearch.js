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
