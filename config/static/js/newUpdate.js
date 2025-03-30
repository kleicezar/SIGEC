document.addEventListener('DOMContentLoaded', function() {
    // Obter o valor do campo pamonha
    var person = document.getElementById('id_pessoa');
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

    const productsFields = document.querySelectorAll('[id$="product"]');
    productsFields.forEach(function(productsField){
        const query = productsField.value;
        
        var idSearchField = productsField.closest('td').querySelector('.idSearch');
        console.log(idSearchField)
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
});