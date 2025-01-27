const input = document.getElementById("searchInput");
const resultContainer = document.getElementById("results");
const messageContainer = document.getElementById("messageContainer");
const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
let paginationContainer = document.getElementById("paginationContainer");
input.addEventListener("input",()=>{
    const query = input.value;
    fetch(`/venda/buscar_vendas/?query=${encodeURIComponent(query)}`)
    .then(response=>{
        if(response.ok && response.headers.get('Content-Type').includes('application/json')){
            return response.json();
        } else{
            throw new Error('Resposta não é JSON')
        }
    })
    .then(data=>{
        resultContainer.innerHTML="";
        messageContainer.innerHTML="";
        console.log('testando vendas');
        console.log(data.vendas)
        if (data.message){
            messageContainer.innerHTML=`<p>${data.message}</p>`;
        }

        if (data.vendas.length > 0){
            data.vendas.forEach(venda=>{
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${venda.id}</td>
                    <td>${venda.pessoa}</td>
                    <td>${venda.data_da_venda}</td>
                    <td>${venda.situacao}</td>
                    <td>${venda.is_active}</td>
                    <td>
                           <a href="/venda/update/${venda.id}">
                                <button class="btn" style="background-color: #117027;color: white;" >Editar</button>
                            </a>

                            <form action="/venda/delete/${venda.id}/" method="POST" style="display:inline-block;">
                                <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                                <button type="submit" class="btn" style="background-color: rgb(139, 16, 16);color: white;" onclick="return confirm('Tem certeza que deseja deletar este cliente?')">Deletar</button>
                            </form>
        
                    </td>
                `;
                resultContainer.appendChild(row);
            });
           
        }
        paginationContainer.innerHTML = "";

        if(data.pagination){
            console.log(data.pagination)
            const { has_previous, has_next, previous_page, next_page } = data.pagination;
            if (has_previous){
                const prevLink = document.createElement("a");

                prevLink.href=`/venda/?page=${previous_page}&query=${encodeURIComponent(query)}`;
                prevLink.textContent = "Anterior";
                prevLink.className="pagination-link";
                paginationContainer.appendChild(prevLink)
            }

            if(has_next){
                const nextLink = document.createElement("a");
                nextLink.href = `/venda/?page=${next_page}&query=${encodeURIComponent(query)}`;
                nextLink.textContent = "Próximo";
                nextLink.className = "pagination-link";
                paginationContainer.appendChild(nextLink);
            }
        }
    })
    .catch(error => console.error("Erro ao buscar vendas:",error));
})