document.addEventListener('DOMContentLoaded', function () {
    const tr_none = document.getElementById('tr_one')
    const th_none = document.getElementById('th_one')
    const templatenone = document.getElementById('id_paymentmethod_accounts_set-0-DELETE')
    const header = document.getElementById('installment')
    
    //escondendo campos de template base e opção de remoção
    templatenone.value = 1
    header.style = 'display:none;'
    tr_none.style = 'display:none;'
    th_none.style = 'display:none;'

    
    let part = 2
    // let part = 0
    // let variavel = null;
    const installments = document.getElementById('generate')//gerador de parcelas
    installments.addEventListener('click', () => {
        const value_initial = document.getElementById("id_paymentmethod_accounts_set-INITIAL_FORMS");
        const TOTAL_FORMS = document.getElementById("id_paymentmethod_accounts_set-TOTAL_FORMS");//TOTAL FORMS
        const days_installment_Range = document.getElementById('installment_Range')
        const installmentRange = document.getElementById('id_numberOfInstallments')
        const dateInitsemvalor = document.getElementById("id_date_init"); // Data de início das faturas
        const table = document.getElementById('installment') // tabela das parcelas
        const payment_method = document.getElementById('account') // select de forma de pagamento
        
        header.style.removeProperty('display')

        clear()
        // console.log('value initial: ' + value_initial.value)
        // console.log('total forms: ' + TOTAL_FORMS.value)
        // console.log('tipo de dados do total forms: ' + typeof(TOTAL_FORMS.value))
        // console.log('tabela das parcelas: ' + table.outerHTML) // mostrar a tag inteira
        console.log('Total de parcelas: ' + TOTAL_FORMS.value) // mostrar a tag inteira
        
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

        console.log('ate o momento foi clicado o botao de gerar as parcelas: FUNÇÃO NOVA')
        fragmento = document.createDocumentFragment()
        const valueOfinstallments = compair(numberOfInstallments, totalValue);
        for (let index = 0; index < installmentRange.value; index++) {           
            let parcela = document.createElement('tr') // linha
            let row_expirationDate = document.createElement('td')     // coluna
            let row_days = document.createElement('td')     // coluna
            let row_value = document.createElement('td')     // coluna

            //-------------------------------//
            //Selecionando Forma de Pagamento//
            let original = document.getElementById("account"); 
            let forma_pagamento = original.cloneNode(true); // clona com conteúdo interno
            forma_pagamento.id = `id_paymentmethod_accounts_set-${parseInt(TOTAL_FORMS.value)+index}-forma_pagamento` // ID único

            // let forma_pagamento = document.createElement('select')
            // forma_pagamento.id = `id_paymentmethod_accounts_set-${parseInt(TOTAL_FORMS.value)+index}-forma_pagamento`
            // forma_pagamento.className = 'form-control row'

            // console.log(typeof(TOTAL_FORMS))
            
            
            // -------------------------//
            expirationDate = document.createElement('input')
            // expirationDate.style.setProperty('margin-right', "5px", 'important')
            expirationDate.id = `id_paymentmethod_accounts_set-${parseInt(TOTAL_FORMS.value)+index}-expirationDate`
            expirationDate.className = 'form-control row'
            // Calcula a data da parcela//
            days_expirationDate = (parseInt(installmentRange.value,10))
            new_date_expirationDate = startDate.setDate(startDate.getDate() + days_expirationDate);
            final_date_expirationDate = new Date(new_date_expirationDate)
            expirationDate.value = `${final_date_expirationDate.getDate().toString().padStart(2, '0')}/${(final_date_expirationDate.getMonth() + 1).toString().padStart(2, '0')}/${final_date_expirationDate.getFullYear()} `  
            div_input_group_date = document.createElement('div')
            div_input_group_date.className = 'input-group date'
            $(document).ready(function () {
                $('.input-group.date input').datepicker({
                    format: 'dd/mm/yyyy',
                    autoclose: true,
                });
            });
            // div_input_group_date.setAttribute('data-provide', 'datepicker')
            div_input_group_addon = document.createElement('div')
            div_input_group_addon.className = 'input-group addon'
            span_glyphicon_glyphicon_th = document.createElement('span') 
            span_glyphicon_glyphicon_th.className = 'glyphicon glyphicon-th'
            
            div_input_group_date.appendChild(expirationDate)
            div_input_group_date.appendChild(div_input_group_addon)
            div_input_group_addon.appendChild(span_glyphicon_glyphicon_th)
            
            
            // -------------------------//
            //Calcula a variação de dias entre parcelas
            days = document.createElement('input')
            days.id = `id_paymentmethod_accounts_set-${parseInt(TOTAL_FORMS.value)+index}-days`
            days.className = 'form-control row'
            days.value = days_installment_Range.value*(index+1);
            // console.log(days_installment_Range.value*(index+1))

            //-------------------------//
            //Calcula o Valor dividido igualmente  
            value = document.createElement('input')
            value.id = `id_paymentmethod_accounts_set-${parseInt(TOTAL_FORMS.value)+index}-value`
            value.className = 'form-control row'
            value.value = valueOfinstallments[index];
            
            row_expirationDate.appendChild(div_input_group_date)
            row_days.appendChild(days)
            row_value.appendChild(value)
            // console.log(row_expirationDate.outerHTML)

            parcela.appendChild(forma_pagamento)
            parcela.appendChild(row_expirationDate)
            parcela.appendChild(row_days)
            parcela.appendChild(row_value)
            fragmento.appendChild(parcela)
        }
        table.appendChild(fragmento)
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
    function clean(TOTAL_FORMS){
        
        
    }
})