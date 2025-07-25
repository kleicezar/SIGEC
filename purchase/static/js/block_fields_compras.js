document.addEventListener("DOMContentLoaded",()=>{

    permition_sale = document.getElementById("permition_sale").value;
    permition_saleItem = document.getElementById("permition_saleItem").value;
    permition_payment = document.getElementById("permition_payment").value;

    if (permition_saleItem == "False"){
        // Não permitir adicionar itens de vendas
        const item = document.getElementById("item");
        item.disabled = true;
        
        // Não permitir remover itens de Vendas
        const deleteInputs = document.querySelectorAll('.delete');
        deleteInputs.forEach(deleteInput=>{
            deleteInput.disabled = true;
        });

        // Torna o campo de sugestões de vendas não editável
        const suggestionsSale = document.querySelectorAll('input[id^="idProduct"]');

        suggestionsSale.forEach(suggestionSale => {
            // suggestionSale.disabled = true;
            suggestionSale.readOnly = true; // <- Corrigido aqui
        });
    }
    
    if(permition_payment == "False"){
        const generate = document.getElementById("generate");
        generate.disabled = true;
    }
    if (permition_sale =='False'){
        
        const idSearch = document.getElementById("idSearch");
        idSearch.readOnly = true;
    }
})

