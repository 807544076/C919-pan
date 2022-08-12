from flask import Flask, render_template, request, redirect, url_for, flash
from linksql import C919SQL
import nacl.encoding
import nacl.hash
import time

HASHER = nacl.hash.sha512
hash_msg = bytes(str(time.time()), 'utf-8')
digest = HASHER(hash_msg, encoder=nacl.encoding.HexEncoder)

pages=Flask(__name__)
pages.secret_key = digest


@pages.route('/')
def index():
    return render_template('template.html', pageName='index')


@pages.route('/login')
def login():
    return render_template('login.html')

# @pages.route('/register')
# def register():
#     return render_template('template.html',pageName='register')


@pages.route('/forgot')
def forgot():
    return render_template('template.html',pageName='forgot')


@pages.route('/testpage_register',methods=['GET','POST'])
def testpage_register():
    if request.method=='POST':
        testSQL=C919SQL()
        testSQL.admin_link()
        bytes_email = bytes(request.form['email'], 'utf-8')
        bytes_password = bytes(request.form['password'], 'utf-8')
        testSQL.userCreate(request.form['username'], HASHER(bytes_email, encoder=nacl.encoding.HexEncoder).decode('utf-8'), HASHER(bytes_password, encoder=nacl.encoding.HexEncoder).decode('utf-8'))
        testSQL.end_link()
        return redirect(url_for('index'))
    else:
        return render_template('login.html')


@pages.route('/testpage_login',methods=['GET','POST'])
def testpage_login():
    if request.method=='POST':
        bytes_email = bytes(request.form['email'], 'utf-8')
        bytes_password = bytes(request.form['password'], 'utf-8')
        selectSQL = C919SQL()
        selectSQL.search_link()
        if selectSQL.select_email(HASHER(bytes_email, encoder=nacl.encoding.HexEncoder).decode('utf-8')):
            if selectSQL.select_password(HASHER(bytes_password, encoder=nacl.encoding.HexEncoder).decode('utf-8')):
                return redirect(url_for('index'))
            else:
                flash('密码错误！')
                return redirect(url_for('login'))
        else:
            flash('用户不存在！')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')


@pages.errorhandler(404)
def page_not_found(error):
    return render_template('template.html', pageName='404')


if __name__ == '__main__':
    pages.run(debug=True)