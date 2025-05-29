let botaoClicado = false;
let botaoClicadoRomaneio = false;
let botaoClicadoImposto = false;
let botaoClicadoFrete = false;

let select_freight = document.getElementById("id_freight_type");
const generateRomaneio = document.getElementById('romaneioGenerate');
const generateTax = document.getElementById('taxGenerate');

document.getElementById('generate').addEventListener('click', () => {
    botaoClicado = true;
});

if (generateRomaneio){
    generateRomaneio.addEventListener('click',()=>{
    botaoClicadoRomaneio = true;
    });
}

if (generateTax){
    generateTax.addEventListener('click',()=>{
    botaoClicadoImposto = true;
    });
}

if (select_freight){
    select_freight.addEventListener("change",()=>{
    if (select_freight.value == 'FOB'){
        const generateFrete = document.getElementById("freightGenerate");
        generateFrete.addEventListener("click",()=>{
            botaoClicadoFrete = true;
        })
    }
    else{
        botaoClicadoFrete = false;
    }
    })
}




document.getElementById('form').addEventListener('submit', function (event) {
    if (select_freight){
        if (select_freight.value == 'FOB'){
            console.log("entrei aqui?")
            if(!botaoClicado){
                event.preventDefault()
                alert('Você precisa gerar os pagamentos dos produtos!');
            }
            if(!botaoClicadoImposto){
                event.preventDefault()
                alert('Você precisa gerar os pagamentos sobre o imposto!');
            }
            if(!botaoClicadoFrete){
                event.preventDefault()
                alert('Você precisa gerar os pagamentos sobre o frete!');
            }
            if(!botaoClicadoRomaneio){
                event.preventDefault()
                alert('Você precisa gerar os pagamentos sobre o romaneio!');
            }
        }
        else{

            if(!botaoClicado){
                    event.preventDefault()
                    alert('Você precisa gerar os pagamentos dos produtos!');
            }
            if(!botaoClicadoImposto){
                    event.preventDefault()
                    alert('Você precisa gerar os pagamentos sobre o imposto!');
            }
            if(!botaoClicadoFrete){
                    event.preventDefault()
                    alert('Você precisa gerar os pagamentos sobre o frete!');
            }
        }
    }
    else{
        if(!botaoClicado){
            event.preventDefault()
            alert('Você precisa gerar os pagamentos dos produtos!');
        }
    }
  
});