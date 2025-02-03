// Usando jQuery para facilitar o controle da visibilidade
document.addEventListener('DOMContentLoaded', function () {
    const interestType = document.getElementById('interest_type');
    const interestValueField = document.getElementById('id_interestValue');
    const interestPercentField = document.getElementById('id_interestPercent');
    const fineType = document.getElementById('fine_type');
    const fineValueField = document.getElementById('id_fineValue');
    const finePercentField = document.getElementById('id_finePercent');
    let TotalValue = document.getElementById('id_value');
    let value_edit = TotalValue.value;
    const TotalValue_default = TotalValue
    const defalt = TotalValue.value 

    data = document.getElementById('id_date_account').value
    dataa = document.getElementById('id_expirationDate').value
    console.log(dataa)
    
    const date = document.getElementById("id_date_account"); // data da conta
    console.log(date)
    
    const convertToDate = (dateStr) => {
        const [year, month, day ] = dateStr.split('-').map(num => parseInt(num, 10));
        return new Date(year, month - 1, day); // Mês no JavaScript começa do 0
    };

    // Pega o valor do input e remove espaços extras
    const inputDate = date.value.trim();

    // Converte a data inicial para um objeto Date
    const startDate = convertToDate(inputDate);

    // Verifica se a conversão foi bem-sucedida
    if (isNaN(startDate.getTime())) {
        console.error('Data inválida');
    } else {
    // Cria uma nova data para evitar modificar startDate
    const final_date = new Date(startDate);

    // Formata a data no formato "DD/MM/YYYY"
    date.value = `${final_date.getDate().toString().padStart(2, '0')}/` +
                 `${(final_date.getMonth() + 1).toString().padStart(2, '0')}/` +
                 `${final_date.getFullYear()}`;
} 
    // console.log(input.value)

    interestPercentField.addEventListener('change', function(){
        const edit = compair_interest_fine(defalt)
        TotalValue.value = edit
    })
    interestValueField.addEventListener('change', function(){
        const edit = compair_interest_fine(defalt)
        TotalValue.value = edit
    })
    finePercentField.addEventListener('change', function(){
        const edit = compair_interest_fine(defalt)
        TotalValue.value = edit
    })
    fineValueField.addEventListener('change', function(){
        const edit = compair_interest_fine(defalt)
        TotalValue.value = edit
    })

    function compair_interest_fine(defalt){
        let calc = 0
        value_edit = parseFloat(defalt)
        console.log(value_edit)

    // console.log('interestValueField.value:"' + interestValueField.value + '"')
    //     console.log('typeof(interestValueField.value):' + typeof(interestValueField.value))

    //     console.log('TotalValue_default:' + TotalValue_default)
    //     console.log('typeof(TotalValue_default):' + typeof(TotalValue_default))
    //     console.log('nao passou pelo primeiro if "if principal')
        
        value_edit = parseFloat(value_edit);
        // console.log('value_edit:' + value_edit)
        // console.log('typeof(value_edit):' + typeof(value_edit))

        // if (value_edit == TotalValue_default.value) {
            console.log('passou pelo primeiro if "if principal')
            if (interestPercentField.value != '' || interestPercentField.value != 0){ 
                if(finePercentField.value != '' || finePercentField.value != 0){
                    calc = calc + parseFloat(finePercentField.value)
                    }
                    calc = calc + parseFloat(interestPercentField.value)
                    console.log(parseFloat(calc/100))
                    console.log(parseFloat((calc/100)*value_edit))
                    console.log(parseFloat(TotalValue_default.value))
                value_edit = value_edit + parseFloat(((calc)/100)*value_edit);
            } else if (finePercentField.value != '' || finePercentField.value != 0) {
                if(interestPercentField.value != '' || interestPercentField.value != 0){
                    calc = calc + parseFloat(interestPercentField.value)  
                }
                    calc = calc + parseFloat(finePercentField.value)
                    value_edit = value_edit + parseFloat((calc/100)*value_edit);
            }
            
            
            if (interestValueField.value != '') {
                value_edit = value_edit + parseFloat(interestValueField.value);
            }
            
            if (fineValueField.value) {
                value_edit = value_edit + parseFloat(fineValueField.value);
            }
            return parseFloat(value_edit).toFixed(2)
        // }else {
        //     value_edit = parseFloat(defalt)
        //     return value_edit
        // }
    }


    // console.log(`"${finePercentField.value}"`)
    // console.log(`"${typeof(parseFloat(interestValueField.value))}"`)
    // console.log(`"${typeof(fineValueField.value)}"`)
    interestType.addEventListener('change',function() {
        if (interestType.value === 'percent') {
            interestPercentField.style.display = 'block'; // Mostrar o campo de porcentagem
            interestValueField.style.display = 'none';   // Esconder o campo de valor
            interestValueField.value = 0;   // Esconder o campo de valor
            TotalValue.value = compair_interest_fine(defalt)
        } else if (interestType.value === 'value') {
            interestValueField.style.display = 'block';   // Mostrar o campo de valor
            interestValueField.value = 0;   // Esconder o campo de valor
            interestPercentField.style.display = 'none';  // Esconder o campo de porcentagem
            interestPercentField.value = '';  // Esconder o campo de porcentagem
            TotalValue.value = compair_interest_fine(defalt)
            
        } else {
            interestValueField.style.display = 'none';    // Esconder ambos os campos
            interestPercentField.style.display = 'none';
        }
    })
    fineType.addEventListener('change',function() {
        if (fineType.value === 'percent') {
            finePercentField.style.display = 'block'; // Mostrar o campo de porcentagem
            fineValueField.style.display = 'none';   // Esconder o campo de valor
            fineValueField.value = 0;   // valor inicial
            TotalValue.value = compair_interest_fine(defalt)
        } else if (fineType.value === 'value') {
            fineValueField.style.display = 'block';   // Mostrar o campo de valor
            fineValueField.value = 0;   // valor inicial
            finePercentField.style.display = 'none';  // Esconder o campo de porcentagem
            finePercentField.value = '';  // Esconder o campo de porcentagem
            TotalValue.value = compair_interest_fine(defalt)

        } else {
            fineValueField.style.display = 'none';    // Esconder ambos os campos
            finePercentField.style.display = 'none';
        }
    })
    // Função para exibir o campo correto
    // document.getElementById() {
    // }
    
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
    toggleFields_Interest();
    toggleFields_Fine();
})