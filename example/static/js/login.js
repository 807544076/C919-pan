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
    hash_password = document.getElementById('r_password').value;
    for (var i = 0; i < 10; i++) {
        hash_password = GetHashPwd(document.getElementById('r_email').value, hash_password);
    }
    document.getElementById('r_password').value = hash_password
    $('.register-box').submit();
    return true;
}
// 登录前端慢哈希
function SetLogin() {
    hash_password = document.getElementById('l_password').value;
    for (var i = 0; i < 10; i++) {
        hash_password = GetHashPwd(document.getElementById('l_email').value, hash_password);
    }
    document.getElementById('l_password').value = hash_password
    $('.login-box').submit();
    return true;
}


// 密码重复检测
$('#r_password_again').on('change', function() { //输入框内容改变时发生的事件通用版
    var a = $('#r_password').val();
    var b = $('#r_password_again').val();
    if (a != b) {
        alert('输入的密码不相同！请重新输入');
        document.getElementById('r_password_again').value = '';
    }
    if (a != '' && b != '') {
        $('#r_submit').removeAttr('hidden');
    }
});

$(document).ready(function() {
    mes = $('#flash_mes').text();
    if (mes.length > 1) {
        alert(mes)
    }
});

// 密码检测
$('#r_password').on('change', function() {
    $('#password_strong').removeAttr('hidden');
    var a = $('#r_password').val();
    var re = zxcvbn(a)
    var length_pass = false;
    var strong_pass = false;
    if (a.length > 6 && a.length < 36) {
        length_pass = true;
    } else {
        alert('密码长度应在 6 到 36 位之间');
    }
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
        strong_pass = true;
    }
    if (re['score'] == 4) {
        $('#password_strong').text(function() {
            return '强';
        });
        $('#password_strong').css("background-color", "greenyellow");
        strong_pass = true;
    }
    if (length_pass && strong_pass) {
        $('#r_password_again').removeAttr('hidden');
    }
});

// 用户名检测
$('#r_username').on('change', function() {
    var username = $('#r_username').val();
    var RegExp = /[`~!@#$^&*()=|{}':;',\[\].<>《》\\\/?~！@#￥……&*（）――|{}【】‘；：”“'。，、？ ]+/g;
    if (RegExp.test(username)) {
        alert('用户名含有特殊字符！');
        $('#r_email').attr('hidden');
    } else {
        $('#r_email').removeAttr('hidden');
    }
});

// 邮箱检测
$('#r_email').on('change', function() {
    var email = $('#r_email').val();
    var RegExp = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if (RegExp.test(email)) {
        $('#r_password').removeAttr('hidden');
    } else {
        alert('邮箱格式不正确！');
        $('#r_password').attr('hidden');
    }
});