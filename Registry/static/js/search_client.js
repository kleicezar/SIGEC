
const input = document.getElementById("searchInput");
const resultsContainer = document.getElementById("results");
const messageContainer = document.getElementById("messageContainer");  // Elemento onde a mensagem será exibida

input.addEventListener("input", () => {
    const query = input.value;

    fetch(`/b-clt/?query=${encodeURIComponent(query)}`)
    .then(response => {
        // Verifica se a resposta é JSON
        if (response.ok && response.headers.get('Content-Type').includes('application/json')) {
            return response.json();
        } else {
            throw new Error('Resposta não é JSON');
        }
    })
    .then(data => {
        resultsContainer.innerHTML = ""; // Limpa os resultados anteriores
        messageContainer.innerHTML = ""; // Limpa qualquer mensagem anterior

        if (data.message) {
            // Exibe a mensagem de erro ou sucesso
            messageContainer.innerHTML = `<p>${data.message}</p>`;
        }
        
        if (data.clientes.length > 0) {
            data.clientes.forEach(cliente => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${cliente.id}</td>
                    <td>${cliente.name || "N/A"}</td>
                    <td>${cliente.WorkPhone || "N/A"}</td>
                    <td>${cliente.PersonalPhone || "N/A"}</td>
                    <td></td>
                `;
                resultsContainer.appendChild(row);
            });
        }
    })
    .catch(error => console.error("Erro ao buscar clientes:", error));
});
