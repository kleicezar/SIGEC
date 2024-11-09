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
const isToggle = true;
// Adiciona eventos de clique para os links do menu
toggles.forEach(toggle => {
    toggle.addEventListener('click', function(event) {
        event.preventDefault(); // Impede o comportamento padrão do link

        const subMenu = this.nextElementSibling; // Seleciona a próxima sub-menu

        // Alterna a exibição da sub-menu
        if (subMenu.style.display === 'block') {
            subMenu.style.display = 'none';
            // toggle.classList.toggle('toggle');
        } else {
            subMenu.style.display = 'block';
            // toggle.classList.toggle('rotate');
        }
        /*nao colocar antes do if e do else de cima*/
        if(isToggle){
            toggle.classList.toggle("rotate");
            isToggle = !isToggle;
        }
        else{
            toggle.classList.toggle("toggle");
            isToggle = !isToggle;
        }
    });
});