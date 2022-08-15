function PWForm() {
    $('#loding').show();
    setTimeout(function() {
        var email = $('#user_email').text();
        var hash_password = document.getElementById('password').value;
        for (var i = 0; i < 10; i++) {
            hash_password = GetHashPwd(email, hash_password);
        }
        document.getElementById('password').value = hash_password;
        $('.password-box').submit();
    }, 50);
    return true;
}

$(document).ready(function() {
    mes = $('#flash_mes').text();
    if (mes.length > 1) {
        alert(mes)
    }
});