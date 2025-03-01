document.addEventListener('DOMContentLoaded', function () {
  
    const header = document.getElementById('installment')

    const formContainer = document.getElementById("payment-method-container");

    
    //escondendo campos de template base e opção de remoção
    header.style = 'display:none;'
    

    let click = 0 // variavel para verificar quantidade de cliques
    const installments = document.getElementById('generate')//gerador de parcelas
    installments.addEventListener('click', () => {
        let value_initial = document.getElementById("id_paymentmethod_accounts_set-INITIAL_FORMS");
        let TOTAL_FORMS = document.getElementById("id_paymentmethod_accounts_set-TOTAL_FORMS");//TOTAL FORMS
        let days_installment_Range = document.getElementById('installment_Range')// intervalo em dias entre parcelas
        let installmentRange = document.getElementById('id_numberOfInstallments')//numero de parcela
        let dateInitsemvalor = document.getElementById("id_date_init"); // Data de início das faturas
        let table = document.getElementById('installment') // tabela das parcelas
        
        if (installmentRange.value <= 0) {
            return 0
        }

        click = click + 1
        console.log('quantidade de cliques ate agora: ' + click)
        if (click > 1){
            clean(TOTAL_FORMS.value)
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

        fragmento = document.createDocumentFragment()
        const valueOfinstallments = compair(numberOfInstallments, totalValue);
        const template = document.getElementById('empty-payment-method-form')
        
        
        for (let index = 0; index < installmentRange.value; index++) {      
            let parcela = document.createElement('tr')                  // linha
            parcela.id = index + 1
            let row_payment_Method = document.createElement('td')       // coluna
            let row_expirationDate = document.createElement('td')       // coluna
            let row_days = document.createElement('td')                 // coluna
            let row_value = document.createElement('td')                // coluna     
            let row_DELETE = document.createElement('td')                // coluna     
            let clone = template.content.cloneNode(true);               // Clonando o template 

            clone.querySelectorAll("input, select").forEach(async (input) => { // interando sobre o formulario
                input.name = input.name.replace("0", index  );
                input.id = input.id.replace("0", index  );

                if (input.tagName === "SELECT") {
                    row_payment_Method.appendChild(input)
                    parcela.appendChild(row_payment_Method)
                }else if (input.name.includes("-expirationDate")) {
                    // Calcula a data da parcela
                    days = (parseInt(days_installment_Range.value,10))
                    new_date = startDate.setDate(startDate.getDate() + days);
                    final_date = new Date(new_date)
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
                        input.value = days_installment_Range.value*(index + 1 -value_initial.value);
                        // console.log(typeof(days_installment_Range))
                        // console.log(days_installment_Range.value*(index + 1 -value_initial.value))
                        row_days.appendChild(input)
                        parcela.appendChild(row_days)
                            
                }
                  await formContainer.appendChild(parcela);
            })
        }    
        TOTAL_FORMS.value = Number(installmentRange.value)
        console.log('total forms é igual a: ' + TOTAL_FORMS.value)
    })

    function compair(numero_parcelas, valor_total){
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
    function clean(total_forms){
        for (let index = 0; index < total_forms; index++) {
            const del = document.getElementById(`${index+1}`)
            console.log('variavel del igual a: ' + del.id)
            if(del.id >= 1){
                del.remove()
            }
        }
    }
})