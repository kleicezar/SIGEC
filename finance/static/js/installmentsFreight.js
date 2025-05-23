import { clean,getCSRFToken,valida,compair } from "./installments.js";

document.addEventListener('DOMContentLoaded',function(){
    const headerFreight = document.getElementById('freightInstallment');
    const freightformContainer = document.getElementById("freight-payment-method-container");

    headerFreight.style = 'display:none';
    const freight_old_payment_method_form = document.getElementById("old-freight-payment-method-form");
    let freightClick = 0;
    const freightInstallments = document.getElementById('freightGenerate');

    freightInstallments.addEventListener('click',()=>{
        if (freight_old_payment_method_form){
            freight_old_payment_method_form.style.display = 'none';
        }

        let FREIGHT_TOTAL_FORMS = document.getElementById("id_freight_paymentmethod_accounts_set-TOTAL_FORMS")|| document.getElementById("id_freight_form_payment_account_set-TOTAL_FORMS");
        let freightDays_installment_Range = document.getElementById("id_freight_form_accounts-installment_Range");
        let freightInstallmentRange = document.getElementById("id_freight_form_accounts-numberOfInstallments");
        let freightDateInitsemvalor = document.getElementById("id_freight_form_accounts-date_init");

        console.log(freightInstallmentRange.value);
        if(freightInstallmentRange.value <= 0){
            return 0
        }
    
        freightClick+=1;
        console.log('quantidade de cliques ate agora: '+freightClick);

         if (freightClick > 1){
            if (isNaN(freightInstallmentRange) || isNaN(freightDays_installment_Range)  || isNaN(freightStartDate) || isNaN(freightTotalValue)) {
                clean(FREIGHT_TOTAL_FORMS.value,freightformContainer)
            }
        }

        headerFreight.style.removeProperty("display");

        const freightConvertToDate = (dateStr)=>{
            const [day,month,year] = dateStr.split('/').map(num => parseInt(num, 10));
            return new Date(year,month - 1,day);
        };
        const freightInputDate = freightDateInitsemvalor.value.trim();

        const freightStartDate = freightConvertToDate(freightInputDate);

        if(isNaN(freightStartDate.getTime())){
            console.log('Data Inválida');
            return;
        }

        const freightTotalValue = parseFloat(document.getElementById("id_freight_form_accounts-totalValue").value);
        const freightNumberOfInstallments = parseInt(document.getElementById("id_freight_form_accounts-numberOfInstallments").value);

        let freightFragmento = document.createDocumentFragment();
        const freightValueOfInstalments = compair(freightNumberOfInstallments,freightTotalValue);
        const freightTemplate = document.getElementById("empty-freight-payment-method-form");
        let freightCont = 0;

        for(let index = 0;index < freightInstallmentRange.value;index++){
            let parcela = document.createElement('tr')                  // linha
            parcela.id = `freightPayment-${index + 1}`;
            let row_payment_Method = document.createElement('td')       // coluna
            let row_expirationDate = document.createElement('td')       // coluna
            let row_days = document.createElement('td')                 // coluna
            let row_value = document.createElement('td')      
            let row_id = document.createElement("td");          // coluna     
            let row_DELETE = document.createElement('td')                // coluna     
            let clone = freightTemplate.content.cloneNode(true);

            let freightCounter = 0;
            clone.querySelectorAll("input, select").forEach(async (input) => { // interando sobre o formulario
                input.name = input.name.replace("0", index  );
                input.id = input.id.replace("0", index  );
               

                if (input.tagName === "SELECT") {
                    row_payment_Method.appendChild(input)
                    parcela.appendChild(row_payment_Method)
                }else if (input.name.includes("-expirationDate")) {
                    // Calcula a data da parcela
                    let days = (parseInt(freightDays_installment_Range.value,10))
                    let new_date = freightStartDate.setDate(freightStartDate.getDate() + days);
                    let final_date = new Date(new_date)
                    input.value = `${final_date.getDate().toString().padStart(2, '0')}/${(final_date.getMonth() + 1).toString().padStart(2, '0')}/${final_date.getFullYear()} `  
                    
                    row_expirationDate.appendChild(input)
                    parcela.appendChild(row_expirationDate)
                // CALCULO DE VALOR
                }else if (input.name.includes("-value")) {
                    // Define o valor da parcela
                    input.value = freightValueOfInstalments[index];
                    row_value.appendChild(input)
                    parcela.appendChild(row_value)
                    
                    //CALCULO DE DIAS
                }else if (input.name.includes("-days")) {
                        // Define os dias entre as parcelas
                        input.value = freightDays_installment_Range.value*(index + 1 -freightCounter);
                        freightCounter+=1;
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
               
                await freightformContainer.appendChild(parcela);
            })
        }
        FREIGHT_TOTAL_FORMS.value = Number(freightInstallmentRange.value);
        
        console.log('IMPOSTO - total forms é igual a: ' + FREIGHT_TOTAL_FORMS.value)
    })
})