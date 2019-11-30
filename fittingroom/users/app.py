 from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from flask import Response
from camera import VideoCamera

app = Flask(__name__)

# Articles = Articles()


@app.route('/')
def index():
    return render_template('home.html')



@app.route("/login/", methods=['POST'])
def move_forward():
    forward_message = "Moving Forward..."
    return render_template('afterLogin.html', forward_message=forward_message)



@app.route('/about')
def about():
    return render_template('about.html')


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [validators.DataRequired(
    ), validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.form == 'POST' and form.validate():
        return render_template('register.html')
    return render_template('register.html', form=form)

# @app.route('/articles/<string:id>/')
# def article(id):
 #   return render_template('article.html', id=id)


if __name__ == '__main__':
    app.run(debug='true')