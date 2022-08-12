// 要操作的元素
$signin = $("#signin");
$login = $("#login");
$register = $("#register");
$threelogin = $("#threelogin");
$form_box = $(".form-box");
$register_box = $(".register-box");
$login_box = $(".login-box");
$threelogin_box = $(".threelogin-box");

//‘第三方登录’按钮点击事件
$threelogin.click(function() {
        $form_box.css({ "background-color": "#96a0d8", "transform": "translateX(0%)" })
        $login_box.addClass('hidden');
        $threelogin_box.removeClass('hidden');
    })
    //‘已有账号登录’按钮点击事件
$signin.click(function() {
        $form_box.css({ "background-color": "#bcb7d8", "transform": "translateX(0%)" })
        $register_box.addClass('hidden');
        $threelogin_box.addClass('hidden');
        $login_box.removeClass('hidden');
    })
    //‘去注册’按钮点击事件
$register.click(function() {
        $form_box.css({ "background-color": "#bcb7d8", "transform": "translateX(85%)" })
        $login_box.addClass('hidden');
        $threelogin_box.addClass('hidden');
        $register_box.removeClass('hidden');
    })
    //‘去登录’按钮点击事件
$login.click(function() {
        $form_box.css({ "background-color": "#bcb7d8", "transform": "translateX(0%)" })
        $register_box.addClass('hidden');
        $threelogin_box.addClass('hidden');
        $login_box.removeClass('hidden');
    })
    // 注册前端慢哈希
function SetRegister() {
    if ($('#password_strong').text() == "弱") {
        alert("密码强度太弱！")
        return false;
    }
    hash_email = document.getElementById('r_email').value;
    hash_password = document.getElementById('r_password').value;
    for (var i = 0; i < 10; i++) {
        hash_email = GetHashPwd('c919_cuc', hash_email);
        hash_password = GetHashPwd(document.getElementById('r_email').value, hash_password);
    }
    document.getElementById('r_email').value = hash_email
    document.getElementById('r_password').value = hash_password
    return true;
}
// 登录前端慢哈希
function SetLogin() {
    hash_email = document.getElementById('l_email').value;
    hash_password = document.getElementById('l_password').value;
    for (var i = 0; i < 10; i++) {
        hash_email = GetHashPwd('c919_cuc', hash_email);
        hash_password = GetHashPwd(document.getElementById('l_email').value, hash_password);
    }
    document.getElementById('l_email').value = hash_email
    document.getElementById('l_password').value = hash_password
    return true;
}

$('#r_password_again').on('change', function() { //输入框内容改变时发生的事件通用版
    var a = $('#r_password').val();
    var b = $('#r_password_again').val();
    if (a != b) {
        alert('输入的密码不相同！请重新输入');
        document.getElementById('r_password_again').value = '';
    }
});

$(document).ready(function() {
    mes = $('#flash_mes').text();
    if (mes.length > 1) {
        alert(mes)
    }
});

$('#r_password').on('change', function() {
    $('#password_strong').removeAttr('hidden');
    var a = $('#r_password').val();
    var re = zxcvbn(a)
    if (re['score'] < 2) {
        $('#password_strong').text(function() {
            return '弱';
        });
        $('#password_strong').css("background-color", "red");
    }
    if (re['score'] >= 2 && re['score'] < 4) {
        $('#password_strong').text(function() {
            return '中';
        });
        $('#password_strong').css("background-color", "yellow");
        $('#r_submit').removeAttr('hidden');
    }
    if (re['score'] == 4) {
        $('#password_strong').text(function() {
            return '强';
        });
        $('#password_strong').css("background-color", "greenyellow");
        $('#r_submit').removeAttr('hidden');
    }
});