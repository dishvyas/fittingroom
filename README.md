Virtual Fitting Room
=======================

Overview
--------

The Virtual Fitting Room is a web application that allows users to try on clothing items virtually by overlaying 2D images of garments onto an image of the user. The application is built using Flask for the backend and uses OpenCV for image processing. The front-end is powered by HTML, CSS, and JavaScript, while Django manages user authentication and other functionalities.

Features
--------

-   User Authentication: Secure registration and login system managed by Django.
-   2D Garment Fitting: Upload a photo and try on clothing items virtually.
-   Image Processing: Real-time image processing using OpenCV to adjust the garment's position and size based on the user's image.
-   Responsive Design: The application is designed to work across various devices and screen sizes.

Tech Stack
----------

-   Backend: Flask, Django, Python
-   Frontend: HTML, CSS, JavaScript
-   Image Processing: OpenCV
-   Database: MySQL (or any other database supported by Django)

Setup and Installation
----------------------

### 1\. Clone the Repository
```bash
git clone https://github.com/dishvyas/fittingroom.git
cd fitting-room
```

### 2\. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  
# On Windows use `venv\Scripts\activate`
```

### 3\. Install Dependancies
```bash
pip install -r requirements.txt
```

### 4/. Configure the Database
Set up your database (e.g., MySQL) and update the database configuration in the Django settings.
```arduino
# settings.py

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.mysql',

        'NAME': 'your_db_name',

        'USER': 'your_db_user',

        'PASSWORD': 'your_db_password',

        'HOST': 'localhost',

        'PORT': '3306',

    }

}
```

### 5\. Apply Migrations
If you're using Django's ORM, apply the migrations to create the necessary database tables.
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6\. Run the Application
```bash
python manage.py runserver
```
The application will start on http://127.0.0.1:8000/.

Usage
-----

1.  Register and Log In: Create an account and log in.
2.  Upload Image: Upload a photo of yourself to the application.
3.  Virtual Fitting: Select a garment to try on, and the application will overlay it onto your uploaded image.
4.  View Results: See how the clothing item looks on you with options to download or share the fitted image.

File Structure
--------------
```plaintext
.

├── app.py                     # Flask application file

├── model2d.py                 # Handles 2D model fitting logic

├── fittingroom/               # Django app for user management and authentication

│   ├── __init__.py

│   ├── settings.py            # Django settings

│   ├── urls.py                # URL routing for Django app

│   ├── views.py               # Views for handling HTTP requests

│   ├── templates/             # HTML templates

│   ├── static/                # Static files (CSS, JS, images)

│   ├── migrations/            # Database migrations

│   ├── forms.py               # Django forms for user creation and login

├── requirements.txt           # Python dependencies

├── README.md                  # This README file

└── ...
```

Future Enhancements
-------------------

-   3D Virtual Fitting: Extend the functionality to allow for 3D virtual fitting using advanced image processing techniques.
-   Improved Image Processing: Enhance the image processing algorithms to support more complex garments and better fit accuracy.
-   User History: Implement a feature to save and view past fittings.
-   Social Sharing: Add options to share the fitted images on social media platforms.

Contributing
------------

Contributions are welcome! Please fork this repository, make your changes, and submit a pull request.

License
-------

This project is licensed under the MIT License - see the LICENSE file for details.
