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

var secret_key = GenPBKDF2('hello aes', 256);
var iv = CryptoJS.lib.WordArray.random(128 / 8);
var dt_f = new DataTransfer();
var dt_k = new DataTransfer();
var dt_i = new DataTransfer();
var temp;
var fileList;
var encrypt = new JSEncrypt();
encrypt.setPublicKey(document.getElementById('pubk').innerHTML);

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
    document.getElementById('file_input').files = fileList;
    if (window.FileReader) {
        var preview = document.querySelector('img');
        var fr = new FileReader();
        fr.onloadend = function(e) {
            preview.src = e.target.result;
            preview.removeAttribute('hidden');
        }
        fr.readAsDataURL(fileList[0]);

        var fr_e = new FileReader();
        fr_e.onloadend = function(e) {
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
        }
        fr_e.readAsBinaryString(fileList[0]);
    }
})

var inputfile = document.querySelector('#file_input');
inputfile.addEventListener('change', function(e) {
    fileList = e.target.files;
    console.log(fileList[0])
    if (window.FileReader) {
        var preview = document.querySelector('img');
        var fr = new FileReader();
        fr.onloadend = function(e) {
            preview.src = e.target.result;
            preview.removeAttribute('hidden');
        }
        fr.readAsDataURL(fileList[0]);

        var fr_e = new FileReader();
        fr_e.onloadend = function(e) {
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
        }
        fr_e.readAsArrayBuffer(fileList[0]);
    }
})

function Upload() {
    if (!document.getElementById('file_input').files[0]) {
        alert('no file selected');
    } else {
        // console.log(document.getElementById('file_input').files[0]);
        document.getElementById('fileform').submit();
        // console.log(CryptoJS.AES.decrypt(temp, secret_key, { iv: iv, mode: CryptoJS.mode.OFB, padding: CryptoJS.pad.Pkcs7 }).toString());
    }
    // 
}