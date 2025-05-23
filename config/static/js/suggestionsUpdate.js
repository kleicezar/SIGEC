document.addEventListener('DOMContentLoaded', function() {
    // Obter o valor do campo
    var person = document.getElementById('id_pessoa')||document.getElementById('id_fornecedor');
    if (person){
        var inputField = person.closest('td').querySelector('.idSearch');
        const query = person.value;
        fetch(`/buscar_pessoas/?query=${encodeURIComponent(query)}`)
        .then(response => {
            if (response.ok && response.headers.get('Content-Type').includes('application/json')) {
                return response.json();
            } else {
                throw new Error('Resposta não é JSON');
            }
        })
        .then(data => {
            console.log(data);
            data.clientes.forEach(cliente=>{
                inputField.value = `${cliente.id} - ${cliente.name}`
            })
        });
    }

    const productsFields = document.querySelectorAll('[id$="product"], [id$="produto"]');
    productsFields.forEach(function(productsField){
        const query = productsField.value;
        
        var idSearchField = productsField.closest('td').querySelector('.idSearch');
        if(idSearchField){
            fetch(`/get_product_id/?query=${encodeURIComponent(query)}`)
                .then(response => {
                    if (response.ok && response.headers.get('Content-Type').includes('application/json')) {
                        return response.json();
                    } else {
                        throw new Error('Resposta não é JSON');
                    }
        })
        .then(data => {
            idSearchField.value = `${data.produto[0].product_code} - ${data.produto[0].description}`;
        });
        }
    })
    const serviceInputs = document.querySelectorAll('input[type="hidden"][name$="-service"]')
    serviceInputs.forEach(serviceInput=>{
    const parentElement = serviceInput.parentElement;
    const textInput = parentElement.querySelector('input[type="text"]');

    if(serviceInput.value != ''){
        console.log('Fetching service data');
        const query = serviceInput.value;
        console.log(query);
        fetch(`/get_service_id/?query=${encodeURIComponent(query)}`)
        .then(response => {
            if (response.ok && response.headers.get('Content-Type').includes('application/json')) {
                return response.json();
            } else {
                throw new Error('Response is not JSON');
            }
        })
        .then(data=>{
            textInput.value = `${data.servico[0].id} - ${data.servico[0].name_Service}`;
        });

    }
    
})
});