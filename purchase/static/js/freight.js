
document.addEventListener("DOMContentLoaded",()=>{
    const selectFreight = document.getElementById("id_freight_type");
    const freightFormAccounts = document.getElementById("freightpaymentMethod_account");
    let FREIGHT_TOTAL_FORMS = document.getElementById("id_freight_paymentmethod_accounts_set-TOTAL_FORMS")|| document.getElementById("id_freight_form_payment_account_set-TOTAL_FORMS");
    const freightTable = document.getElementById("freightInstallment");
    const freightValue = document.getElementById("id_freight_value");
    const selectedValue = selectFreight.value;
    if(selectedValue === "fob"){
        freightValue.style.display = "table";
        freightFormAccounts.style.display = "table";
        freightTable.style.display = "table";
    }
    else{
        freightValue.style.display = "none";
        freightFormAccounts.style.display = "none";
        freightTable.style.display = "none";
        FREIGHT_TOTAL_FORMS.value = 0;
    }
})



// id_freight_form_accounts-numberOfInstallments
const freightNumberOfInstallments = document.getElementById("id_freight_form_accounts-numberOfInstallments");
// id_freight_form_accounts-date_init
const freightDateInit = document.getElementById("id_freight_form_accounts-date_init");
// id_freight_form_accounts-installment_Range
const freightInstallmentRange = document.getElementById("id_freight_form_accounts-installment_Range");
// id_freight_form_accounts-totalValue
const freightTotalValue = document.getElementById("id_freight_form_accounts-totalValue");


const selectFreight = document.getElementById("id_freight_type");
selectFreight.addEventListener("change",function(){
    const old_freightPayments = document.getElementById("old-freight-payment-method-form");
    const selectedValue = this.value;
    
    const freightFormAccounts = document.getElementById("freightpaymentMethod_account");
    let FREIGHT_TOTAL_FORMS = document.getElementById("id_freight_paymentmethod_accounts_set-TOTAL_FORMS")|| document.getElementById("id_freight_form_payment_account_set-TOTAL_FORMS");
    const freightTable = document.getElementById("freightInstallment");
    const freightValue = document.getElementById("id_freight_value");
    if(selectedValue === "fob"){
        freightValue.style.display = "table";
        freightFormAccounts.style.display = "table";
        freightTable.style.display = "table";

        freightNumberOfInstallments.setAttribute('required',true);
        freightDateInit.setAttribute('required',true);
        freightInstallmentRange.setAttribute('required',true);
        freightTotalValue.setAttribute('required',true);
        freightValue.setAttribute('required',true);
    }
    else{
        freightValue.style.display = "none";
        freightFormAccounts.style.display = "none";
        freightTable.style.display = "none";

        freightNumberOfInstallments.removeAttribute('required');
        freightDateInit.removeAttribute('required');
        freightInstallmentRange.removeAttribute('required');
        freightTotalValue.removeAttribute('required');
        freightValue.removeAttribute('required');
        console.log('oipaaa')
        console.log("oooopppa")
        if (old_freightPayments){
            const inputFreights = old_freightPayments.querySelectorAll("input[name$='DELETE']");
            inputFreights.forEach(inputFreight=>{
                console.log(inputFreight)
                inputFreight.value = "on";
            })
            old_freightPayments.style.display="none"
        }
        

    }
})