from flask import Flask, render_template, request, redirect, url_for, flash
from linksql import C919SQL
import nacl.encoding
import nacl.hash
import time
import random
from send_mail import sendMail

certFile='./cert/selfsigned.crt'
keyFile='./cert/selfsigned.key'

HASHER = nacl.hash.sha512
hash_msg = bytes(str(time.time()), 'utf-8')
digest = HASHER(hash_msg, encoder=nacl.encoding.HexEncoder)

pages=Flask(__name__)
pages.secret_key = digest

r_info = ['', '', '', '']   # [0]用户名，[1]hash邮箱，[2]hash密码，[3]原邮箱
check_num = []
start_time = [0]


@pages.route('/')
def to_index():
    return redirect(url_for('index'))


@pages.route('/index')
def index():
    if request.args.get('userName'):
        username = request.args.get('userName')
        return render_template('index.html', userName=username)
    else:
        return render_template('index.html')


@pages.route('/login')
def login():
    return render_template('login.html')


@pages.route('/forgot')
def forgot():
    return render_template('template.html',pageName='forgot')


@pages.route('/testpage_register',methods=['GET', 'POST'])
def testpage_register():
    if request.method == 'POST':
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
        return render_template('login.html')


@pages.route('/testpage_login', methods=['GET', 'POST'])
def testpage_login():
    if request.method == 'POST':
        bytes_email = bytes(request.form['email'], 'utf-8')
        bytes_password = bytes(request.form['password'], 'utf-8')
        selectSQL = C919SQL()
        selectSQL.search_link()
        if selectSQL.select_email(HASHER(bytes_email, encoder=nacl.encoding.HexEncoder).decode('utf-8')):
            if selectSQL.select_password(HASHER(bytes_password, encoder=nacl.encoding.HexEncoder).decode('utf-8')):
                return redirect(url_for('index', userName=selectSQL.select_username(HASHER(bytes_email, encoder=nacl.encoding.HexEncoder).decode('utf-8'))[0]))
            else:
                flash('密码错误！')
                return redirect(url_for('login'))
        else:
            flash('用户不存在！')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')


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
            return redirect(url_for('index', userName=r_info[0]))
        else:
            flash('验证码错误！请重新输入')
            print(request.form['check'])
            return redirect(url_for('email_check'))
    else:
        return render_template('email_check.html')


@pages.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


if __name__ == '__main__':
    pages.run(debug=True,ssl_context=(certFile,keyFile),port=443)