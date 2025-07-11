function imprimirCupom(vendaId) {
    const url = `cupom/${vendaId}/`;

    const novaAba = window.open(url, '_blank');

    if (novaAba) {
        novaAba.focus();

        novaAba.onload = function () {
            novaAba.print();
            // novaAba.onafterprint = () => novaAba.close();
        };
    } else {
        alert("Por favor, permita pop-ups no navegador para imprimir o cupom.");
    }
}