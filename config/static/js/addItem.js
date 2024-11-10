// Script para adicionar novos itens dinamicamente
// function addItem() {
//     // Obtém o container onde os itens serão adicionados
//     const container = document.getElementById('itens-container');

//     // Obtém o template do formulário vazio
//     const template = document.getElementById('empty-form-template');
//     const newForm = template.content.cloneNode(true);  // Clona o formulário vazio

//     // Ajusta o número total de formulários no management_form
//     const totalForms = document.querySelector('#id_form-TOTAL_FORMS');
//     totalForms.value = parseInt(totalForms.value) + 1;

//     // Adiciona o novo formulário ao container
//     container.appendChild(newForm);
// }


// function addItem() {
//     const container = document.getElementById('itens-container');
//     const formset = {{ formset.management_form|safe }};
//     const newForm = formset.forms[0].cloneNode(true);  // Clona o primeiro formulário
//     container.appendChild(newForm);  // Adiciona ao container
// }  





// document.addEventListener('DOMContentLoaded', function () {
//     // let itemCount = {{ venda_items|length }};  // Conta o número de itens renderizados inicialmente
//     let itemCount = document.getElementById('itemCount').getAttribute('data-count');
//     console.log(itemCount);
//     const addItemButton = document.getElementById('addItemButton');
//     const itemsContainer = document.getElementById('itemsContainer');
    
//     // Array com todos os produtos (será usado para preencher os selects)
//     // const products = [
//     //     {% for product in products %}
//     //         { id: {{ product.id }}, descricao: "{{ product.descricao }}" },
//     //     {% endfor %}
//     // ];

//     addItemButton.addEventListener('click', function() {
//         itemCount++;
        
//         // Cria um novo campo para o item
//         const newItemDiv = document.createElement('div');
//         newItemDiv.classList.add('itemForm');
//         newItemDiv.innerHTML = `{{ item_form.as_p }}`;
//         itemsContainer.appendChild(newItemDiv);
//     });
// });

// <h4>Item ${itemCount}</h4>
//             <div>
//                 <label for="id_item_${itemCount}-product">Produto:</label>
//                 <select name="item_${itemCount}-product" required>
//                     <option value="">Escolha um Produto</option>
//                     ${products.map(product => `<option value="${product.id}">${product.descricao}</option>`).join('')}
//                 </select>
//             </div>
//             <div>
//                 <label for="id_item_${itemCount}-quantidade">Quantidade:</label>
//                 <input type="number" name="item_${itemCount}-quantidade" required>
//             </div>
//             <div>
//                 <label for="id_item_${itemCount}-preco_unitario">Preço Unitário:</label>
//                 <input type="number" step="0.01" name="item_${itemCount}-preco_unitario" required>
//             </div>



// API DE CEP


// function copiarValorParaCampos(origemId, destinosIds) {
//     const valor = document.getElementById(origemId).value;
//     destinosIds.forEach(destinoId => {
//         document.getElementById(destinoId).value = valor;
//     });
// }

// // Uso da função no evento "blur"
// document.getElementById("input-cep").addEventListener("blur", function () {
//     copiarValorParaCampos("input-cep", ["inputDestino1", "inputDestino2"]);
// });