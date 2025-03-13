
    document.addEventListener("DOMContentLoaded", function () {
        document.querySelectorAll(".status-select").forEach(select => {
            select.addEventListener("change", function () { 
                let idVenda = this.dataset.vendaId; 

                if (this.value != "Pendente") {
                    let confirmar = confirm(`Realmente deseja o status do produto para ENTREGUE?`);
                    if (confirmar) {
                        let form = this.closest("form");  
                        form.submit(); // Envia o formulário
                    } else {
                        this.value = "Pendente";
                    }
                }
            });
        });
    });

