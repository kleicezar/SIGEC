document.addEventListener('DOMContentLoaded', function () {
    const id_plannedAccount = document.getElementById("id_plannedAccount");
    if (id_plannedAccount){
        if (id_plannedAccount.checked){
            console.log('entrei aqui na verdade');
            const date_init = document.getElementById("id_date_init");
            date_init.id = "date_init_planned_account";
            generateInstallmentsPlannedAccount();
        }
        else{
            const date_init = document.getElementById("date_init_planned_account");
            
            if (date_init){
                date_init.id = "id_date_init";
            }
            generateInstallments();
        }
        
    }
    else{
        generateInstallments();
    }
   


}
)
function generateInstallmentsPlannedAccount(){
    const header = document.getElementById('installment');
    
    const formContainer = document.getElementById("payment-method-container");

    header.style = 'display:none;'
    //escondendo campos de template base e opção de remoção
    // header.style = 'display:none;'
    const old_payment_method_form = document.getElementById("old-payment-method-form");
    let click = 0 // variavel para verificar quantidade de cliques
    const installments = document.getElementById('generate')//gerador de parcelas
    
    installments.addEventListener('click', () => {
        // Ao clicar em gerar e haver pagamentos presentes no banco, eles serao apagados
        if (old_payment_method_form){                
            old_payment_method_form.style.display="none";
        }

        let TOTAL_FORMS = document.getElementById("id_paymentmethod_accounts_set-TOTAL_FORMS");//TOTAL FORMS
        let mounths_installment_Range = document.getElementById('id_installment_Range');// intervalo em dias entre parcelas
        let installmentRange = document.getElementById('id_numberOfInstallments');//numero de parcela
        let dateInitsemvalor = document.getElementById("date_init_planned_account"); // Data de início das faturas

        if (installmentRange.value <= 0) {
            return 0
        }

        click = click + 1
        console.log('quantidade de cliques ate agora: ' + click)
        if (click > 1){
            if (isNaN(installmentRange) || isNaN(mounths_installment_Range)  || isNaN(startDate) || isNaN(totalValue)) {
                clean(TOTAL_FORMS.value)
            }
        }
        
        header.style.removeProperty('display')

        
        const convertToDate = (dateStr) => { //#FIXME inportante
            const [month, year] = dateStr.split('/').map(num => parseInt(num, 10));
            return new Date(year, month - 1); // Mês no JavaScript é baseado em zero
        };
        const inputDate = dateInitsemvalor.value.trim();
        
        // Converter a data inicial
        const startDate = convertToDate(inputDate);
        // Verifica se a data foi convertida corretamente
        if (isNaN(startDate.getTime())) {
            console.error('Data inválida');
            return;
        }

        
        const totalValue = parseFloat(document.getElementById("id_totalValue").value); // Valor de cada parcela
        const numberOfInstallments = parseInt(document.getElementById("id_numberOfInstallments").value); // Número de parcelas

        let fragmento = document.createDocumentFragment()
        const valueOfinstallments = compair(numberOfInstallments, totalValue);
        const template = document.getElementById('empty-payment-method-form');
        let cont=0;
        let counter2 = 0;
        for (let index = 0; index < installmentRange.value; index++) { 
            let parcela = document.createElement('tr')                  // linha
            parcela.id = index + 1
            let row_payment_Method = document.createElement('td')       // coluna
            let row_expirationDate = document.createElement('td')       // coluna
            let row_mounths = document.createElement('td')                 // coluna
            let row_value = document.createElement('td')      
            let row_id = document.createElement("td");          // coluna     
            let row_DELETE = document.createElement('td')                // coluna     
            let clone = template.content.cloneNode(true);               // Clonando o template 
            
            
            let counter = 0;
           
            clone.querySelectorAll("input, select").forEach(async (input) => { // interando sobre o formulario
                input.name = input.name.replace("0", index  );
                input.id = input.id.replace("0", index  );
               

                if (input.tagName === "SELECT") {
                    row_payment_Method.appendChild(input)
                    parcela.appendChild(row_payment_Method)
                }else if (input.name.includes("-expirationDate")) {
                    // Calcula a data da parcela
                    counter2+=1;
                    let mounth = (parseInt(mounths_installment_Range.value,10));       
                    let newDate = new Date(startDate.getFullYear(), startDate.getMonth() + (counter2*mounth)+1, 0);
                    let final_date = new Date(newDate)
                    input.value = `${final_date.getDate().toString().padStart(2, '0')}/${(final_date.getMonth()+1).toString().padStart(2, '0')}/${final_date.getFullYear()}`  
                    
                    row_expirationDate.appendChild(input)
                    parcela.appendChild(row_expirationDate)
                // CALCULO DE VALOR
                }else if (input.name.includes("-value")) {
                    // Define o valor da parcela
                    input.value = valueOfinstallments[index];
                    row_value.appendChild(input)
                    parcela.appendChild(row_value)
                    
                    //CALCULO DE DIAS
                }else if (input.name.includes("-days")) {
                        // Define os dias entre as parcelas
                        input.value = mounths_installment_Range.value*(index + 1 -counter);

                        counter+=1;
                        // console.log(typeof(mounths_installment_Range))
                        // console.log(days_installment_Range.value*(index + 1 -value_initial.value))
                        row_mounths.appendChild(input)
                        parcela.appendChild(row_mounths)
                            
                }
                else if(input.name.includes("-id")){
                    // input.value = id_payments[0];
                    row_id.appendChild(input);
                    parcela.appendChild(row_id)
                }
               
                await formContainer.appendChild(parcela);
            })
        }    
        TOTAL_FORMS.value = Number(installmentRange.value)
        console.log('total forms é igual a: ' + TOTAL_FORMS.value)
    })
}
function generateInstallments(){
    const header = document.getElementById('installment');
    
    const formContainer = document.getElementById("payment-method-container");

    header.style = 'display:none;'
    //escondendo campos de template base e opção de remoção
    // header.style = 'display:none;'
    const old_payment_method_form = document.getElementById("old-payment-method-form");
    let click = 0 // variavel para verificar quantidade de cliques
    const installments = document.getElementById('generate')//gerador de parcelas
    
    installments.addEventListener('click', () => {
        // Ao clicar em gerar e haver pagamentos presentes no banco, eles serao apagados
        if (old_payment_method_form){                
            old_payment_method_form.style.display="none";
        }

        let TOTAL_FORMS = document.getElementById("id_paymentmethod_accounts_set-TOTAL_FORMS");//TOTAL FORMS
        let days_installment_Range = document.getElementById('id_installment_Range');// intervalo em dias entre parcelas
        let installmentRange = document.getElementById('id_numberOfInstallments');//numero de parcela
        let dateInitsemvalor = document.getElementById("id_date_init"); // Data de início das faturas

        if (installmentRange.value <= 0) {
            return 0
        }

        click = click + 1
        console.log('quantidade de cliques ate agora: ' + click)
        if (click > 1){
            if (isNaN(installmentRange) || isNaN(days_installment_Range)  || isNaN(startDate) || isNaN(totalValue)) {
                clean(TOTAL_FORMS.value)
            }
        }
        
        header.style.removeProperty('display')

        
        const convertToDate = (dateStr) => { //#FIXME inportante
            const [day, month, year] = dateStr.split('/').map(num => parseInt(num, 10));
            return new Date(year, month - 1, day); // Mês no JavaScript é baseado em zero
        };
        const inputDate = dateInitsemvalor.value.trim();
        // Converter a data inicial
        const startDate = convertToDate(inputDate);
        // Verifica se a data foi convertida corretamente
        if (isNaN(startDate.getTime())) {
            console.error('Data inválida');
            return;
        }

        
        const totalValue = parseFloat(document.getElementById("id_totalValue").value); // Valor de cada parcela
        const numberOfInstallments = parseInt(document.getElementById("id_numberOfInstallments").value); // Número de parcelas

        let fragmento = document.createDocumentFragment()
        const valueOfinstallments = compair(numberOfInstallments, totalValue);
        const template = document.getElementById('empty-payment-method-form');
        let cont=0;
        for (let index = 0; index < installmentRange.value; index++) { 
            console.log("entrie")     
            let parcela = document.createElement('tr')                  // linha
            parcela.id = index + 1
            let row_payment_Method = document.createElement('td')       // coluna
            let row_expirationDate = document.createElement('td')       // coluna
            let row_days = document.createElement('td')                 // coluna
            let row_value = document.createElement('td')      
            let row_id = document.createElement("td");          // coluna     
            let row_DELETE = document.createElement('td')                // coluna     
            let clone = template.content.cloneNode(true);               // Clonando o template 
            
            
            let counter = 0;
            clone.querySelectorAll("input, select").forEach(async (input) => { // interando sobre o formulario
                input.name = input.name.replace("0", index  );
                input.id = input.id.replace("0", index  );
               

                if (input.tagName === "SELECT") {
                    row_payment_Method.appendChild(input)
                    parcela.appendChild(row_payment_Method)
                }else if (input.name.includes("-expirationDate")) {
                    // Calcula a data da parcela
                    let days = (parseInt(days_installment_Range.value,10))
                    let new_date = startDate.setDate(startDate.getDate() + days);
                    let final_date = new Date(new_date)
                    input.value = `${final_date.getDate().toString().padStart(2, '0')}/${(final_date.getMonth() + 1).toString().padStart(2, '0')}/${final_date.getFullYear()} `  
                    
                    row_expirationDate.appendChild(input)
                    parcela.appendChild(row_expirationDate)
                // CALCULO DE VALOR
                }else if (input.name.includes("-value")) {
                    // Define o valor da parcela
                    input.value = valueOfinstallments[index];
                    row_value.appendChild(input)
                    parcela.appendChild(row_value)
                    
                    //CALCULO DE DIAS
                }else if (input.name.includes("-days")) {
                        // Define os dias entre as parcelas
                        input.value = days_installment_Range.value*(index + 1 -counter);
                        counter+=1;
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
               
                await formContainer.appendChild(parcela);
            })
        }    
        TOTAL_FORMS.value = Number(installmentRange.value)
        console.log('total forms é igual a: ' + TOTAL_FORMS.value)
    })
}

export function compair(numero_parcelas, valor_total){
    const array_valor_parcelas = [];
    let all_parcela = 0
    for (let index = 0; index <= numero_parcelas-1; index++) {
        let valor_parcela = (valor_total/numero_parcelas).toFixed(2)
            
        all_parcela = parseFloat(all_parcela) + parseFloat(valor_parcela)
        if(index===numero_parcelas-1){
            let ultima_parcela = parseFloat(valor_parcela) + (valor_total - all_parcela);
            array_valor_parcelas[index] = ultima_parcela.toFixed(2);
        }else {
            array_valor_parcelas[index] = valor_parcela;
        }
    }
    return array_valor_parcelas
    }
export function valida(){
    if (isNaN(numberOfInstallments) || isNaN(installment_Range)  || isNaN(startDate) || isNaN(totalValue)) { 
        alert("Por favor, preencha todos os campos corretamente. BY: kleitin");
        return;
    }
    }
export function clean(total_forms){
    for (let index = 0; index < total_forms; index++) {
        const del = document.getElementById(`${index+1}`)
        if (del != null) {
            console.log('variavel del igual a: ' + del.id)
            if(del.id >= 1){
                del.remove()
            }
        }
    }
    }
    
export function getCSRFToken() {
    let cookieValue = null;
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith('csrftoken=')) {
            cookieValue = cookie.substring('csrftoken='.length, cookie.length);
            break;
        }
    }
    return cookieValue;
}

