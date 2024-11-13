// Script para adicionar novos itens dinamicamente
function addItem() {
    // Obtém o container onde os itens serão adicionados
    const container = document.getElementById('itens-container');

    // Obtém o template do formulário vazio
    const template = document.getElementById('empty-form-template');
    const newForm = template.content.cloneNode(true);  // Clona o formulário vazio

    // Ajusta o número total de formulários no management_form
    const totalForms = document.querySelector('#id_form-TOTAL_FORMS');
    totalForms.value = parseInt(totalForms.value) + 1;

    // Adiciona o novo formulário ao container
    container.appendChild(newForm);
}