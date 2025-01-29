function addItemCompra(){
    const formset = document.getElementById("itens-container");
    const formCountElem = document.getElementById("id_compraitem_set-TOTAL_FORMS");

    if(!formCountElem){
        console.log("Elemento TOTAL_FORMS de VendaItem não encontrado");
        return;
    }

    const formCount = formCountElem.ariaValueMax;
    const emptyFormTemplate = document.getElementById("empty-form-template");

    if(!emptyFormTemplate){
        console.error("Template de formulário vazio (empty-form-template")
        return;
    }

    const newForm = emptyFormTemplate.content.cloneNode(true);

    newForm.querySelectorAll('input, select').forEach(input => {
        input.name = input.name.replace('__prefix__', formCount);
        input.id = input.id.replace('__prefix__', formCount);
        input.value = ''; // Limpa os valores dos campos
    })

    formCountElem.value = parseInt(formCount) + 1;
}
