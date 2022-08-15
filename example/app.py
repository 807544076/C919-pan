from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_session import Session
from linksql import C919SQL
import nacl.encoding
import nacl.hash
import time
import random
from send_mail import sendMail
from datetime import timedelta

certFile='./cert/selfsignedCertificate.pem'
keyFile='./cert/privateKey.pem'

HASHER = nacl.hash.sha512
hash_msg = bytes(str(time.time()), 'utf-8')
digest = HASHER(hash_msg, encoder=nacl.encoding.HexEncoder)

pages=Flask(__name__)
pages.secret_key = digest

pages.config['SESSION_PERMANENT'] = True
pages.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=12)
pages.config['SESSION_TYPE'] = 'filesystem'
Session(pages)

r_info = ['', '', '', '']   # [0]用户名，[1]hash邮箱，[2]hash密码，[3]原邮箱
check_num = []
start_time = [0]


@pages.route('/')
def to_index():
    if session.get('name'):
        return render_template('index.html', userName=session.get('name'))
    else:
        return redirect(url_for('index'))


@pages.route('/index')
def index():
    if session.get('name'):
        return render_template('index.html', userName=session.get('name'))
    else:
        return redirect(url_for('login'))


@pages.route('/login')
def login():
    if session.get('name'):
        return redirect(url_for('index', userName=session.get('name')))
    else:
        session['csrf'] = digest.decode('utf-8')
        return render_template('login.html', csrf=session.get('csrf'))


@pages.route('/forgot')
def forgot():
    if request.method == 'POST':
        email = request.form['email']
        if email == '':
            flash('请输入邮箱')
            return redirect(url_for('forgot'))
        else:
            sql = C919SQL()
            if sql.check_email(email):
                flash('已发送验证邮件，请查收')
                sendMail(email)
                return redirect(url_for('set_password'))
            else:
                flash('邮箱未注册')
                return redirect(url_for('forgot'))
    return render_template('forgot.html', pageName='forgot')


@pages.route('/set_password')
def setpassword():
    if request.method == 'POST':
        passwd = request.form['passwd']
        if passwd == '':
            flash('请输入密码')
            return redirect(url_for('set_password'))
        else:
            sql = C919SQL()
            if sql.set_password(passwd):
                flash('密码设置成功')
                return redirect(url_for('login'))
            else:
                flash('密码设置失败')
                return redirect(url_for('set_password'))
        return redirect(url_for('login'))
    return render_template('set_password.html', pageName='setpassword')

@pages.route('/testpage_register',methods=['GET', 'POST'])
def testpage_register():
    if session.get('name'):
        return redirect(url_for('index', userName=session.get('name')))
    if request.method == 'POST':
        if request.form['get_csrf'] == digest.decode('utf-8'):
            bytes_email = bytes(request.form['email'], 'utf-8')
            bytes_password = bytes(request.form['password'], 'utf-8')
            r_info[0] = (request.form['username'])
            r_info[1] = (HASHER(bytes_email, encoder=nacl.encoding.HexEncoder).decode('utf-8'))
            r_info[2] = (HASHER(bytes_password, encoder=nacl.encoding.HexEncoder).decode('utf-8'))
            r_info[3] = (request.form['email'])
            sql = C919SQL()
            sql.search_link()
            if not sql.select_email(r_info[1]):
                sql.end_link()
                check_num.append(random.randint(100000, 999999))
                message = """
                                <body style="height: 100vh; display: flex; justify-content: center; align-items: center; background-color: linear-gradient(200deg, #cbdcf5, #fce7ef);">
                                    <div class="show" style="font: size 12px;">
                                        <p>您好，</p>
                                        <p>这里是 C919 中传放心传，您的验证码为：</p><br>
                                        <p style="font-size: 30px;"><strong>""" + str(check_num[0]) + """</strong></p><br>
                                        <p>本验证码有效期为 5 分钟，仅可使用一次。</p>
                                        <p>您没有收到来自 C919 的输入验证码要求，却收到了这封邮件？如果是这样，您的账号可能有安全隐患。请尽快更改您的密码。</p>
                                        <p>诚挚祝福，</p>
                                        <p>来自 C919 指挥部</p>
                                    </div>
                                </body>
                                """
                sendMail(message, 'C919注册邮箱验证', 'C919指挥部', 'New User', request.form['email'])
                start_time[0] = time.time()
                return redirect(url_for('email_check'))
            else:
                sql.end_link()
                flash('邮箱已注册！请重新输入')
                return redirect(url_for('login'))
        else:
            return redirect(url_for('403'))
    else:
        return redirect(url_for('login'))


@pages.route('/testpage_login', methods=['GET', 'POST'])
def testpage_login():
    if session.get('name'):
        return redirect(url_for('index', userName=session.get('name')))
    if request.method == 'POST':
        if request.form['get_csrf'] == digest.decode('utf-8'):
            bytes_email = bytes(request.form['email'], 'utf-8')
            bytes_password = bytes(request.form['password'], 'utf-8')
            selectSQL = C919SQL()
            selectSQL.search_link()
            if selectSQL.select_email(HASHER(bytes_email, encoder=nacl.encoding.HexEncoder).decode('utf-8')):
                if selectSQL.select_password(HASHER(bytes_password, encoder=nacl.encoding.HexEncoder).decode('utf-8')):
                    session['name']=selectSQL.select_username(HASHER(bytes_email, encoder=nacl.encoding.HexEncoder).decode('utf-8'))[0]
                    return redirect(url_for('index', userName=session.get('name')))
                else:
                    flash('密码错误！')
                    return redirect(url_for('login'))
            else:
                flash('用户不存在！')
                return redirect(url_for('login'))
        else:
            return redirect(url_for('403'))
    else:
        return redirect(url_for('login'))


@pages.route('/email_check', methods=['GET', 'POST'])
def email_check():
    if request.method == 'POST':
        if time.time() - start_time[0] > 300:
            print(time.time() - start_time[0])
            flash('验证超时！请重新输入')
            return redirect(url_for('login'))
        if request.form['check'] == str(check_num[0]):
            sql = C919SQL()
            sql.admin_link()
            sql.userCreate(r_info[0], r_info[1], r_info[2])
            sql.end_link()
            session['name'] = r_info[0]
            return redirect(url_for('index', userName=session.get('name')))
        else:
            flash('验证码错误！请重新输入')
            print(request.form['check'])
            return redirect(url_for('email_check'))
    else:
        return render_template('403.html')


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
    pages.run(debug=True,  ssl_context=(certFile,  keyFile),  port=443)

