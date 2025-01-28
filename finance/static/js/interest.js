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
    const formCountElem = document.getElementById("id_paymentmethod_accountspayable_set-TOTAL_FORMS");
    const installments = document.getElementById('generate')//gerador de parcelas
    
    
    installments.addEventListener('click', () => {
        const itensPaymentMethodContainer = formContainer.querySelectorAll("item-form");
        itensPaymentMethodContainer.forEach(item=>{
            console.log('removido')
        formContainer.removeChild(item)
        })
        const numberOfInstallments = parseInt(document.getElementById("id_numberOfInstallments").value); // Número de parcelas
        const dateInit = document.getElementById("id_date_init"); // Data de início das faturas
        const installment_Range = parseInt(document.getElementById("installment_Range").value); // Intervalo entre faturas (em dias)
        const valueOfInstallments = parseFloat(document.getElementById("id_valueOfInstallments").value); // Valor de cada parcela
        const totalValue = parseFloat(document.getElementById("id_totalValue").value); // Valor de cada parcela
        // Validações básicas
        console.log(numberOfInstallments)
        console.log(dateInit.value)
        console.log(installment_Range)
        console.log(valueOfInstallments)
        console.log(totalValue)

        const selectedDate = new Date(dateInit.value);
        console.log(selectedDate)
        if (isNaN(numberOfInstallments) || isNaN(installment_Range) || isNaN(valueOfInstallments) || isNaN(selectedDate.getTime())) {
            alert("Por favor, preencha todos os campos corretamente. BY: kleitin");
            return;
        }
        
        for (let index = 0; index < numberOfInstallments - 1; index++) {
            const emptyFormTemplate = document.getElementById('empty-payment-method-form');
            if (!emptyFormTemplate) {
                console.error("Template de formulário vazio (empty-payment-method-form) não encontrado!");
                return;
            }
            const newForm = emptyFormTemplate.content.cloneNode(true);
            // Atualiza os campos do formulário clonado
            newForm.querySelectorAll("input, select").forEach(async (input) => {
                input.name = input.name.replace("__prefix__", formCountElem.value);
                input.id = input.id.replace("__prefix__", formCountElem.value);
                console.log(input.name)
                // Preenche os valores iniciais nos campos do formulário
                if (input.name.includes("-expirationDate")) {
                    // Calcula a data da parcela
                    const installmentDate = new Date(dateInit);
                    // console.log('-----------------------')
                    // console.log(installmentDate)
                    input.value = installmentDate.setDate(installmentDate.getDate() + installment_Range * index);

                    //------------------------

        
                    //------------------------

                    }else if (input.name.includes("-value")) {
                        // Define o valor da parcela
                        input.value = valueOfInstallments.toFixed(2);
                    
                    }else if (input.name.includes("-days")) {
                        // Define os dias entre as parcelas
                        input.value = installment_Range;
                    }
                    // Adiciona o formulário ao contêiner
            // console.log(newForm)
            await formContainer.appendChild(newForm);
            })
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
