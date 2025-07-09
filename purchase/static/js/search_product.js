const input = document.getElementById("searchInput");
const resultContainer = document.getElementById("results");
const messageContainer = document.getElementById("messageContainer");
const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

input.addEventListener("input",()=>{
    const query = input.value;
    fetch(`/product/buscar_produtos/?query=${encodeURIComponent(query)}`)
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
        if (data.message && query !=''){
            messageContainer.innerHTML=`<p>${data.message}</p>`;
        }

        if (data.produtos.length > 0){
            data.produtos.forEach(produto=>{
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${produto.id}</td>
                    <td>${produto.description}</td>
                    <td>${produto.product_code}</td>
                    <td>${produto.selling_price}</td>
                    <td>
                           <a href="/product/upt/${produto.id}">
                                <button class="btn" style="background-color: #117027;color: white;" >Editar</button>
                            </a>

                            <form action="/product/dlt/${produto.id}/" method="POST" style="display:inline-block;">
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
            const { has_previous, has_next, previous_page, next_page } = data.pagination;

            const createDiv = document.createElement('div');
            const boxPagination = document.createElement('div');

            createDiv.className = 'row text-center';
            boxPagination.className = 'col me-5';
            if (has_previous){
                const prevLink = document.createElement("a");

                prevLink.href=`/product/?page=${previous_page}&query=${encodeURIComponent(query)}`;
                prevLink.className="pagination-link me-5";

                const span = document.createElement('span');
                span.setAttribute('aria-hidden','true');
                span.style.fontSize = '32px';
                span.innerHTML = '&laquo;'

                prevLink.appendChild(span);
                prevLink.appendChild(span);
                boxPagination.appendChild(prevLink);
                createDiv.appendChild(boxPagination)
                paginationContainer.appendChild(createDiv);
            }
            else{
                const prevLink = document.createElement("a");
                prevLink.className="pagination-link me-5";

                const span = document.createElement('span');
                span.setAttribute('aria-hidden','true');
                span.setAttribute('aria-disabled','true');
                span.style.fontSize = '32px';
                span.style.color = 'gray';
                span.style.pointerEvents = 'none';
                span.innerHTML = '&laquo;'

                prevLink.appendChild(span);
                boxPagination.appendChild(prevLink);
                createDiv.appendChild(boxPagination)
                paginationContainer.appendChild(createDiv);
            }

            if(has_next){
                const nextLink = document.createElement("a");
                nextLink.href = `/product/?page=${next_page}&query=${encodeURIComponent(query)}`;
                nextLink.className = "pagination-link me-5";

                const span = document.createElement('span');
                span.setAttribute('aria-hidden','true');
                span.style.fontSize = '32px';
                span.innerHTML = `&raquo;`

                nextLink.appendChild(span);
                boxPagination.appendChild(nextLink);
                createDiv.appendChild(boxPagination)
                paginationContainer.appendChild(createDiv);
            }
             else{
                const nextLink = document.createElement("a");
                nextLink.className = "pagination-link me-5";

                const span = document.createElement('span');
                span.setAttribute('aria-hidden','true');
                span.setAttribute('aria-disabled','true');
                span.style.fontSize = '32px';
                span.style.color = 'gray';
                span.style.pointerEvents = 'none';
                span.innerHTML = `&raquo;`

                nextLink.appendChild(span);
                boxPagination.appendChild(nextLink);
                createDiv.appendChild(boxPagination)
                paginationContainer.appendChild(createDiv);
            }
        }
    })
    .catch(error => console.error("Erro ao buscar vendas:",error));
})