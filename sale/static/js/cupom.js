function imprimirCupom(vendaId) {
    const url = `/cupom/${vendaId}/`;  // URL que chama a view do Django
    const janela = window.open(url, 'Impressão', 'width=300,height=600');

    janela.onload = function () {
        janela.print();
        janela.onafterprint = () => janela.close();
    };
}