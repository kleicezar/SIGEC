const productsTotalValue = document.getElementById("id_total_value");
const taxTotalValue = document.getElementById("id_tax_form_accounts-totalValue");
const taxValue = document.getElementById("id_tax_value");

taxValue.addEventListener("input",()=>{
    console.log('Monitorando o valor de Imposto');

    if (productsTotalValue.value != 0){
        taxTotalValue.value = (Number(productsTotalValue.value) - Number(productsTotalValue.value)*Number((taxValue.value)/100));
    }
    else{
        taxTotalValue.value = 0;
    }
})