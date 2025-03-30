// TOTAL VALOR DE FORMULÁRIO DE ITENS
const totalValueInput = document.getElementById("id_total_value");
const totalProductsInput = document.getElementById("id_product_total");
const totalDiscountInput = document.getElementById("id_discount_total");
const itemsContainer = document.getElementById("itens-container");

const productTitle = document.createElement("p");

itemsContainer.addEventListener("click", (event) => {
    if (event.target.tagName === 'BUTTON') {
        const itemForms = itemsContainer.querySelectorAll(".item-form");
        updateTotals(itemForms);
    }
});


itemsContainer.addEventListener("input", (event) => {
  
    if (event.target.tagName === 'INPUT') {
        const modifiedInput = event.target;
        const itemForm = modifiedInput.closest(".item-form");
        const inputs = itemForm.querySelectorAll("input");

        let productInput, quantityInput, discountInput, totalPriceInput, unitPriceInput, searchProductInput;
        inputs.forEach(input => {
            const fieldType = input.id;
            if (fieldType.endsWith('product') || fieldType.endsWith('produto') || fieldType.endsWith('service')) {
                productInput = input;
            } else if (fieldType.endsWith('quantidade')) {
                quantityInput = input;
            } else if (fieldType.endsWith('preco_unitario')) {
                unitPriceInput = input;
            } else if (fieldType.endsWith('discount')) {
                discountInput = input;
            } else if (fieldType.endsWith('price_total')) {
                totalPriceInput = input;
            } else if (fieldType.startsWith("idProduct")) {
                searchProductInput = input;
            }
        });

        // Monitorar o campo de produto
       

        if (discountInput && quantityInput && unitPriceInput) {
            if (discountInput.value != 0) {
                totalPriceInput.value = ((unitPriceInput.value - ((discountInput.value / 100) * unitPriceInput.value)) * quantityInput.value).toFixed(2);
            } else {
                totalPriceInput.value = (unitPriceInput.value * quantityInput.value).toFixed(2);
            }
        }
        updateTotals(itemsContainer.querySelectorAll(".item-form"));
    }
});
totalValue = document.getElementById("id_totalValue");
function updateTotals(itemForms) {
    let totalSemDesconto = 0;
    let totalComDesconto = 0;
    let totalProdutos = 0;

    itemForms.forEach(itemForm => {
        if (window.getComputedStyle(itemForm).display !== 'none') {
            const inputs = itemForm.querySelectorAll("input");
            let quantidade = 0, precoUnitario = 0, desconto = 0, totalItem = 0;

            inputs.forEach(input => {
                if (input.id.endsWith("quantidade")) {
                    quantidade = Number(input.value) || 0;
                } else if (input.id.endsWith("preco_unitario")) {
                    precoUnitario = Number(input.value) || 0;
                } else if (input.id.endsWith("discount")) {
                    desconto = Number(input.value) || 0;
                } else if (input.id.endsWith("price_total")) {
                    totalItem = Number(input.value) || 0;
                }
            });

            let subtotalSemDesconto = precoUnitario * quantidade;
            let subtotalComDesconto = subtotalSemDesconto * (1 - desconto / 100);

            totalSemDesconto += subtotalSemDesconto;
            totalComDesconto += subtotalComDesconto;
            totalProdutos += quantidade;
        }
        totalValue.value = totalComDesconto.toFixed(2);
    });

    let percentualDesconto = totalSemDesconto > 0
        ? ((1 - totalComDesconto / totalSemDesconto) * 100).toFixed(2)
        : 0;

    totalDiscountInput.value = percentualDesconto;
    totalProductsInput.value = totalProdutos;
    totalValueInput.value = totalComDesconto.toFixed(2);
}

const itemForms = document.querySelectorAll('.item-form');
let index = 0;

// EDIÇÃO DE VENDA - INVERTER A LÓGICA
let isAutoCompleteInverted = false;
const personInput = document.getElementById("id_pessoa") || document.getElementById("id_fornecedor");

let productInputs = document.querySelectorAll('input[type="hidden"][name$="-product"]');
if (productInputs.length === 0) {
    productInputs = document.querySelectorAll('input[type="hidden"][name$="-produto"]');
}

productInputs.forEach(productInput => {
    const parentElement = productInput.parentElement;
    const textInput = parentElement.querySelector('input[type="text"]');

    if (productInput.value !== '') {
        console.log('Fetching product data');
        const query = productInput.value;
        fetch(`/get_product_id/?query=${encodeURIComponent(query)}`)
            .then(response => {
                if (response.ok && response.headers.get('Content-Type').includes('application/json')) {
                    return response.json();
                } else {
                    throw new Error('Response is not JSON');
                }
            })
            .then(data => {
                textInput.value = `${data.produto[0].product_code} - ${data.produto[0].description}`;
               
            });
    }
});





// Função de monitoramento de alterações nos itens
document.addEventListener("DOMContentLoaded", function () {
    const itemsContainer = document.querySelector("#itens-container");
    if (itemsContainer) {
        // Monitorar mudanças nos selects dentro do container
        itemsContainer.addEventListener("change", function (event) {
            if (event.target.matches("[id^='id_vendaitemservice_set-'][id$='-service']")) {
                const selectElement = event.target;
                const formContainer = selectElement.closest(".item-form");

                if (formContainer) {
                    const priceInput = formContainer.querySelector("[id^='id_vendaitemservice_set-'][id$='-preco']");
                    const serviceInput = formContainer.querySelector("[id^='id_vendaitemservice_set-'][id$='-service']");
                    const serviceText = serviceInput.textContent;

                    
                    fetch(`/buscar_servicos/?query=${encodeURIComponent(serviceText)}`)
                        .then(response => {
                            if (response.ok && response.headers.get('Content-Type').includes('application/json')) {
                                return response.json();
                            } else {
                                throw new Error('Response is not JSON');
                            }
                        })
                        .then(data => {
                            if (priceInput) {
                                priceInput.value = data.servico[0].value_Service;
                            }
                        });
                }
            }
        });

        // Monitorar cliques nos botões de deletar dentro do container
        itemsContainer.addEventListener("click", function (event) {
            if (event.target.matches(".delete")) {
                const button = event.target;
                const formContainer = button.closest(".item-form");

                if (formContainer) {
                    const deleteInput = formContainer.querySelector("[id^='id_vendaitemservice_set-'][id$='-DELETE']");
                    if (deleteInput) {
                        deleteInput.value = "on";
                        
                    }
                }
            }
        });
    }
});
