document.addEventListener('DOMContentLoaded', function() {
    // Obter o valor do campo
    let id_client = document.getElementById('id_pessoa')
    let id_supplier = document.getElementById('id_fornecedor');
    if (id_client){
        var inputField = id_client.closest('td').querySelector('.idSearch');
        const query = id_client.value;
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
    else{
        var inputField = id_supplier.closest('td').querySelector('.idSearch');
        const query = id_supplier.value;
        fetch(`/buscar_fornecedores/?query=${encodeURIComponent(query)}`)
        .then(response => {
            if (response.ok && response.headers.get('Content-Type').includes('application/json')) {
                return response.json();
            } else {
                throw new Error('Resposta não é JSON');
            }
        })
        .then(data => {
            console.log(data);
            data.fornecedores.forEach(fornecedor=>{
                inputField.value = `${fornecedor.id} - ${fornecedor.name}`
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