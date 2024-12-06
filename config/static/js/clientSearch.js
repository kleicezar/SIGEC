
// TOTAL VALOR DE FORMULARIO DE ITENS;

const item_forms = document.querySelectorAll('.item-form')

let allTrs = [];
let index = 0;
item_forms.forEach(itemForm=>{
    let delet = document.querySelector('.delete');
    let mount = document.getElementById(`id_vendaitem_set-${index}-quantidade`);
    let price = document.getElementById(`id_vendaitem_set-${index}-preco_unitario`);
    let discount = itemForm.querySelector('td .descont');
    let totalValue = itemForm.querySelector('td .totalValue');
    console.log(delet);

    item = itemForm.querySelector("tbody tr");
    console.log(item);
            
    
    discount.addEventListener("input",()=>{
        console.log('OLHA O DESCONTO:',discount.value);
        totalValue.value = (((discount.value/100)*price.value)*mount.value).toFixed(2);
    });

    mount.addEventListener("input",()=>{
        totalValue.value = (((discount.value/100)*price.value)*mount.value).toFixed(2);
        console.log('OLHA A QUANTIDADE',mount.value);
    });

    price.addEventListener("input",()=>{
        totalValue.value = (((discount.value/100)*price.value)*mount.value).toFixed(2);
        console.log('OLHA O PRECO',price.value);
       
    })
})

const itemButton = document.getElementById("item");
const itens = []
itemButton.addEventListener('click',()=>{
    const new_item_forms = document.querySelectorAll('.item-form')
    let index = 0;
    new_item_forms.forEach(itemForm => {
        // if(index!=0){
            // let delet = itemForm.querySelector("td .delete");


            // MONITORAR A ALTERAÇÃO DE VALORES PARA MUDAR O VALOR TOTAL
            let discount = itemForm.querySelector("td .descont");
            let totalValue = itemForm.querySelector("td .totalValue");
            let amount = document.getElementById(`id_vendaitem_set-${index}-quantidade`);
            let price = document.getElementById(`id_vendaitem_set-${index}-preco_unitario`);
            index = index + 1;
            discount.addEventListener("input",()=>{
                console.log('OLHA O DESCONTO:',discount.value);
                totalValue.value = ( (price.value - (discount.value/100)*price.value)*amount.value).toFixed(2);
            })

            amount.addEventListener("input",()=>{
                console.log('OLHA A QUANTIDADE',amount.value);
                totalValue.value = ( (price.value - (discount.value/100)*price.value)*amount.value).toFixed(2);
            });

            price.addEventListener("input",()=>{
                console.log('OLHA O PRECO',price.value);
                totalValue.value = ( (price.value - (discount.value/100)*price.value)*amount.value).toFixed(2);
            })


            // DELETAR UM ITEM 
            // delet.addEventListener("click",()=>{
            //     console.log(delet);
            //     item = itemForm.querySelector("tbody tr");
            //     item.innerHTML = ' ';
            //     console.log(item)
            // })

        // }
        
        });
        
       
    })



// // function deleteItem(){

// // }
// const client_id = document.getElementById("form-client");
const input_client = document.getElementById("id_pessoa");
input_client.addEventListener("input",()=>{
    const clients = document.getElementById("clients");
    if (input_client.value.length >=1 && input_client.value != " "){
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
        clients.innerHTML = '';
        if(data.clientes.length > 0){
            data.clientes.forEach(cliente=>{
                selectClient = document.createElement("button");
                selectClient.className ="btn btn-outline-secondary form-control";
                selectClient.id = `option-${id_options}`
                // selectClient.textContent= `${cliente.id} -- ${cliente.name}`
                selectClient.textContent= `${cliente.name}`
                clients.appendChild(selectClient);

                const button = document.getElementById(selectClient.id);
                button.addEventListener("click",()=>{
                    input_client.value = button.textContent ;
                    console.log(button.textContent)
                    clients.innerHTML = "";
                })
                id_options+=1;
            })
        }
    })
    }else{
        clients.innerHTML = ''
    }
    

    
    

})



teste = document.getElementById("id_paymentmethod_venda_set-0-DELETE");
console.log(teste.value)
teste.addEventListener("click",()=>{
    console.log(teste.value)
})
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

