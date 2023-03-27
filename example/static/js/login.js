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
    var csrf_token = $('#csrf_text').text();
    var remail = document.getElementById('r_email').value;
    document.getElementById('r_csrf').value = csrf_token;
    $('#loding').show();
    setTimeout(function() {
        var hash_password = document.getElementById('r_password').value;
        for (var i = 0; i < 10; i++) {
            hash_password = GetHashPwd(remail, hash_password);
        }
        document.getElementById('r_password').value = hash_password;
        $('.register-box').submit();
    }, 50);
    return true;
}
// 登录前端慢哈希
function SetLogin() {
    var csrf_token = $('#csrf_text').text();
    var lemail = document.getElementById('l_email').value;
    document.getElementById('l_csrf').value = csrf_token;
    $('#loding').show();
    setTimeout(function() {
        var hash_password = document.getElementById('l_password').value;
        for (var i = 0; i < 10; i++) {
            hash_password = GetHashPwd(lemail, hash_password);
        }
        document.getElementById('l_password').value = hash_password;
        $('.login-box').submit();
    }, 50);
    return true;
}


// 密码重复检测
$('#r_password_again').focusout(function() { //输入框内容改变时发生的事件通用版
    var a = $('#r_password').val();
    var b = $('#r_password_again').val();
    if (a != b) {
        alert('输入的密码不相同！请重新输入');
        document.getElementById('r_password_again').value = '';
        $('#r_submit').hide();
    }
    if (a != '' && b != '') {
        $('#r_submit').show();
    }
});

$(document).ready(function() {
    mes = $('#flash_mes').text();
    if (mes.length > 1) {
        alert(mes)
    }
});

// 密码检测
$('#r_password').focusout(function() {
    $('#password_strong').removeAttr('hidden');
    var a = $('#r_password').val();
    var re = zxcvbn(a);
    var RegExp1 = /[A-Z]/g
    var RegExp2 = /[a-z]/g
    var RegExp3 = /[0-9]/g
    var length_pass = false;
    var safity_pass = false;
    var strong_pass = false;
    if (a.length >= 6 && a.length <= 36) {
        length_pass = true;
    } else {
        alert('密码长度应在 6 到 36 位之间');
    }
    if (RegExp1.test(a) && RegExp2.test(a) && RegExp3.test(a)) {
        safity_pass = true;
    } else {
        alert('密码应包含大小写及数字');
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
    if (length_pass && strong_pass && safity_pass) {
        $('#password_strong').show();
        $('#r_password_again').show();
    } else {
        $('#r_password_again').hide();
        $('#r_submit').hide();
    }
});

// 用户名检测
$('#r_username').focusout(function() {
    var username = $('#r_username').val();
    var RegExp = /[`~!@#$^&*()=|{}':;',\[\].<>《》\\\/?~！@#￥……&*（）――|{}【】‘；：”“'。，、？ ]+/g;
    if (RegExp.test(username)) {
        alert('用户名含有特殊字符！');
        $('#r_email').hide();
        $('#r_password').hide();
        $('#password_strong').hide();
        $('#r_password_again').hide();
        $('#r_submit').hide();

    } else {
        $('#r_email').show();
    }
});

// 邮箱检测
$('#r_email').focusout(function() {
    var email = $('#r_email').val();
    var RegExp = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if (RegExp.test(email)) {
        $('#r_password').show();
    } else {
        alert('邮箱格式不正确！');
        $('#r_password').hide();
        $('#password_strong').hide();
        $('#r_password_again').hide();
        $('#r_submit').hide();
    }
});