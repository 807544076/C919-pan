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
    $form_box.css({"background-color":"#96a0d8","transform": "translateX(0%)"})
    $login_box.addClass('hidden');
    $threelogin_box.removeClass('hidden');
})
//‘已有账号登录’按钮点击事件
$signin.click(function() {
    $form_box.css({"background-color":"#bcb7d8","transform": "translateX(0%)"})
    $register_box.addClass('hidden');
    $threelogin_box.addClass('hidden');
    $login_box.removeClass('hidden');
})
//‘去注册’按钮点击事件
$register.click(function() {
        $form_box.css({"background-color":"#bcb7d8","transform": "translateX(85%)"})
        $login_box.addClass('hidden');
        $threelogin_box.addClass('hidden');
        $register_box.removeClass('hidden');
    })
//‘去登录’按钮点击事件
$login.click(function() {
    $form_box.css({"background-color":"#bcb7d8","transform": "translateX(0%)"})
    $register_box.addClass('hidden');
    $threelogin_box.addClass('hidden');
    $login_box.removeClass('hidden');
})



