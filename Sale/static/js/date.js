$(document).ready(function() {
    $('#date_sale').datepicker({
        format: 'yyyy-mm-dd', // Formato de data
        autoclose: true,     // Fecha o calendário automaticamente após a seleção
        todayHighlight: true // Destaca o dia atual
    });
});

$(document).ready(function() {
    $('#payment_method').datepicker({
        format: 'yyyy-mm-dd', // Formato de data
        autoclose: true,     // Fecha o calendário automaticamente após a seleção
        todayHighlight: true, // Destaca o dia atual
        startDate: '+0d',
    });
});