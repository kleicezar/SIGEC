// Seleciona o botão de toggle e a sidebar
const toggleButton = document.querySelector('.toggle-menu');
const sidebar = document.querySelector('.sidebar');
const content = document.querySelector('.content'); // Adicionado para referenciar o conteúdo
const toggles = document.querySelectorAll('.toggle');
// Alterna a visibilidade da sidebar
toggleButton.addEventListener('click', () => {
    sidebar.classList.toggle('hidden');
    content.classList.toggle('expanded'); // Alterna a classe no conteúdo
});


// Seleciona o botão e o menu
const userMenuButton = document.getElementById('user-menu-button');
const userDropdownMenu = document.getElementById('user-dropdown-menu');

// Adiciona um evento de clique para mostrar/ocultar o menu
userMenuButton.addEventListener('click', function(event) {
    // Impede que o clique no botão feche o menu imediatamente
    event.stopPropagation();
    
    // Alterna a visibilidade do menu
    const isMenuVisible = userDropdownMenu.style.display === 'block';
    userDropdownMenu.style.display = isMenuVisible ? 'none' : 'block';
});

// Fecha o menu se o usuário clicar fora dele
window.addEventListener('click', function(event) {
    if (!userDropdownMenu.contains(event.target) && event.target !== userMenuButton) {
        userDropdownMenu.style.display = 'none';
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const toggles = document.querySelectorAll(".toggle");

    toggles.forEach((toggle, index) => {
        const submenu = toggle.nextElementSibling; // Pegamos o submenu associado

        //Recupera o estado salvo no localStorage
        const estadoSalvo = localStorage.getItem(`submenu-${index}`);

  
        if (estadoSalvo === "block") {
            submenu.style.display = "block";
            toggle.classList.replace( "toggle","rotate")
        } else {
            submenu.style.display = "none";
            
            toggle.classList.replace("rotate", "toggle");
        }

        toggle.addEventListener("click", function () {
            const displayAtual = window.getComputedStyle(submenu).display;

            if (displayAtual === "none") {
                submenu.style.display = "block";
                localStorage.setItem(`submenu-${index}`, "block"); // Salva o estado
                toggle.classList.replace( "toggle","rotate")
            } else {
                submenu.style.display = "none";
                localStorage.setItem(`submenu-${index}`, "none"); // Salva o estado
                toggle.classList.replace("rotate", "toggle");
            }
        });
    });
});
