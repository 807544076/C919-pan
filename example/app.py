from flask import Flask
from flask import render_template

pages=Flask(__name__)

@pages.route('/')
def index():
    return render_template('template.html',pageName='index')

@pages.route('/login')
def login():
    return render_template('template.html',pageName='login')

@pages.route('/register')
def register():
    return render_template('template.html',pageName='register')

@pages.route('/forgot')
def forgot():
    return render_template('template.html',pageName='forgot')

if __name__ == '__main__':
    pages.run(debug=True)