// 要操作的元素
$fileupload = $("#fileupload");
$floder = $("#floder");
$file_upload = $(".file-upload");
$library = $(".library");


//‘上传文件’按钮点击事件
$fileupload.click(function() {
    $library.addClass('hidden');
    $file_upload.removeClass('hidden');
})

//‘文件库’按钮点击事件
$floder.click(function() {
    $file_upload.addClass('hidden');
    $library.removeClass('hidden');
})

const showMenu = (toggleId, navbarId, bodyId) => {
    const toggle = document.getElementById(toggleId),
        navbar = document.getElementById(navbarId),
        bodypadding = document.getElementById(bodyId);

    if (toggle && navbar) {
        toggle.addEventListener('click', () => {
            navbar.classList.toggle('expander');
            $('#welcome').toggle();
            bodypadding.classList.toggle('body-pd');
        })
    }
}

showMenu('nav-toggle', 'navbar', 'body-pd')


const linkColor = document.querySelectorAll(".nav_link")

function colorLink() {
    linkColor.forEach(l => l.classList.remove('active'))
    this.classList.add('active')
}
linkColor.forEach(l => l.addEventListener('click', colorLink))

const linkCollapse = document.getElementsByClassName('collapse__link')
var i

for (i = 0; i < linkCollapse.length; i++) {
    linkCollapse[i].addEventListener('click', function() {
        const collapseMenu = this.nextElementSibling
        collapseMenu.classList.toggle('showCollapse')

        const rotate = collapseMenu.previousElementSibling
        rotate.classList.toggle("")
    })
}

function fileUpload() {
    $('#fileupload').click();
}