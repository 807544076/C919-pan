$(document).ready(function() {
    mes = $('#flash_mes').text();
    if (mes.length > 1) {
        alert(mes);
    }
});

function Loading() {
    $('#loding').show();
}

$('#email').focusout(function() {
    var email = $('#email').val();
    var RegExp = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if (RegExp.test(email)) {
        $('#sbtn').show();
    } else {
        alert('邮箱格式不正确！');
        $('#sbtn').hide();
    }
});