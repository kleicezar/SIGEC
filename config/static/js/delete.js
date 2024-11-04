    // Obter o modal
    var modal = document.getElementById("myModal");
    var btn = document.getElementById("openModal");
    var span = document.getElementById("closeModal");

    // Quando o botão é clicado, abre o modal
    btn.onclick = function() {
        modal.style.display = "block";
    }
    // Quando o usuário clica no <span> (x), fecha o modal
    span.onclick = function() {
        modal.style.display = "none";
    }

    // Quando o usuário clica fora do modal, fecha-o
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    $(document).ready(function() {
        $('.delete-button').on('click', function() {
            const id = $(this).data('id');
            const url = `/Stn/dlt/${id}/`; // Ajuste o caminho conforme necessário

            if (confirm("Tem certeza que deseja deletar esta situação?")) {
                $.ajax({
                    type: "POST",
                    url: url,
                    data: {
                        csrfmiddlewaretoken: '{{ csrf_token }}'
                    },
                    success: function(response) {
                        if (response.success) {
                            // Remove a linha da tabela ou atualiza a interface
                            alert("Situação deletada com sucesso!");
                            location.reload(); // Atualiza a página
                        }
                    },
                    error: function() {
                        alert("Erro ao deletar a situação.");
                    }
                });
            }
        });
    });