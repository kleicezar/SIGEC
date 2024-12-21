
const input = document.getElementById("searchInput");
const resultsContainer = document.getElementById("results");
const messageContainer = document.getElementById("messageContainer");  // Elemento onde a mensagem será exibida
// const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

input.addEventListener("input", () => {
    const query = input.value;

    fetch(`/b-prsn/?query=${encodeURIComponent(query)}`)
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
                    <td>
                        <a href="/prsn/upt/${cliente.id}">
                            <button class="btn" style="background-color: #117027;color: white;">Editar</button>
                        </a>
                        <form action="/prsn/del/${cliente.id}" method="POST" style="display:inline-block;">
                            <input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">
                            <button type="submit" class="btn" style="background-color: rgb(139, 16, 16);color: white;" onclick="return confirm('Tem certeza que deseja deletar este cliente?')">Deletar</button>
                        </form>

                    </td>
                `;
                resultsContainer.appendChild(row);
            });
        }
    })
    .catch(error => console.error("Erro ao buscar clientes:", error));
});

// const config = document.getElementById('config');
// const updateUrl = config.dataset.updateUrl;
// const deleteUrl = config.dataset.deleteUrl;
//bateria 75 650,00 consumidor final
// // Substituir 0 pelo cliente.id ao gerar as URLs
// row.innerHTML = `
//     <td>${cliente.id}</td>
//     <td>${cliente.name || "N/A"}</td>
//     <td>${cliente.WorkPhone || "N/A"}</td>
//     <td>${cliente.PersonalPhone || "N/A"}</td>
//     <td>
//         <form action="${updateUrl.replace('0', cliente.id)}" method="POST" style="display:inline-block;">
//             <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
//             <button type="submit" class="btn" style="background-color: #117027;color: white;">Editar</button>
//         </form>
//         <form action="${deleteUrl.replace('0', cliente.id)}" method="POST" style="display:inline-block;">
//             <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
//             <button type="submit" class="btn" style="background-color: rgb(139, 16, 16);color: white;" onclick="return confirm('Tem certeza que deseja deletar este cliente?')">Deletar</button>
//         </form>
//     </td>
// `;

{/* <td>
<a href="/prsn/upt/${cliente.id}">
    <button class="btn" style="background-color: #117027;color: white;">Editar</button>
</a>
<form action="/prsn/del/${cliente.id}" method="POST" style="display:inline-block;">
    <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
    <button type="submit" class="btn" style="background-color: rgb(139, 16, 16);color: white;" onclick="return confirm('Tem certeza que deseja deletar este cliente?')">Deletar</button>
</form>
</td> */}
