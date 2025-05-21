import { clean,getCSRFToken,valida,compair } from "./installments.js";

document.addEventListener('DOMContentLoaded',function(){
     const headerTax = document.getElementById('taxInstallment');
    const taxformContainer = document.getElementById("tax-payment-method-container");

    headerTax.style = 'display:none';
    const tax_old_payment_method_form = document.getElementById("old-tax-payment-method-form");
    let taxClick = 0;
    const taxInstallments = document.getElementById('taxGenerate');

    taxInstallments.addEventListener('click',()=>{
        if (tax_old_payment_method_form){
            tax_old_payment_method_form.style.display = 'none';
        }

        let TAX_TOTAL_FORMS = document.getElementById("id_tax_paymentmethod_accounts_set-TOTAL_FORMS")|| document.getElementById("id_tax_form_payment_account_set-TOTAL_FORMS");
        let taxDays_installment_Range = document.getElementById("id_tax_form_accounts-installment_Range");
        let taxInstallmentRange = document.getElementById("id_tax_form_accounts-numberOfInstallments");
        let taxDateInitsemvalor = document.getElementById("id_tax_form_accounts-date_init");
        console.log("OITO");
        console.log(taxInstallmentRange.value);
        if(taxInstallmentRange.value <= 0){
            return 0
        }
    
        taxClick+=1;
        console.log('quantidade de cliques ate agora: '+taxClick);

         if (taxClick > 1){
            if (isNaN(taxInstallmentRange) || isNaN(taxDays_installment_Range)  || isNaN(taxStartDate) || isNaN(taxTotalValue)) {
                clean(TAX_TOTAL_FORMS.value,taxformContainer)
            }
        }

        headerTax.style.removeProperty("display");

        const taxConvertToDate = (dateStr)=>{
            const [day,month,year] = dateStr.split('/').map(num => parseInt(num, 10));
            return new Date(year,month - 1,day);
        };
        const taxInputDate = taxDateInitsemvalor.value.trim();

        const taxStartDate = taxConvertToDate(taxInputDate);

        if(isNaN(taxStartDate.getTime())){
            console.log('Data Inválida');
            return;
        }

        const taxTotalValue = parseFloat(document.getElementById("id_tax_form_accounts-totalValue").value);
        const taxNumberOfInstallments = parseInt(document.getElementById("id_tax_form_accounts-numberOfInstallments").value);

        let taxFragmento = document.createDocumentFragment();
        const taxValueOfInstalments = compair(taxNumberOfInstallments,taxTotalValue);
        const taxTemplate = document.getElementById("empty-tax-payment-method-form");
        let taxCont = 0;

        for(let index = 0;index < taxInstallmentRange.value;index++){
            let parcela = document.createElement('tr')                  // linha
            parcela.id = `taxPayment-${index + 1}`;
            let row_payment_Method = document.createElement('td')       // coluna
            let row_expirationDate = document.createElement('td')       // coluna
            let row_days = document.createElement('td')                 // coluna
            let row_value = document.createElement('td')      
            let row_id = document.createElement("td");          // coluna     
            let row_DELETE = document.createElement('td')                // coluna     
            let clone = taxTemplate.content.cloneNode(true);

            let taxCounter = 0;
            clone.querySelectorAll("input, select").forEach(async (input) => { // interando sobre o formulario
                input.name = input.name.replace("0", index  );
                input.id = input.id.replace("0", index  );
               

                if (input.tagName === "SELECT") {
                    row_payment_Method.appendChild(input)
                    parcela.appendChild(row_payment_Method)
                }else if (input.name.includes("-expirationDate")) {
                    // Calcula a data da parcela
                    let days = (parseInt(taxDays_installment_Range.value,10))
                    let new_date = taxStartDate.setDate(taxStartDate.getDate() + days);
                    let final_date = new Date(new_date)
                    input.value = `${final_date.getDate().toString().padStart(2, '0')}/${(final_date.getMonth() + 1).toString().padStart(2, '0')}/${final_date.getFullYear()} `  
                    
                    row_expirationDate.appendChild(input)
                    parcela.appendChild(row_expirationDate)
                // CALCULO DE VALOR
                }else if (input.name.includes("-value")) {
                    // Define o valor da parcela
                    input.value = taxValueOfInstalments[index];
                    row_value.appendChild(input)
                    parcela.appendChild(row_value)
                    
                    //CALCULO DE DIAS
                }else if (input.name.includes("-days")) {
                        // Define os dias entre as parcelas
                        input.value = taxDays_installment_Range.value*(index + 1 -taxCounter);
                        taxCounter+=1;
                        // console.log(typeof(days_installment_Range))
                        // console.log(days_installment_Range.value*(index + 1 -value_initial.value))
                        row_days.appendChild(input)
                        parcela.appendChild(row_days)
                            
                }
                else if(input.name.includes("-id")){
                    // input.value = id_payments[0];
                    row_id.appendChild(input);
                    parcela.appendChild(row_id)
                }
               
                await taxformContainer.appendChild(parcela);
            })
        }
        TAX_TOTAL_FORMS.value = Number(taxInstallmentRange.value);
        
        console.log('IMPOSTO - total forms é igual a: ' + TAX_TOTAL_FORMS.value)
    })
})