// 要操作的元素
$login = $("#login");
$register = $("#register");
$form_box = $(".form-box");
$register_box = $(".register-box");
$login_box = $(".login-box");

//‘去注册’按钮点击事件
$register.click(function() {
        $form_box.css("transform", "translateX(100%)")
        $login_box.addClass('hidden');
        $register_box.removeClass('hidden');
    })
//‘去登录’按钮点击事件
$login.click(function() {
    $form_box.css("transform", "translateX(0%)")
    $register_box.addClass('hidden');
    $login_box.removeClass('hidden');
})

//无法实现js滑动效果