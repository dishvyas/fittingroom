from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, Response
import pymysql
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
import os
from model2d import get2dfit

app = Flask(__name__)

pymysql.install_as_MySQLdb()

UPLOAD_FOLDER = 'static/uploads/'  # Removed leading slash to make it relative to current directory
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}  # Use set literal for efficiency

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(24)  # Securely generate a secret key for session management

# MySQL configurations (Add your MySQL configurations here)
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'password'
# app.config['MYSQL_DB'] = 'mydatabase'


def allowed_file(filename):
    """
    Check if the file extension is allowed.

    Args:
        filename (str): The name of the file.

    Returns:
        bool: True if the file extension is allowed, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """
    Render the home page.

    Returns:
        str: Rendered HTML content for the home page.
    """
    return render_template('home.html')

@app.route("/login/", methods=['POST'])
def move_forward():
    """
    Handle the login form submission and redirect to the upload page.

    Returns:
        Response: Redirect to the upload page.
    """
    return redirect(url_for("upload"))

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('uploadphoto.html')
    
    if request.method == 'POST':
        file = request.files.get('file')

        if file is None or file.filename == '':
            flash('No file selected', 'danger')
            return redirect(url_for('upload'))

        if file and allowed_file(file.filename):
            filename = file.filename
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)

            get2dfit('templates/t1.png', save_path)

            fitted_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'fitted_result.jpg')

            flash('File successfully uploaded', 'success')
            return render_template("photo.html", image_path=fitted_image_path)

    flash('File upload failed', 'danger')
    return redirect(url_for('upload'))

class RegisterForm(Form):
    """
    User Registration Form.

    Attributes:
        name (StringField): The name of the user.
        username (StringField): The username of the user.
        email (StringField): The email address of the user.
        password (PasswordField): The password for the user.
        confirm (PasswordField): Field to confirm the password.
    """
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration.

    Returns:
        str: Rendered HTML content for the registration page.
    """
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        # Insert registration logic here (e.g., saving to the database)
        flash('Registration successful!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/results')
def results():
    """
    Render the results page.

    Returns:
        str: Rendered HTML content for the results page.
    """
    return render_template('products.html')

@app.route('/twodmodel')
def twodmodel():
    """
    Render the 2D model results.

    Returns:
        str: Rendered HTML content for the 2D model image page.
    """
    try:
        with open("/opt/lampp/htdocs/hack/tmp.txt", 'r') as f:
            line = f.readline().strip()[1:-1]
            points = [int(pt) for pt in line.split(',')]
        
        ptuple = [(points[i], points[i+1]) for i in range(0, len(points), 2)]

        get2dfit('templates/t1.png', "static/uploads/exp1.jpg", *ptuple)
        return render_template('image.html')

    except Exception as e:
        logging.error(f"Error in twodmodel: {str(e)}")
        flash('An error occurred while processing the 2D model.', 'danger')
        return redirect(url_for('index'))

@app.route('/modeld')
def model_3d():
    """
    Render the 3D model page.

    Returns:
        str: Rendered HTML content for the 3D model page.
    """
    return render_template('model3D.html')

@app.route('/modeld1')
def model_3d_alternate():
    """
    Render an alternate 3D model page.

    Returns:
        str: Rendered HTML content for the alternate 3D model page.
    """
    return render_template('model3D1.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)