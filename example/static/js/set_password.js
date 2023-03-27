function PWForm() {
    var uemail = document.getElementById('user_email').innerHTML;
    $('#loding').show();
    setTimeout(function() {
        var hash_password = document.getElementById('password').value;
        for (var i = 0; i < 10; i++) {
            hash_password = GetHashPwd(uemail, hash_password);
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

$('#password').focusout(function() {
    var a = $('#password').val();
    var re = zxcvbn(a);
    var RegExp1 = /[A-Z]/g
    var RegExp2 = /[a-z]/g
    var RegExp3 = /[0-9]/g
    var length_pass = false;
    var safity_pass = false;
    var strong_pass = false;
    if (a.length >= 6 && a.length <= 36) {
        length_pass = true;
        if (RegExp1.test(a) && RegExp2.test(a) && RegExp3.test(a)) {
            safity_pass = true;
            if (re['score'] < 2) {
                alert('密码太弱，请重试');
            } else {
                strong_pass = true;
            }
        } else {
            alert('密码应包含大小写及数字');
        }
    } else {
        alert('密码长度应在 6 到 36 位之间');
    }


    if (length_pass && strong_pass && safity_pass) {
        $('#bcommit').show();
    } else {
        $('#bcommit').hide();
    }
});