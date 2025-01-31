// TOTAL VALOR DE FORMULARIO DE ITENS;
const totalValueField = document.getElementById("id_total_value");
const totalProductsField = document.getElementById("id_service_total");
const discountTotalField = document.getElementById("id_discount_total");
const itemsContainer = document.getElementById("itens-container");
console.log('agora')
let serviceOptionsContainer = document.getElementById("options_services-0");
let serviceOptionsCell = serviceOptionsContainer.parentElement;
serviceOptionsCell.style.display = "none";  
const serviceInfoParagraph = document.createElement("p");

document.querySelectorAll(".suggest").forEach(el => el.style.display = "none");
console.log('oura')
// Listener para garantir que apenas uma sugestão apareça de cada vez
document.addEventListener("focusin", (event) => {
    if (event.target.tagName === "INPUT") {
        document.querySelectorAll(".suggest").forEach(el => el.style.display = "none");
    }
});

// Atualiza o total do desconto, valor total e total de produtos ao clicar no botão de deletar
itemsContainer.addEventListener("click", (event) => {
    if (event.target.tagName === 'BUTTON') {
        const itemForms = itemsContainer.querySelectorAll(".item-form");
        updateTotal(itemForms);
    }
});

itemsContainer.addEventListener("input", (event) => {
    if (event.target.tagName === 'INPUT') {

        const itemForms = itemsContainer.querySelectorAll(".item-form");
        const modifiedInput = event.target;
        const itemForm = modifiedInput.closest(".item-form");
        const itemFormInputs = itemForm.querySelectorAll("input");

        // Monitorando o campo ID_PRODUCT
        if (modifiedInput.id.startsWith("idService")) {
            let tbody = modifiedInput.parentElement.parentElement.parentElement;
            let td = tbody.querySelector(".tre").querySelector("td");
            let productsContainer = td.querySelector("div");
            let productValueInput;
            let searchProductInput;
            let priceUnitValueInput;

            itemFormInputs.forEach((input) => {
                const fieldType = input.id;
                if (fieldType.endsWith('service')) {
                    productValueInput = input;
                } else if (fieldType.startsWith("idService")) {
                    searchProductInput = input;
                } else if (fieldType.endsWith('preco')) {
                    priceUnitValueInput = input;
                }
            });

            if (modifiedInput.value.length >= 1) {
                let optionsIndex = 0;
                const query = modifiedInput.value;

                fetch(`/buscar_servicos/?query=${encodeURIComponent(query)}`)
                    .then(response => {
                        if (response.ok && response.headers.get('Content-Type').includes('application/json')) {
                            return response.json();
                        } else {
                            throw new Error('Resposta não é JSON');
                        }
                    })
                    .then(data => {
                        productsContainer.innerHTML = "";
                        serviceInfoParagraph.textContent = "ID - NOME";
                        serviceInfoParagraph.className = "title-service text-center";
                        productsContainer.style.width = "300px";
                        productsContainer.appendChild(serviceInfoParagraph);

                        if (data.servicos.length > 0) {
                            data.servicos.forEach(servico => {
                                td.style.display = "block";
                                let serviceButton = document.createElement("button");
                                serviceButton.className = "btn btn-outline-secondary form-control x mb-2";
                                serviceButton.type = "button";
                                serviceButton.id = `option-service-${optionsIndex}`;
                                serviceButton.textContent = `${servico.id} - ${servico.name_Service}`;

                                let titleService = td.querySelector('.title-service');
                                titleService.insertAdjacentElement('afterend', serviceButton);

                                const button = td.querySelector(".x");
                                button.addEventListener("click", () => {
                                    productValueInput.value = servico.id;
                                    searchProductInput.value = button.textContent;
                                    priceUnitValueInput.value = servico.price;
                                    td.style.display = "none";
                                });

                                optionsIndex += 1;
                            });
                        }
                    });
            } else {
                td.style.display = "none";
            }
        }

        updateTotal(itemForms);
    }
});

const serviceInputs = document.querySelectorAll('input[type="hidden"][name$="-service"]')
serviceInputs.forEach(serviceInput=>{
    console.log('fdddddddd')
    const parentElement = serviceInput.parentElement;
    const textInput = parentElement.querySelector('input[type="text"]');

    if(serviceInput.value!=''){
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
            console.log(data)
            textInput.value = `${data.servico[0].id} - ${data.servico[0].name_Service}`;
            console.log('ofdasfdas')
        });

    }
    
})
function updateTotal(itemForms, numServices = 0, totalPrice = 0, totalValue = 0) {
    let total = 0;
    let price = 0;
    itemForms.forEach(itemForm => {
        const style = window.getComputedStyle(itemForm);
        let quantity = 0;
        let inputs = itemForm.querySelectorAll("input");

        if (style.display !== 'none') {
            inputs.forEach(input => {
                if (input.id.endsWith("quantidade")) {
                    totalValue += price * Number(quantity);
                } else if (input.id.endsWith("preco")) {
                    price = input.value;
                    totalValue += Number(price);
                }
            });
            total += 1;
        }
    });

    discountTotalField.value = 11;
    totalProductsField.value = 20;
    totalValueField.value = totalValue;
}

const productInputFields = document.querySelectorAll('input[type="hidden"][name$="-product"]');

productInputFields.forEach(inputProduct => {
    let container = inputProduct.parentElement;
    let inputText = container.querySelector('input[type="text"]');

    if (inputProduct.value !== '') {
        const query = inputProduct.value;
        fetch(`/get_product_id/?query=${encodeURIComponent(query)}`)
            .then(response => {
                if (response.ok && response.headers.get('Content-Type').includes('application/json')) {
                    return response.json();
                } else {
                    throw new Error('Resposta não é JSON');
                }
            })
            .then(data => {
                inputText.value = `${data.produto[0].product_code} - ${data.produto[0].description}`;
            });
    }
});

const clientInput = document.getElementById("idSearch");
let autoCompleteInverted = false;
const personField = document.getElementById("id_pessoa") || document.getElementById("id_fornecedor");

if (personField.value !== "") {
    autoCompleteInverted = !autoCompleteInverted;
}

if (autoCompleteInverted) {
    const query = personField.value;
    fetch(`/buscar_pessoas/?query=${encodeURIComponent(query)}`)
        .then(response => {
            if (response.ok && response.headers.get('Content-Type').includes('application/json')) {
                return response.json();
            } else {
                throw new Error('Resposta não é JSON');
            }
        })
        .then(data => {
            data.clientes.forEach(cliente => {
                clientInput.value = `${cliente.id} - ${cliente.name}`;
            });
        });
}

let optionsContainerClient = document.getElementById("options-1");
let clientOptionsCell = optionsContainerClient.parentElement;
clientOptionsCell.style.display = "none";

clientInput.addEventListener("input", () => {
    clientOptionsCell.style.display = "none";

    if (clientInput.value.length >= 1 && clientInput.value.trim() !== "") {
        let optionsIndex = 0;
        const query = clientInput.value;

        fetch(`/buscar_pessoas/?query=${encodeURIComponent(query)}`)
            .then(response => {
                if (response.ok && response.headers.get('Content-Type').includes('application/json')) {
                    return response.json();
                } else {
                    throw new Error('Resposta não é JSON');
                }
            })
            .then(data => {
                optionsContainerClient.innerHTML = '';
                serviceInfoParagraph.textContent = "ID - CLIENTE";
                serviceInfoParagraph.id = "title-client";
                serviceInfoParagraph.className = "text-center";
                optionsContainerClient.style.width = "300px";
                optionsContainerClient.appendChild(serviceInfoParagraph);

                if (data.clientes.length > 0) {
                    data.clientes.forEach(cliente => {
                        if (data.clientes.length <= query.length) {
                            clientOptionsCell.style.display = "block";
                            let selectClientButton = document.createElement("button");
                            selectClientButton.className = "btn btn-outline-secondary form-control mb-2";
                            selectClientButton.id = `option-${optionsIndex}`;
                            selectClientButton.textContent = `${cliente.id} - ${cliente.name}`;
                            selectClientButton.type = "button";

                            let titleClient = document.getElementById("title-client");
                            titleClient.insertAdjacentElement('afterend', selectClientButton);

                            selectClientButton.addEventListener("click", () => {
                                clientInput.value = selectClientButton.textContent;
                                personField.value = `${cliente.id}`;
                                clientOptionsCell.style.display = "none";
                            });

                            optionsIndex += 1;
                        }
                    });
                }
            });
    } else {
        clientOptionsCell.style.display = "none";
    }
});
