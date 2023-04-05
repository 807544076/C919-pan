from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from flask_session import Session
from linksql import C919SQL
import nacl.encoding
import nacl.hash
import time
import random
from send_mail import sendMail
from datetime import timedelta
from os import remove
import upload
from userKeyGen import create_key, get_server_pubkey, server_decrypt, aes_decrypt, user_decrypt, aes_decrypt_download, user_encrypt
import base64
import binascii

certFile = './cert/c919pan.xyz_bundle.pem'
keyFile = './cert/c919pan.xyz.key'
fileTypeWhiteList = ['jpg', 'png', 'gif', 'jpeg', 'bmp', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt']

HASHER = nacl.hash.sha512
hash_msg = bytes(str(time.time()), 'utf-8')
digest = HASHER(hash_msg, encoder=nacl.encoding.HexEncoder)

pages = Flask(__name__)
pages.secret_key = digest

pages.config['SESSION_PERMANENT'] = True
pages.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=12)
pages.config['SESSION_TYPE'] = 'filesystem'
Session(pages)


def mail_content_link():
    token = HASHER(bytes(digest.decode('utf-8') + str(session.get('start_time')), 'utf-8'),
                   encoder=nacl.encoding.HexEncoder).decode('utf-8')
    randompage = 'https://c919pan.xyz/email_check/' + str(token)
    message = """
        <body style="height: 100vh; display: flex; justify-content: center; align-items: center; background-color: linear-gradient(200deg, #cbdcf5, #fce7ef);">
            <div class="show" style="font: size 12px;">
                <p>您好，</p>
                <p>这里是 C919 Pan，您的验证连接为：</p><br>
                <a style="font-size: 30px;" href="
                """ + randompage + """
                "><strong>=>点击进行验证<=</strong></a><br>
                <p>本连接有效期为 5 分钟，仅可使用一次。</p>
                <p>您没有收到来自 C919 的验证要求，却收到了这封邮件？如果是这样，您的账号可能有安全隐患。请尽快更改您的密码。</p>
                <p>诚挚祝福，</p>
                <p>来自 C919 指挥部</p>
            </div>
        </body>
    """
    return message


def mail_content_token():
    randomtoken = random.randint(100000, 999999)
    session['randomtoken'] = randomtoken
    message = """
        <body style="height: 100vh; display: flex; justify-content: center; align-items: center; background-color: linear-gradient(200deg, #cbdcf5, #fce7ef);">
            <div class="show" style="font: size 12px;">
                <p>您好，</p>
                <p>这里是 C919 Pan，您的验证码为：</p>
                <br><h3> """ + str(randomtoken) + """</h3><br>
                <p>验证码有效期为 5 分钟，仅可使用一次。</p>
                <p>您没有收到来自 C919 的验证要求，却收到了这封邮件？如果是这样，您的账号可能有安全隐患。请尽快更改您的密码。</p>
                <p>诚挚祝福，</p>
                <p>来自 C919 指挥部</p>
            </div>
        </body>
    """
    return message


def mail_authorization_code(filename, code):
    message = """
        <body style="height: 100vh; display: flex; justify-content: center; align-items: center; background-color: linear-gradient(200deg, #cbdcf5, #fce7ef);">
            <div class="show" style="font: size 12px;">
                <p>您好，</p>
                <p>这里是 C919 Pan，您的文件""" + filename + """的授权码为：</p>
                <br><h3> """ + str(code) + """</h3><br>
                <p>该授权码在您取消分享或分享过期之前均有效，快去分享您的文件吧。</p>
                <p>诚挚祝福，</p>
                <p>来自 C919 指挥部</p>
            </div>
        </body>
    """
    return message


@pages.route('/waitfor')
def waitfor():
    return render_template('waitfor.html')


@pages.route('/testUpload', methods=['GET', 'POST'])
def testUpload():
    if request.method == 'POST':
        return 'Let\'s back to Index'
        db = C919SQL()
        db.search_link()
        userUUID = str(db.selectUserUID(session.get('h_email'))[0])
        db.end_link()
        # get file(aes encrypt), key(rsa encrypt), iv(rsa encrypt)
        file = request.files['file']
        key = request.files['e_key']
        iv = request.files['e_iv']
        k = base64.b64decode(key.read())
        i = base64.b64decode(iv.read())
        c = base64.b64decode(file.read())
        # key, iv ras decrypt
        key = server_decrypt(userUUID, k)
        iv = server_decrypt(userUUID, i)
        key = binascii.unhexlify(key)
        iv = binascii.unhexlify(iv)
        # file aes decrypt
        filecont = aes_decrypt(key, iv, c)  # c is bytes
        filecont = binascii.unhexlify(filecont.decode())  # filecont is original bytes(non-encrypt)
        filename = request.files['file'].filename
        filename_plain = filename[::-1].split('.', 1)[1][::-1]
        fileExtension = filename.split('.')[-1]
        if len(filename) > 45:
            return '文件名过长,超过45个字符'
        if fileExtension not in fileTypeWhiteList:
            return '不允许的文件类型'
        result = upload.upload(session.get('h_email'), filecont, filename_plain)  # filecont is bytes
        return result
    else:
        sql = C919SQL()
        sql.admin_link()
        uid = sql.selectUserUID(session.get('h_email'))[0]
        sql.end_link()
        pubk = get_server_pubkey(uid)  # sent pubk
        # todo: sign
        # return render_template('testUpload.html', pubk=pubk)
        return '<h1> Congratulations! </h1><h1> You find an Easter egg! </h1><h1> Have a nice day! </h1>'


@pages.route('/')
def to_index():
    if session.get('name'):
        return render_template('index.html', userName=session.get('name'))
    else:
        return redirect(url_for('index'))


@pages.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        session['check_fun'] = 0  # 0 代表注册检测，1 代表忘记密码检测
        session['forgot_flag'] = 0  # 转跳标记位
        if session.get('name'):
            db = C919SQL()
            db.search_link()
            re = db.select_all_file(session.get('uid'))  # 第四项 stamp 为了文件下载页面铺垫
            pubk = get_server_pubkey(session.get('uid'))  # sent pubk
            return render_template('index.html', userName=session.get('name'), filelist=re, pubk=pubk)
        else:
            return redirect(url_for('login'))
    if request.method == 'POST':
        db = C919SQL()
        db.admin_link()
        if not request.form['fun_select']:
            return render_template('403.html')
        if request.form['fun_select'] == 'file_delete':
            del_stamp = request.form['delfilestamp']
            upload.delete_file(del_stamp)
            db.delete_file(del_stamp)
            flash('删除成功')
            return redirect(url_for('index'))
        if request.form['fun_select'] == 'file_share':
            share_stamp = request.form['sharefilestamp']
            code = random.randint(100000, 999999)
            hcode = HASHER(bytes(str(code), 'utf-8'), encoder=nacl.encoding.HexEncoder).decode('utf-8')
            f = open('./userKey/' + str(session.get('uid')) + '/file_aes/' + share_stamp + '/code.key', 'wb')
            f.write(user_encrypt(session.get('uid'), str(code).encode('utf-8')))
            f.close()
            db.set_shared(share_stamp, True)
            db.set_authorization_code(share_stamp, hcode)
            flash('您的授权码为：' + str(code))
            return redirect(url_for('index'))
        if request.form['fun_select'] == 'file_upload':
            userUUID = str(db.selectUserUID(session.get('h_email'))[0])
            # get file(aes encrypt), key(rsa encrypt), iv(rsa encrypt)
            file = request.files['file']
            key = request.files['e_key']
            iv = request.files['e_iv']
            k = base64.b64decode(key.read())
            i = base64.b64decode(iv.read())
            c = base64.b64decode(file.read())
            # key, iv ras decrypt
            key = server_decrypt(userUUID, k)
            iv = server_decrypt(userUUID, i)
            key = binascii.unhexlify(key)
            iv = binascii.unhexlify(iv)
            # file aes decrypt
            filecont = aes_decrypt(key, iv, c)  # c is bytes
            filecont = binascii.unhexlify(filecont.decode())  # filecont is original bytes(non-encrypt)
            filename = request.files['file'].filename
            filename_plain = filename[::-1].split('.', 1)[1][::-1]
            fileExtension = filename.split('.')[-1]
            if len(filename) > 45:
                flash('文件名过长,超过45个字符')
                return redirect(url_for('index'))
            if fileExtension not in fileTypeWhiteList:
                flash('不允许的文件类型')
                return redirect(url_for('index'))
            result = upload.upload(session.get('h_email'), filecont, filename)  # filecont is bytes
            flash('上传成功！')
            return redirect(url_for('index'))
        db.end_link()


@pages.route('/login')
def login():
    if session.get('name'):
        return redirect(url_for('index', userName=session.get('name')))
    else:
        session['csrf'] = digest.decode('utf-8')
        return render_template('login.html', csrf=session.get('csrf'))


@pages.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        session['email'] = request.form['email']
        bytes_email = bytes(request.form['email'], 'utf-8')
        email = HASHER(bytes_email, encoder=nacl.encoding.HexEncoder).decode('utf-8')
        session['h_email'] = email
        if request.form['email'] == '':
            flash('请输入邮箱')
            return redirect(url_for('forgot'))
        else:
            sql = C919SQL()
            sql.search_link()
            if sql.check_email(email):
                sql.end_link()
                session['start_time'] = time.time()
                message = mail_content_token()
                sendMail(message, 'C919邮箱验证', 'C919指挥部', 'User', request.form['email'])
                session['start_time'] = time.time()
                session['check_fun'] = 1
                return redirect(url_for('email_check_code'))
            else:
                sql.end_link()
                flash('邮箱未注册')
                return redirect(url_for('forgot'))
    else:
        if session.get('name'):
            session.clear()
        return render_template('forgot.html')


@pages.route('/set_password', methods=['GET', 'POST'])
def set_password():
    if request.method == 'POST':
        bytes_password = bytes(request.form['password'], 'utf-8')
        passwd = HASHER(bytes_password, encoder=nacl.encoding.HexEncoder).decode('utf-8')
        if request.form['password'] == '$2a$12$26adcdf68dfb176d4c876u6ocbRW0ZNqedwx5ZlKIxmPI/H/wwele':
            flash('请输入密码')
            return redirect(url_for('set_password', user_email=session.get('email')))
        else:
            sql = C919SQL()
            sql.admin_link()
            if sql.reset_passwd(session.get('h_email'), passwd):
                flash('密码设置成功')
                sql.end_link()
                session['forgot_flag'] = 0
                return redirect(url_for('login'))
            else:
                flash('密码设置失败')
                sql.end_link()
                session['forgot_flag'] = 1
                return redirect(url_for('set_password', user_email=session.get('email')))
    else:
        if session.get('forgot_flag') == 1:
            return render_template('set_password.html', user_email=session.get('email'))
        else:
            return render_template('403.html')


@pages.route('/testpage_register', methods=['GET', 'POST'])
def testpage_register():
    if session.get('name'):
        return redirect(url_for('index', userName=session.get('name')))
    if request.method == 'POST':
        if request.form['get_csrf'] == digest.decode('utf-8'):
            bytes_email = bytes(request.form['email'], 'utf-8')
            bytes_password = bytes(request.form['password'], 'utf-8')
            session['r_name'] = (request.form['username'])  # 用户名
            session['h_email'] = (HASHER(bytes_email, encoder=nacl.encoding.HexEncoder).decode('utf-8'))  # hash邮箱
            session['h_password'] = (HASHER(bytes_password, encoder=nacl.encoding.HexEncoder).decode('utf-8'))  # hash密码
            session['email'] = (request.form['email'])  # 原邮箱
            sql = C919SQL()
            sql.search_link()
            if not sql.check_email(session.get('h_email')):
                sql.end_link()
                session['start_time'] = time.time()
                message = mail_content_token()
                sendMail(message, 'C919注册邮箱验证', 'C919指挥部', 'New User', request.form['email'])
                session['check_fun'] = 0
                return redirect(url_for('email_check_code'))
            else:
                sql.end_link()
                flash('邮箱已注册！请重新输入')
                return redirect(url_for('login'))
        else:
            return render_template('403.html')
    else:
        return redirect(url_for('login'))


@pages.route('/testpage_login', methods=['GET', 'POST'])
def testpage_login():
    session['forget_flag'] = 0
    if session.get('name'):
        return redirect(url_for('index', userName=session.get('name')))
    if request.method == 'POST':
        if request.form['get_csrf'] == digest.decode('utf-8'):
            bytes_email = bytes(request.form['email'], 'utf-8')
            bytes_password = bytes(request.form['password'], 'utf-8')
            h_email = HASHER(bytes_email, encoder=nacl.encoding.HexEncoder).decode('utf-8')
            session['h_email'] = h_email
            h_passwd = HASHER(bytes_password, encoder=nacl.encoding.HexEncoder).decode('utf-8')
            selectSQL = C919SQL()
            selectSQL.search_link()
            if selectSQL.check_email(h_email):
                if selectSQL.check_password(h_email, h_passwd):
                    session['name'] = \
                        selectSQL.select_username(
                            HASHER(bytes_email, encoder=nacl.encoding.HexEncoder).decode('utf-8'))[0]
                    session['uid'] = \
                        selectSQL.selectUserUID(HASHER(bytes_email, encoder=nacl.encoding.HexEncoder).decode('utf-8'))[
                            0]
                    session['email'] = request.form['email']
                    return redirect(url_for('index', userName=session.get('name')))
                else:
                    flash('密码错误！')
                    return redirect(url_for('login'))
            else:
                flash('用户不存在！')
                return redirect(url_for('login'))
        else:
            print('csrf error')
            return render_template('403.html')
    else:
        return redirect(url_for('login'))


@pages.route('/email_check/<token>')
def email_check(token):
    if time.time() - session.get('start_time') > 300:
        flash('验证超时！')
        return redirect(url_for('login'))
    if session.get('check_fun') == 0:
        sql = C919SQL()
        sql.admin_link()
        sql.userCreate(session.get('r_name'), session.get('h_email'), session.get('h_password'))
        sql.end_link()
        flash('注册成功！')
        return redirect(url_for('login'))
    else:
        session['check_fun'] = 0
        session['forgot_flag'] = 1
        return redirect(url_for('set_password', user_email=session.get('email')))


@pages.route('/email_check_code', methods=['GET', 'POST'])
def email_check_code():
    if request.method == 'POST':
        if time.time() - session.get('start_time') > 300:
            flash('验证超时！')
            return redirect(url_for('login'))
        if session.get('randomtoken') != int(request.form['check']):
            flash('验证码错误')
            return redirect(url_for('email_check_code'))
        if session.get('check_fun') == 0:
            sql = C919SQL()
            sql.admin_link()
            sql.userCreate(session.get('r_name'), session.get('h_email'), session.get('h_password'))
            uid = sql.selectUserUID(session.get('h_email'))[0]
            sql.end_link()
            create_key(uid)  # 创建公私钥对
            flash('注册成功！')
            return redirect(url_for('login'))
        else:
            session['check_fun'] = 0
            session['forgot_flag'] = 1
            return redirect(url_for('set_password', user_email=session.get('email')))
    else:
        return render_template('email_check.html')


@pages.route('/file/<stamp>', methods=['POST', 'GET'])
def file(stamp):
    if request.method == 'GET':
        db = C919SQL()
        db.search_link()
        result = db.select_file_stamp(stamp)
        owner = db.select_username_by_uid(result[2])[0]
        if not result:
            return render_template('404.html')
        if result[2] != session.get('uid'):
            return render_template('403.html')
        db.end_link()
        return render_template('fileinfo.html', file=result, owner=owner)
    else:
        if request.form['select_fun'] == 'disshare':
            db = C919SQL()
            db.admin_link()
            remove('./userKey/' + str(session.get('uid')) + '/file_aes/' + stamp + '/code.key')
            db.set_shared(stamp, False)
            db.end_link()
            return redirect(url_for('file', stamp=stamp))
        if request.form['select_fun'] == 'showcode':
            db = C919SQL()
            db.search_link()
            result = db.select_file_stamp(stamp)
            f = open('./userKey/' + str(session.get('uid')) + '/file_aes/' + stamp + '/code.key', 'rb')
            code = user_decrypt(str(session.get('uid')), f.read()).decode()
            f.close()
            mes = mail_authorization_code(result[1], code)
            sendMail(mes, 'C919授权码', 'C919指挥部', 'User', session.get('email'))
            return redirect(url_for('file', stamp=stamp))
        else:
            return render_template('403.html')


@pages.route('/sharefile/<stamp>')
def sharefile(stamp):
    db = C919SQL()
    db.search_link()
    result = db.select_file_stamp(stamp)
    owner = db.select_username_by_uid(result[2])[0]
    if not result:
        return render_template('404.html')
    if not result[6]:
        return render_template('403.html')
    if session.get('uid') == result[2]:
        return redirect(url_for('file', stamp=stamp))
    db.end_link()
    return render_template('sharefile.html', file=result, owner=owner)


@pages.route('/download/<stamp>', methods=['POST'])
def download(stamp):
    flag = False
    db = C919SQL()
    db.search_link()
    result = db.select_file_stamp(stamp)
    if not result:
        return redirect(url_for('404'))
    aes_path = './userKey/' + str(result[2]) + '/file_aes/' + stamp + '/'
    file_path = './fileStorage/' + str(result[2]) + '/' + result[1] + result[4]
    code = request.form['code']
    hcode = HASHER(bytes(str(code), 'utf-8'), encoder=nacl.encoding.HexEncoder).decode('utf-8')
    if result[6] == 1 and hcode == result[9]:    # 已分享且授权码正确
        flag = True
    elif session.get('uid') == result[2]:
        flag = True
    db.end_link()
    if flag:
        f = open(aes_path + 'key.key', 'rb')
        e_k = f.read()
        f.close()
        key = user_decrypt(result[2], e_k)
        f = open(aes_path + 'iv.key', 'rb')
        e_i = f.read()
        f.close()
        iv = user_decrypt(result[2], e_i)
        f = open(file_path, 'rb')
        e_filecont = f.read()
        f.close()
        filecont = aes_decrypt_download(key, iv, e_filecont)
        f = open('./temp/' + result[1], 'wb')
        f.write(filecont)
        f.close()
        return send_file('./temp/' + result[1], as_attachment=True)
    else:
        return send_file(file_path)


@pages.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))


@pages.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


@pages.errorhandler(403)
def access_denied(error):
    return render_template('403.html')


@pages.errorhandler(400)
def bad_request(error):
    return render_template('400.html')


if __name__ == '__main__':
    pages.run(debug=True, ssl_context=(certFile, keyFile), port=443)
