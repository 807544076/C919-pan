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

@pages.errorhandler(404)
def page_not_found(error):
    return render_template('template.html',pageName='404')

if __name__ == '__main__':
    pages.run(debug=True)