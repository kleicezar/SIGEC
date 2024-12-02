// const searchInput = document.getElementById('searchBox'); // O campo de pesquisa
// const resultsDiv = document.getElementById('results'); // Div onde os resultados serão exibidos

// searchInput.addEventListener('input', function() {
//     const query = searchInput.value;

//     if (query.length > 0) {
//         fetch(`/search/?p=${query}`)
//             .then(response => response.json())
//             .then(data => {
//                 // Limpa os resultados anteriores
//                 resultsDiv.innerHTML = '';

//                 // Adiciona os novos resultados
//                 data.forEach(client => {
//                     const clientDiv = document.createElement('div');
//                     clientDiv.textContent = client.id_FisicPerson_fk__name || client.id_LegalPerson_fk__name || client.id_ForeignPerson_fk__name;
//                     resultsDiv.appendChild(clientDiv);
//                 });
//             });
//     } else {
//         resultsDiv.innerHTML = ''; // Limpa os resultados se não houver consulta
//     }
// });

// document.addEventListener('DOMContentLoaded', function () {
//     const searchBox = document.getElementById('search');
//     const tableBody = document.querySelector('tbody');

//     searchBox.addEventListener('input', function () {
//         const query = searchBox.value;

//         // Fazendo uma requisição AJAX para a busca dinâmica
//         fetch(`/client-search/?q=${query}`, {
//             method: 'GET',
//             headers: {
//                 'X-Requested-With': 'XMLHttpRequest'
//             }
//         })
//             .then(response => response.json())
//             .then(data => {
//                 // Limpa a tabela antes de atualizar
//                 tableBody.innerHTML = '';

//                 // Preenchendo a tabela com os resultados
//                 data.results.forEach(client => {
//                     const row = document.createElement('tr');
//                     row.innerHTML = `
//                         <td>${client.id}</td>
//                         <td>${client.name}</td>
//                         <td>${client.personal_phone || 'N/A'}</td>
//                         <td>${client.work_phone || 'N/A'}</td>
//                         <td><a href="/client-detail/${client.id}/">Detalhes</a></td>
//                     `;
//                     tableBody.appendChild(row);
//                 });
//             })
//             .catch(error => console.error('Erro ao buscar clientes:', error));
//     });
// });


// document.addEventListener('DOMContentLoaded', function () {
//     const searchBox = document.getElementById('search');
//     const tableBody = document.querySelector('tbody');

//     // Adiciona o evento de input ao campo de pesquisa
//     searchBox.addEventListener('input', function () {
//         const query = searchBox.value;

//         // Fazendo uma requisição AJAX para a busca
//         fetch(`/client-search/?q=${query}`, {
//             method: 'GET',
//             headers: {
//                 'X-Requested-With': 'XMLHttpRequest' // Marca a requisição como AJAX
//             }
//         })
//             .then(response => response.json())
//             .then(data => {
//                 // Limpa a tabela antes de atualizar
//                 tableBody.innerHTML = '';

//                 // Verifica se há resultados
//                 if (data.results.length > 0) {
//                     // Preenche a tabela com os resultados
//                     data.results.forEach(client => {
//                         const row = document.createElement('tr');
//                         row.innerHTML = `
//                             <td>${client.id}</td>
//                             <td>${client.name}</td>
//                             <td>${client.personal_phone || 'N/A'}</td>
//                             <td>${client.work_phone || 'N/A'}</td>
//                             <td><a href="/client-detail/${client.id}/">Detalhes</a></td>
//                         `;
//                         tableBody.appendChild(row);
//                     });
//                 } else {
//                     // Adiciona uma linha informando que não há resultados
//                     const noResultsRow = document.createElement('tr');
//                     noResultsRow.innerHTML = `
//                         <td colspan="5" style="text-align: center;">Nenhum resultado encontrado</td>
//                     `;
//                     tableBody.appendChild(noResultsRow);
//                 }
//             })
//             .catch(error => console.error('Erro ao buscar clientes:', error));
//     });
// });


// $(document).ready(function() {  // Garante que o código execute após o carregamento completo da página.
//     $('#search').on('keyup', function() {  // Event listener para o evento "keyup", ou seja, quando o usuário digitar algo
//         var query = $(this).val();  // Obtém o valor digitado no campo de input com o id "search"
        
//         if (query.length > 0) {  // Se o valor digitado for maior que 0 (não estiver vazio)
//             $.ajax({  // Realiza uma requisição AJAX para o servidor
//                 url: "{% url 'buscar_dinamico' %}",  // URL que a requisição AJAX vai chamar. No caso, é uma URL do Django que irá processar a busca
//                 data: {  // Envia a consulta (query) como parâmetro na requisição
//                     'q': query
//                 },
//                 success: function(data) {  // Quando a requisição for bem-sucedida, esta função é chamada
//                     $('#results').html(data);  // Atualiza a <div id="results"> com os dados retornados da consulta
//                 }
//             });
//         } else {
//             $('#results').html("");  // Se não houver texto no campo de busca, limpa os resultados
//         }
//     });
// });


// let timeout;
// let timeout;
// function buscarProdutos() {
//     clearTimeout(timeout);
//     timeout = setTimeout(function() {
//         var query = document.getElementById('campoBusca').value;
//         if (query.length > 0) {
//             // Fazendo requisição AJAX para a view Django
//             fetch('/buscar_produtos/?query=' + query)
//                 .then(response => response.json())
//                 .then(data => {
//                     var tabela = document.getElementById('tabelaResultados');
//                     var corpoTabela = tabela.getElementsByTagName('tbody')[0];
//                     corpoTabela.innerHTML = ''; // Limpa os resultados anteriores
                    
//                     if (data.resultados.length > 0) {
//                         data.resultados.forEach(produto => {
//                             var linha = document.createElement('tr');
                            
//                             var celulaNome = document.createElement('td');
//                             celulaNome.innerHTML = produto.nome;
//                             linha.appendChild(celulaNome);
                            
//                             var celulaDescricao = document.createElement('td');
//                             celulaDescricao.innerHTML = produto.descricao;
//                             linha.appendChild(celulaDescricao);
                            
//                             corpoTabela.appendChild(linha);
//                         });
//                     } else {
//                         var linhaVazia = document.createElement('tr');
//                         var celulaVazia = document.createElement('td');
//                         celulaVazia.colSpan = 2;
//                         celulaVazia.innerHTML = 'Nenhum produto encontrado';
//                         linhaVazia.appendChild(celulaVazia);
//                         corpoTabela.appendChild(linhaVazia);
//                     }
//                 });
//         } else {
//             // Limpar tabela se o campo de busca estiver vazio
//             document.getElementById('tabelaResultados').getElementsByTagName('tbody')[0].innerHTML = '';
//         }
//     }, 300); // Espera 300ms após o usuário parar de digitar
// }

let timeout;
function buscarPessoas() {
    clearTimeout(timeout);
    timeout = setTimeout(function() {
        var query = document.getElementById('campoBusca').value;
        if (query.length > 0) {
            // Fazendo requisição AJAX para a view Django
            fetch('/buscar_pessoas/?query=' + query)
                .then(response => response.json())
                .then(data => {
                    var tabela = document.getElementById('tabelaResultados');
                    var corpoTabela = tabela.getElementsByTagName('tbody')[0];
                    corpoTabela.innerHTML = ''; // Limpa os resultados anteriores
                    
                    if (data.resultados.length > 0) {
                        data.resultados.forEach(pessoa => {
                            var linha = document.createElement('tr');
                            
                            var celulaNome = document.createElement('td');
                            celulaNome.innerHTML = pessoa.nome || '';
                            linha.appendChild(celulaNome);
                            
                            var celulaFantasyName = document.createElement('td');
                            celulaFantasyName.innerHTML = pessoa.fantasy_name || '';
                            linha.appendChild(celulaFantasyName);
                            
                            var celulaNameForeigner = document.createElement('td');
                            celulaNameForeigner.innerHTML = pessoa.name_foreigner || '';
                            linha.appendChild(celulaNameForeigner);
                            
                            corpoTabela.appendChild(linha);
                        });
                    } else {
                        var linhaVazia = document.createElement('tr');
                        var celulaVazia = document.createElement('td');
                        celulaVazia.colSpan = 3; // Coloca em 3 colunas (já que temos 3 campos)
                        celulaVazia.innerHTML = 'Nenhuma pessoa encontrada';
                        linhaVazia.appendChild(celulaVazia);
                        corpoTabela.appendChild(linhaVazia);
                    }
                });
        } else {
            // Limpar tabela se o campo de busca estiver vazio
            document.getElementById('tabelaResultados').getElementsByTagName('tbody')[0].innerHTML = '';
        }
    }, 300); // Espera 300ms após o usuário parar de digitar
}