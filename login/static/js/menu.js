// Seleciona o botão de toggle e a sidebar
const toggleButton = document.querySelector('.toggle-menu');
const sidebar = document.querySelector('.sidebar');
const content = document.querySelector('.content'); // Adicionado para referenciar o conteúdo
const toggles = document.querySelectorAll('.toggle');
// console.log('dfsfadsf');
// Alterna a visibilidade da sidebar
toggleButton.addEventListener('click', () => {
    sidebar.classList.toggle('hidden');
    content.classList.toggle('expanded'); // Alterna a classe no conteúdo
});

// Adiciona eventos de clique para os links do menu
toggles.forEach(toggle => {
    toggle.addEventListener('click', function(event) {
        event.preventDefault(); // Impede o comportamento padrão do link

        const subMenu = this.nextElementSibling; // Seleciona a próxima sub-menu
        // let isToggle = true;
        // Alterna a exibição da sub-menu
        if (subMenu.style.display === 'block') {
            
            // toggle.classList.toggle('toggle');
            subMenu.style.display = 'none';

            toggle.classList.replace("rotate", "toggle");
           
            // console.log(meuElemento.className); // "classe3 classe2"

        } else {
            toggle.classList.replace( "toggle","rotate");
            subMenu.style.display = 'block';
          
        }
        /*nao colocar antes do if e do else de cima*/
        // if(isToggle){
        //     toggle.classList.toggle("rotate");
        //     isToggle = !isToggle;
        // }
        // else{
        //     toggle.classList.toggle("toggle");
        //     isToggle = !isToggle;
        // }
    });
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