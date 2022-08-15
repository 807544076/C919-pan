$(document).ready(function() {
    mes = $('#flash_mes').text();
    if (mes.length > 1) {
        alert(mes);
    }
});

function Loading() {
    $('#loding').show();
}