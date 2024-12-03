const fieldClient = document.getElementById("field-client");
const select = document.getElementById("selection");
select.style.display = "none";
console.log('testando');
const options = select.querySelectorAll("option");
fieldClient.addEventListener("input", () => {
    const filterValue = fieldClient.value.toLowerCase(); 

    console.log(filterValue);
    options.forEach(option => {
        var contentText = option.textContent.toLowerCase();
        
        const contentTextLoc = contentText.indexOf("-")
        
        contentText = contentText.slice(contentTextLoc+2);
     
        console.log(contentText);
        if (filterValue.length > 0) {
            select.style.display = "block";
            if (contentText.startsWith(filterValue)) {
                option.style.display = "block";

            } else {
                
                option.style.display = "none";
            }
        } else {
            select.style.display = "none";
        }
    });
});

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




