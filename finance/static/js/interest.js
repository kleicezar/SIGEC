// Usando jQuery para facilitar o controle da visibilidade
document.addEventListener('DOMContentLoaded', function () {
    
  



    
    // rascunho 01
    // function toggleFields_installment_Range() {
    //     if (installmentRange.value == 'A cada 15 dias') {
    //         finePercentField.style.display = 'block'; // Mostrar o campo de porcentagem
    //         fineValueField.style.display = 'none';   // Esconder o campo de valor
    //     } else if (installmentRange.value === 'A cada 20 dias') {
    //         fineValueField.style.display = 'block';   // Mostrar o campo de valor
    //         finePercentField.style.display = 'none';  // Esconder o campo de porcentagem
    //     } else if (installmentRange.value === 'A cada 23 dias') {
    //         fineValueField.style.display = 'block';   // Mostrar o campo de valor
    //         finePercentField.style.display = 'none';  // Esconder o campo de porcentagem
    //     } else if (installmentRange.value === 'A cada 28 dias') {
    //         fineValueField.style.display = 'block';   // Mostrar o campo de valor
    //         finePercentField.style.display = 'none';  // Esconder o campo de porcentagem
    //     } else if (installmentRange.value === 'A cada 30 dias') {
    //         fineValueField.style.display = 'block';   // Mostrar o campo de valor
    //         finePercentField.style.display = 'none';  // Esconder o campo de porcentagem
    //     } else {
            
    //     }
    // }
    
    // rascunho 02
    // CODIGO A PARTIR DAQ
    // Obtém os elementos principais
    const installmentRange = document.getElementById('installment_Range')
    const formContainer = document.getElementById("payment-method-container");
    const dateInitsemvalor = document.getElementById("id_date_init"); // Data de início das faturas
    const formCountElem = document.getElementById("id_paymentmethod_accounts_set-TOTAL_FORMS");//TOTAL FORMS
    const installments = document.getElementById('generate')//gerador de parcelas
    const templatenone = document.getElementById('id_paymentmethod_accounts_set-0-DELETE')//gerador de parcelas

    let part = 0
    let table = null;
    installments.addEventListener('click', () => {
        console.log("Tá clicado meu amigo")
        const itensPaymentMethodContainer = formContainer.querySelectorAll("item-form");
        itensPaymentMethodContainer.forEach(item=>{
            console.log('removido')
        formContainer.removeChild(item)
        })
        const numberOfInstallments = parseInt(document.getElementById("id_numberOfInstallments").value); // Número de parcelas
        const dateInit = document.getElementById("id_date_init"); // Data de início das faturas
        const installment_Range = parseInt(document.getElementById("installment_Range").value); // Intervalo entre faturas (em dias)
        const totalValue = parseFloat(document.getElementById("id_totalValue").value); // Valor de cada parcela

        if (templatenone) {
            templatenone.remove()
        }
        // --------------------------------- //
        // Validações básicas
        // converter a data no formato js 
        const convertToDate = (dateStr) => {
            const [day, month, year] = dateStr.split('/').map(num => parseInt(num, 10));
            return new Date(year, month - 1, day); // Mês no JavaScript é baseado em zero
        };
        const inputDate = dateInit.value.trim();
        // Converter a data inicial
        const startDate = convertToDate(inputDate);
        // Verifica se a data foi convertida corretamente
        if (isNaN(startDate.getTime())) {
            console.error('Data inválida');
            return;
        }
        // --------------------------------- //

        if (isNaN(numberOfInstallments) || isNaN(installment_Range)  || isNaN(startDate) || isNaN(totalValue)) { 
            alert("Por favor, preencha todos os campos corretamente. BY: kleitin");
            return;
        }
        
        // console.log(numberOfInstallments)
        //apaga tudo
        if (table != null) {
            console.log(formCountElem)
                for (let index = 1; index <= formCountElem.value; index++) {
                    let div = document.getElementById('del') ;
                    if (div != null) {
                        div.remove();
                    }
                }


            table = null;
            formCountElem.value = 1
        }
        
        const valueOfinstallments = compair(numberOfInstallments, totalValue)     
        const emptyFormTemplate = document.getElementById('empty-payment-method-form');
        for (let index = 1; index < numberOfInstallments + 1 ; index++) {
            if (!emptyFormTemplate) {
                console.error("Template de formulário vazio (empty-payment-method-form) não encontrado!");
                return;
            }
            const newForm = emptyFormTemplate.content.cloneNode(true);
            // Atualiza os campos do formulário clonado
            newForm.querySelectorAll("input, select").forEach(async (input) => {
                input.name = input.name.replace("__prefix__", formCountElem.value);
                input.id = input.id.replace("__prefix__", formCountElem.value);
                // Preenche os valores iniciais nos campos do formulário

                // CALCULO DE DADAS DE VENCIMENTO
                if (input.name.includes("-expirationDate")) {
                    // Calcula a data da parcela
                    days = (parseInt(installmentRange.value,10))
                    new_date = startDate.setDate(startDate.getDate() + days);
                    final_date = new Date(new_date)
                    input.value = `${final_date.getDate().toString().padStart(2, '0')}/${(final_date.getMonth() + 1).toString().padStart(2, '0')}/${final_date.getFullYear()} `  
                    // console.log(input.value)
                    // CALCULO DE VALOR
                }else if (input.name.includes("-value")) {
                    // Define o valor da parcela
                    input.value = valueOfinstallments[index-1];
                    //CALCULO DE DIAS
                    }else if (input.name.includes("-days")) {
                        // Define os dias entre as parcelas
                        input.value = installment_Range*index;
                    }
                    // Adiciona o formulário ao contêiner
                    await formContainer.appendChild(newForm);
                })
                formCountElem.value = Number(formCountElem.value) + 1
            }
        table = 'null';
        part = formCountElem
        
    })
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