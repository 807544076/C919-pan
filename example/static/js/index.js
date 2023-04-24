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
            // bodypadding.classList.toggle('body-pd');
        })
    }
}

showMenu('nav-toggle', 'navbar', 'body-pd')
document.getElementById('nav-toggle').click();

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

function GenPBKDF2(pass, size) {
    var salt = CryptoJS.lib.WordArray.random(128 / 8);
    var key = CryptoJS.PBKDF2(pass, salt, {
        keySize: size / 32,
        iterations: 4096,
        hasher: CryptoJS.algo.SHA256
    });
    return key;
}

function aes_encrypt(msg, key, iv) {
    var ciphertext = CryptoJS.AES.encrypt(msg, key, {
        iv: iv,
        mode: CryptoJS.mode.OFB,
        padding: CryptoJS.pad.Pkcs7
    });
    return ciphertext.toString();
}

function bufferToHex(buffer) {
    var hex = "";
    var view = new Uint8Array(buffer); // 创建一个字节视图
    for (var i = 0; i < view.length; i++) {
        var byte = view[i].toString(16); // 把每个字节转为16进制字符串
        if (byte.length < 2) {
            byte = "0" + byte; // 如果长度小于2，补0
        }
        hex += byte; // 拼接字符串
    }
    return hex;
}

function hexStringToByteArray(hexString) {
    if (hexString.length % 2 !== 0) {
        throw "Must have an even number of hex digits to convert to bytes";
    }
    var numBytes = hexString.length / 2;
    var byteArray = new Uint8Array(numBytes);
    for (var i = 0; i < numBytes; i++) {
        byteArray[i] = parseInt(hexString.substr(i * 2, 2), 16);
    }
    return byteArray;
}

function fromHex(h) {
    var s = ''
    for (var i = 0; i < h.length; i += 2) {
        s += String.fromCharCode(parseInt(h.substr(i, 2), 16))
    }
    return s
}

var secret_key = GenPBKDF2('hello aes', 256);
var iv = CryptoJS.lib.WordArray.random(128 / 8);
var dt_f = new DataTransfer();
var dt_k = new DataTransfer();
var dt_i = new DataTransfer();
var temp;
var fileList;
var previewType = ['image/jpg', 'image/jpeg', 'image/png', 'image/gif', 'image/bmp']
var encrypt = new JSEncrypt();
encrypt.setPublicKey(document.getElementById('pubk').innerHTML);
var sign = $('#sign').text(); //sign is sign encode with base64(string)
var rb = $('#rb').text(); //rb is plain text
var d_sign = encrypt.verify(rb, sign, CryptoJS.SHA256);
if (!d_sign) {
    alert('您当前所处网络环境不安全！您的功能将被暂时冻结，请切换至安全的网络环境后重新登录。');
    var buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.disabled = true;
    })
    var ha = document.querySelectorAll('a');
    ha.forEach(a => {
        a.setAttribute('style', 'pointer-events:none;');
    })
}

var area = document.querySelector('.drop-area');
area.addEventListener("dragenter", function(e) { //拖进
    e.preventDefault();
})
area.addEventListener("dragover", function(e) { //拖来拖去 
    e.preventDefault();
})
area.addEventListener('drop', function(event) {
    event.preventDefault();
    // 将类数组对象 转换成数组
    // var fileList = Array.from(event.dataTransfer.files);  //  es6 格式
    fileList = event.dataTransfer.files; // es5 格式
    document.getElementById('selectfilename').innerHTML = fileList[0].name;
    document.getElementById('file_input').files = fileList;
    if (window.FileReader) {
        var preview = document.querySelector('img');
        var fr = new FileReader();
        fr.onloadend = function(e) {
            if (previewType.includes(fileList[0].type)) {
                preview.src = e.target.result;
                preview.removeAttribute('hidden');
            }
        }
        fr.readAsDataURL(fileList[0]);

        var fr_e = new FileReader();
        fr_e.onloadend = function(e) {
            document.getElementById('file_hash').value = CryptoJS.SHA256(bufferToHex(e.target.result));
            var aes_result = aes_encrypt(bufferToHex(e.target.result), secret_key, iv); //input is string
            var encrypted_key = encrypt.encrypt(secret_key.toString());
            var encrypted_iv = encrypt.encrypt(iv.toString());
            let key_blob = new File([encrypted_key], "key", {
                type: "text/plain",
                lastModified: new Date()
            });
            let iv_blob = new File([encrypted_iv], "iv", {
                type: "text/plain",
                lastModified: new Date()
            });
            var encryptedfile = new File([aes_result], fileList[0].name, {
                type: fileList[0].type,
                lastModified: fileList[0].lastModified
            })
            dt_f.items.add(encryptedfile);
            document.getElementById('file_input').files = dt_f.files;
            dt_k.items.add(key_blob);
            document.getElementById('e_key').files = dt_k.files;
            dt_i.items.add(iv_blob);
            document.getElementById('e_iv').files = dt_i.files;
            document.getElementById('fileDeleteButton').removeAttribute('style');
            document.getElementById('addfilebutton').disabled = true;
            fastUploadCheck();
        }
        fr_e.readAsBinaryString(fileList[0]);
    }
})

var inputfile = document.querySelector('#file_input');
inputfile.addEventListener('change', function(e) {
    fileList = e.target.files;
    document.getElementById('selectfilename').innerHTML = fileList[0].name;
    if (window.FileReader) {
        var preview = document.querySelector('img');
        var fr = new FileReader();
        fr.onloadend = function(e) {
            if (previewType.includes(fileList[0].type)) {
                preview.src = e.target.result;
                preview.removeAttribute('hidden');
            }
        }
        fr.readAsDataURL(fileList[0]);
        var fr_e = new FileReader();
        fr_e.onloadend = function(e) {
            document.getElementById('file_hash').value = CryptoJS.SHA256(bufferToHex(e.target.result));
            var aes_result = aes_encrypt(bufferToHex(e.target.result), secret_key, iv);
            var encrypted_key = encrypt.encrypt(secret_key.toString());
            var encrypted_iv = encrypt.encrypt(iv.toString());
            let key_blob = new File([encrypted_key], "key", {
                type: "text/plain",
                lastModified: new Date()
            });
            let iv_blob = new File([encrypted_iv], "iv", {
                type: "text/plain",
                lastModified: new Date()
            });
            var encryptedfile = new File([aes_result], fileList[0].name, {
                type: fileList[0].type,
                lastModified: fileList[0].lastModified
            })
            dt_f.items.add(encryptedfile);
            document.getElementById('file_input').files = dt_f.files;
            dt_k.items.add(key_blob);
            document.getElementById('e_key').files = dt_k.files;
            dt_i.items.add(iv_blob);
            document.getElementById('e_iv').files = dt_i.files;
            document.getElementById('fileDeleteButton').removeAttribute('style');
            document.getElementById('addfilebutton').disabled = true;
            fastUploadCheck();
        }
        fr_e.readAsArrayBuffer(fileList[0]);
    }
})

function fastUploadCheck() {
    // console.log(document.getElementById('file_hash').innerHTML);
    $.ajax({
        type: 'POST',
        url: this.url,
        data: {
            'fun_select': 'hash_check',
            'file_hash_val': document.getElementById('file_hash').value,
        },
        success: function(data) {
            console.log(data.condition);
            if (data.condition == 0) {
                document.getElementById('fileUploadButton').disabled = false;
            } else if (data.condition == 1) {
                alert('该文件已经上传过啦~');
                fileDelete();
            } else if (data.condition == 2) {
                // fast upload
                document.getElementById('fileUploadButton').disabled = false;
                document.getElementById('fileUploadButton').setAttribute('onclick', 'fileFastUpload()');
            } else {
                alert('未知情况');
            }
        },
        error: function() {
            // console.log('server error')
            alert('网络错误或服务器异常，请稍后重试');
        }
    })
}

function fileUpload() {
    if (!document.getElementById('file_input').files[0]) {
        alert('未选择文件！');
    } else {
        // console.log(document.getElementById('file_input').files[0]);
        document.getElementById('fileform').submit();
        // console.log(CryptoJS.AES.decrypt(temp, secret_key, { iv: iv, mode: CryptoJS.mode.OFB, padding: CryptoJS.pad.Pkcs7 }).toString());
    }
    // 
}

function fileFastUpload() {
    if (!document.getElementById('file_hash')) {
        alert('未选择文件！');
    } else {
        document.getElementById('fastuploadform').submit();
    }
}

function fileDelete() {
    $('#file_input').val('');
    document.getElementById('selectfilename').innerHTML = '';
    fileList = null;
    dt_f.clearData()
    dt_k.clearData()
    dt_i.clearData();
    document.getElementById('fileDeleteButton').setAttribute('style', 'display: none;');
    document.querySelector('img').hidden = true;
    document.getElementById('addfilebutton').disabled = false;
    document.getElementById('file_hash').value = null;
    document.getElementById('fileUploadButton').setAttribute('onclick', 'fileUpload()');
}

$(document).ready(function() {
    mes = $('#flash_mes').text();
    if (mes.length > 1) {
        alert(mes);
    }
});


document.querySelectorAll('.delform').forEach(item => {
    item.addEventListener('submit', event => {
        if (confirm('您确定要删除该文件吗')) {
            this.submit();
        } else {
            event.preventDefault();
        }
    })
})

document.querySelectorAll('.shareform').forEach(item => {
    item.addEventListener('submit', event => {
        if (confirm('您确定要分享该文件吗')) {
            this.submit();
        } else {
            event.preventDefault();
        }
    })
})