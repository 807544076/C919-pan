from flask import Flask,render_template,request,redirect,url_for
from form import LoginForm,RegisterForm,PasswordForm

pages=Flask(__name__)

@pages.route('/')
def index():
    return render_template('template.html',pageName='index')

@pages.route('/login')
def login():
    return render_template('login.html')

@pages.route('/register')
def register():
    return render_template('template.html',pageName='register')

@pages.route('/forgot')
def forgot():
    return render_template('template.html',pageName='forgot')

@pages.route('/testpage_register',methods=['GET','POST'])
def testpage_register():
    if request.method=='POST':
        for item in request.form:
            print(request.form[item])
        return redirect(url_for('index'))
    else:
        return render_template('login.html')

@pages.route('/testpage_login',methods=['GET','POST'])
def testpage_login():
    if request.method=='POST':
        for item in request.form:
            print(request.form[item])
        return redirect(url_for('index'))
    else:
        return render_template('login.html')

@pages.errorhandler(404)
def page_not_found(error):
    return render_template('template.html',pageName='404')

if __name__ == '__main__':
    pages.run(debug=True)