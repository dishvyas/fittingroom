from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from flask import Response
from model2d import get2dfit
import os

app = Flask(__name__)

UPLOAD_FOLDER = '/static/uploads/'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('home.html')


@app.route("/login/", methods=['POST'])
def move_forward():
    return redirect(url_for("upload"))


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('uploadphoto.html')
    elif request.method == 'POST':
        file = request.files['file']

    if file.filename == '':
        return render_template('index.html', msg='No file selected')

    if file and allowed_file(file.filename):
        file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))
    str = "/static/uploads/" + file.filename
    print(file.filename)
    return render_template("photo.html", str=str)


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [validators.Required(
    ), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.form == 'POST' and form.validate():
        return render_template('home.html')
    return render_template('home.html', form=form)

# @app.route('/twod', methods=['GET','POST'])
# def model():
@app.route('/results')
def routes():
    return render_template('products.html')

@app.route('/twodmodel')
def twodmodel():
    with open("/opt/lampp/htdocs/hack/tmp.txt",'r') as f:
        line = f.readline()
        line = line[1:]
        line = line[:-1]
        list_pts = line.split(',')
        points = list()
        for pt in list_pts:
            pt= pt.replace('[','')
            pt = pt.replace(']','')
            points.append(int(pt))

    ptuple = list()
    k = 0
    for i in range(0,4):
        ptuple.append((points[k],points[k+1]))
        k+= 2
    get2dfit('/home/dishant/Desktop/Assignments/Hackathon/templates/t1.png',"/home/dishant/Desktop/Assignments/Hackathon/static/uploads/exp1.jpg",ptuple[0],ptuple[1],ptuple[2],ptuple[3])
    # print (ptuple)
    return render_template('image.html')

@app.route('/modeld')
def outes():
    return render_template('model3D.html')

@app.route('/modeld1')
def kjhjk():
    return render_template('model3D1.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug='true')
