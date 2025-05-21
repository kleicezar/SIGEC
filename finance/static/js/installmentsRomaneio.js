import { clean,getCSRFToken,valida,compair } from "./installments.js";

document.addEventListener('DOMContentLoaded',function(){
    const headerRomaneio = document.getElementById('romaneioInstallment');
    const romaneioformContainer = document.getElementById("romaneio-payment-method-container");

    headerRomaneio.style = 'display:none';
    const romaneio_old_payment_method_form = document.getElementById("old-romaneio-payment-method-form");
    let romaneioClick = 0;
    const romaneioInstallments = document.getElementById('romaneioGenerate');

    romaneioInstallments.addEventListener('click',()=>{
        if (romaneio_old_payment_method_form){
            romaneio_old_payment_method_form.style.display = 'none';
        }

        let ROMANEIO_TOTAL_FORMS = document.getElementById("id_romaneio_paymentmethod_accounts_set-TOTAL_FORMS")|| document.getElementById("id_romaneio_form_payment_account_set-TOTAL_FORMS");
        let romaneioDays_installment_Range = document.getElementById("id_romaneio_form_accounts-installment_Range");
        let romaneioInstallmentRange = document.getElementById("id_romaneio_form_accounts-numberOfInstallments");
        let romaneioDateInitsemvalor = document.getElementById("id_romaneio_form_accounts-date_init");

        console.log(romaneioInstallmentRange.value);
        if(romaneioInstallmentRange.value <= 0){
            return 0
        }
    
        romaneioClick+=1;
        console.log('quantidade de cliques ate agora: '+romaneioClick);

         if (romaneioClick > 1){
            if (isNaN(romaneioInstallmentRange) || isNaN(romaneioDays_installment_Range)  || isNaN(romaneioStartDate) || isNaN(romaneioTotalValue)) {
                clean(ROMANEIO_TOTAL_FORMS.value,romaneioformContainer)
            }
        }

        headerRomaneio.style.removeProperty("display");

        const romaneioConvertToDate = (dateStr)=>{
            const [day,month,year] = dateStr.split('/').map(num => parseInt(num, 10));
            return new Date(year,month - 1,day);
        };
        const romaneioInputDate = romaneioDateInitsemvalor.value.trim();

        const romaneioStartDate = romaneioConvertToDate(romaneioInputDate);

        if(isNaN(romaneioStartDate.getTime())){
            console.log('Data Inválida');
            return;
        }

        const romaneioTotalValue = parseFloat(document.getElementById("id_romaneio_form_accounts-totalValue").value);
        const romaneioNumberOfInstallments = parseInt(document.getElementById("id_romaneio_form_accounts-numberOfInstallments").value);

        let romaneioFragmento = document.createDocumentFragment();
        const romaneioValueOfInstalments = compair(romaneioNumberOfInstallments,romaneioTotalValue);
        const romaneioTemplate = document.getElementById("empty-romaneio-payment-method-form");
        let romaneioCont = 0;

        for(let index = 0;index < romaneioInstallmentRange.value;index++){
            let parcela = document.createElement('tr')                  // linha
            parcela.id = `romaneioPayment-${index + 1}`;
            let row_payment_Method = document.createElement('td')       // coluna
            let row_expirationDate = document.createElement('td')       // coluna
            let row_days = document.createElement('td')                 // coluna
            let row_value = document.createElement('td')      
            let row_id = document.createElement("td");          // coluna     
            let row_DELETE = document.createElement('td')                // coluna     
            let clone = romaneioTemplate.content.cloneNode(true);

            let romaneioCounter = 0;
            clone.querySelectorAll("input, select").forEach(async (input) => { // interando sobre o formulario
                input.name = input.name.replace("0", index  );
                input.id = input.id.replace("0", index  );
               

                if (input.tagName === "SELECT") {
                    row_payment_Method.appendChild(input)
                    parcela.appendChild(row_payment_Method)
                }else if (input.name.includes("-expirationDate")) {
                    // Calcula a data da parcela
                    let days = (parseInt(romaneioDays_installment_Range.value,10))
                    let new_date = romaneioStartDate.setDate(romaneioStartDate.getDate() + days);
                    let final_date = new Date(new_date)
                    input.value = `${final_date.getDate().toString().padStart(2, '0')}/${(final_date.getMonth() + 1).toString().padStart(2, '0')}/${final_date.getFullYear()} `  
                    
                    row_expirationDate.appendChild(input)
                    parcela.appendChild(row_expirationDate)
                // CALCULO DE VALOR
                }else if (input.name.includes("-value")) {
                    // Define o valor da parcela
                    input.value = romaneioValueOfInstalments[index];
                    row_value.appendChild(input)
                    parcela.appendChild(row_value)
                    
                    //CALCULO DE DIAS
                }else if (input.name.includes("-days")) {
                        // Define os dias entre as parcelas
                        input.value = romaneioDays_installment_Range.value*(index + 1 -romaneioCounter);
                        romaneioCounter+=1;
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
               
                await romaneioformContainer.appendChild(parcela);
            })
        }
        ROMANEIO_TOTAL_FORMS.value = Number(romaneioInstallmentRange.value);
        
        console.log('IMPOSTO - total forms é igual a: ' + ROMANEIO_TOTAL_FORMS.value)
    })
})