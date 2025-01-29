// Usando jQuery para facilitar o controle da visibilidade
document.addEventListener('DOMContentLoaded', function () {
    const interestType = document.getElementById('interest_type');
    const interestValueField = document.getElementById('interest_value_field');
    const interestPercentField = document.getElementById('interest_percent_field');
    const fineType = document.getElementById('fine_type');
    const fineValueField = document.getElementById('fine_value_field');
    const finePercentField = document.getElementById('fine_percent_field');
    
    // Função para exibir o campo correto
    function toggleFields_Interest() {
        if (interestType.value === 'percent') {
            interestPercentField.style.display = 'block'; // Mostrar o campo de porcentagem
            interestValueField.style.display = 'none';   // Esconder o campo de valor
        } else if (interestType.value === 'value') {
            interestValueField.style.display = 'block';   // Mostrar o campo de valor
            interestPercentField.style.display = 'none';  // Esconder o campo de porcentagem
        } else {
            interestValueField.style.display = 'none';    // Esconder ambos os campos
            interestPercentField.style.display = 'none';
        }
    }
    
    function toggleFields_Fine() {
        if (fineType.value === 'percent') {
            finePercentField.style.display = 'block'; // Mostrar o campo de porcentagem
            fineValueField.style.display = 'none';   // Esconder o campo de valor
        } else if (fineType.value === 'value') {
            fineValueField.style.display = 'block';   // Mostrar o campo de valor
            finePercentField.style.display = 'none';  // Esconder o campo de porcentagem
        } else {
            fineValueField.style.display = 'none';    // Esconder ambos os campos
            finePercentField.style.display = 'none';
        }
    }

    const installmentRange = document.getElementById('installment_Range');

    // Chama a função ao carregar a página para garantir que o campo certo apareça
    // toggleFields_Interest();
    // toggleFields_Fine();
    // toggleFields_installment_Range();

    // Chama a função sempre que a seleção mudar
    // interestType.addEventListener('change', toggleFields_Interest);
    // fineType.addEventListener('change', toggleFields_Fine);



    
    // rascunho 01
    function toggleFields_installment_Range() {
        if (installmentRange.value == 'A cada 15 dias') {
            finePercentField.style.display = 'block'; // Mostrar o campo de porcentagem
            fineValueField.style.display = 'none';   // Esconder o campo de valor
        } else if (installmentRange.value === 'A cada 20 dias') {
            fineValueField.style.display = 'block';   // Mostrar o campo de valor
            finePercentField.style.display = 'none';  // Esconder o campo de porcentagem
        } else if (installmentRange.value === 'A cada 23 dias') {
            fineValueField.style.display = 'block';   // Mostrar o campo de valor
            finePercentField.style.display = 'none';  // Esconder o campo de porcentagem
        } else if (installmentRange.value === 'A cada 28 dias') {
            fineValueField.style.display = 'block';   // Mostrar o campo de valor
            finePercentField.style.display = 'none';  // Esconder o campo de porcentagem
        } else if (installmentRange.value === 'A cada 30 dias') {
            fineValueField.style.display = 'block';   // Mostrar o campo de valor
            finePercentField.style.display = 'none';  // Esconder o campo de porcentagem
        } else {
            
        }
    }
    
    // rascunho 02
    // CODIGO A PARTIR DAQ
    // Obtém os elementos principais
    const formContainer = document.getElementById("payment-method-container");
    const dateInitsemvalor = document.getElementById("id_date_init"); // Data de início das faturas
    const formCountElem = document.getElementById("id_paymentmethod_accountspayable_set-TOTAL_FORMS");//TOTAL FORMS
    const installments = document.getElementById('generate')//gerador de parcelas
    // const valueOfInstallments = parseFloat(document.getElementById("id_valueOfInstallments").value); // Valor de cada parcela
    
    // // console.log(formCountElem.value)
    // valueOfInstallments.addEventListener()

    
    installments.addEventListener('click', () => {
        const itensPaymentMethodContainer = formContainer.querySelectorAll("item-form");
        itensPaymentMethodContainer.forEach(item=>{
            console.log('removido')
        formContainer.removeChild(item)
        })
        const numberOfInstallments = parseInt(document.getElementById("id_numberOfInstallments").value); // Número de parcelas
        const dateInit = document.getElementById("id_date_init"); // Data de início das faturas
        const installment_Range = parseInt(document.getElementById("installment_Range").value); // Intervalo entre faturas (em dias)
        // const valueOfInstallments = parseFloat(document.getElementById("id_valueOfInstallments")); // Valor de cada parcela
        const totalValue = parseFloat(document.getElementById("id_totalValue").value); // Valor de cada parcela

        // valueOfInstallments.value = (parseFloat(totalValue).toFixed(2) / parseFloat(numberOfInstallments)).toFixed(2)

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

        if (isNaN(numberOfInstallments) || isNaN(installment_Range)  || isNaN(startDate) || isNaN(totalValue)) {  //  || isNaN(valueOfInstallments)
            alert("Por favor, preencha todos os campos corretamente. BY: kleitin");
            return;
        }
        
        if (numberOfInstallments == (Number(formCountElem.value) && numberOfInstallments != 1)){
            compair(numberOfInstallments,(Number(formCountElem.value)));


        }else if(numberOfInstallments >= (Number(formCountElem.value) || numberOfInstallments == 1)){
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
                        // console.log(days)
                        new_date = startDate.setDate(startDate.getDate() + days);
                        // startDate.setDate(startDate.getDate() + (parseInt(installmentRange) * index))
                        final_date = new Date(new_date)

                        input.value = `${final_date.getDate()}/${(final_date.getMonth() + 1).toString().padStart(2, '0')}/${final_date.getFullYear()} `  
                        // console.log(input)                                
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
                        // console.log(newForm)
                        await formContainer.appendChild(newForm);
                    })
                formCountElem.value = Number(formCountElem.value) + 1
            }
        } else {
            console.log('numberOfInstallments é: '+ numberOfInstallments + ' e formCountElem é: ')
            console.log(parseInt(formCountElem.value) + 1)
        }

    })
})
    // console.log(numberOfInstallments)
    // console.log(installment_Range)
    // console.log(valueOfInstallments)
    // console.log(formCountElem)
    
    // dateInit.addEventListener('change', () => {
    //     if (dateInit.value.trim() !== '') {
    //       console.log('Informação confirmada:', dateInit.value);
    //       // Execute sua lógica aqui
    //     }
    //   });
    // numberOfInstallments.addEventListener('change', () => {
    //     if (numberOfInstallments.value.trim() !== '') {
    //       console.log('Informação confirmada:', numberOfInstallments.value);
    //       // Execute sua lógica aqui
    //     }
    //   });
    // installment_Range.addEventListener('change', () => {
    //     if (installment_Range.value.trim() !== '') {
    //       console.log('Informação confirmada:', installment_Range.value);
    //       // Execute sua lógica aqui
    //     }
    //   });
    // valueOfInstallments.addEventListener('change', () => {
    //     if (valueOfInstallments.value.trim() !== '') {
    //       console.log('Informação confirmada:', valueOfInstallments.value);
    //       // Execute sua lógica aqui
    //     }
    //   });
    // formCountElem.addEventListener('change', () => {
    //     if (formCountElem.value.trim() !== '') {
    //       console.log('Informação confirmada:', formCountElem.value);
    //       // Execute sua lógica aqui
    //     }
    //   });




    // if (!formCountElem) {
    //     console.error("Elemento TOTAL_FORMS não encontrado!");
    //     return;
    // }

    // const initialFormCount = parseInt(formCountElem.value); // Valor inicial de TOTAL_FORMS
        
    // // Validações básicas
    // if (isNaN(numberOfInstallments) || isNaN(installment_Range) || isNaN(valueOfInstallments) || isNaN(dateInit.getTime())) {
    //     alert("Por favor, preencha todos os campos corretamente.");
    //     return;
    // }

    // for (let index = 0; index < numberOfInstallments; index++) {
    //     const emptyPaymentMethodTemplate = document.getElementById("empty-payment-method-form");

    //     if (!emptyPaymentMethodTemplate) {
    //         console.error("Template de formulário vazio (empty-payment-method-form) não encontrado!");
    //         return;
    //     }

    //     // Clona o template vazio
    //     const newForm = emptyPaymentMethodTemplate.content.cloneNode(true);

    //     // Define o índice do formulário no formset
    //     const formIndex = initialFormCount + index;

    //     // Atualiza os campos do formulário clonado
    //     newForm.querySelectorAll("input, select").forEach((input) => {
    //         input.name = input.name.replace("__prefix__", formIndex);
    //         input.id = input.id.replace("__prefix__", formIndex);

    //         // Preenche os valores iniciais nos campos do formulário
    //         if (input.name.includes("-expirationDate")) {
    //             // Calcula a data da parcela
    //             const installmentDate = new Date(dateInit);
    //             input.value = installmentDate.setDate(dateInit.getDate() + installment_Range * index);

    //         } else if (input.name.includes("-value")) {
    //             // Define o valor da parcela
    //             input.value = valueOfInstallments.toFixed(2);
    //         }
    //     });

    //     // Adiciona o formulário ao contêiner
    //     formContainer.appendChild(newForm);
    // }

    // // Atualiza o número total de formulários no formset
    // formCountElem.value = initialFormCount;

    // alert("Formulários de parcelas gerados com sucesso!");


    function compair(numero_parcelas, valor_total){
        const array_valor_parcelas = [];
        let all_parcela = 0
        for (let index = 0; index <= numero_parcelas-1; index++) {
            let valor_parcela = (valor_total/numero_parcelas).toFixed(2)
             
            all_parcela = parseFloat(all_parcela) + parseFloat(valor_parcela)
            if(index==numero_parcelas-1){
                array_valor_parcelas[index] = parseFloat(valor_parcela) + parseFloat(valor_total-all_parcela);
                console.log(array_valor_parcelas[index])
            }else {
                array_valor_parcelas[index] = valor_parcela;
                console.log(array_valor_parcelas[index])
            }
        }
        return array_valor_parcelas
    }