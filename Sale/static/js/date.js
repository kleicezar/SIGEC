$(document).ready(function() {
    $('#date_sale').datepicker({
        format: 'dd/mm/yyyy', // Formato de data
        autoclose: true,     // Fecha o calendário automaticamente após a seleção
        todayHighlight: true, // Destaca o dia atual
        language: 'pt-BR'
    });
});

$(document).ready(function() {
    $('#date_purchase').datepicker({
        format: 'dd/mm/yyyy', // Formato de data
        autoclose: true,     // Fecha o calendário automaticamente após a seleção
        todayHighlight: true, // Destaca o dia atual
        language: 'pt-BR',
    });
});

$(document).ready(function() {
    $('#payment_method').datepicker({
        format: 'dd/mm/yyyy', // Formato de data
        autoclose: true,     // Fecha o calendário automaticamente após a seleção
        todayHighlight: true, // Destaca o dia atual
        startDate: '+0d',
        language: 'pt-BR'
    });
});
$(document).ready(function() {
    $('#date_init').datepicker({
        format: 'dd/mm/yyyy', // Formato de data
        autoclose: true,     // Fecha o calendário automaticamente após a seleção
        todayHighlight: true, // Destaca o dia atual
        startDate: '+0d',
        language: 'pt-BR'
    });
});
$(document).ready(function() {
    $('#empty-payment-method-form').datepicker({
        format: 'dd/mm/yyyy', // Formato de data
        autoclose: true,     // Fecha o calendário automaticamente após a seleção
        todayHighlight: true, // Destaca o dia atual
        startDate: '+0d',
        language: 'pt-BR'
    });
});