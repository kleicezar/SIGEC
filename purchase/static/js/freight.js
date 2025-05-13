
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
    }
    else{
        freightValue.style.display = "none";
        freightFormAccounts.style.display = "none";
        freightTable.style.display = "none";
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