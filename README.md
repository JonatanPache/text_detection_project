# TEXT DETECTION PROJECT

Es un proyecto para la deteccion de placas vehiculares.


Version Python 3.10.14


# First Steps

Creation an Virtual Env

`virtualenv -p /usr/bin/python3.10 venv`

Activation
`source venv/bin/activate`


Install this packages

pip install django==5.0.6
pip install easyocr==1.6.2
pip install matplotlib==3.7.1
pip install opencv-python-headless==4.5.4.60
pip install numpy==1.24.2

Or install by requirements.txt and run `pip install -r requirements.txt`

Check all your installed packages `pip freeze`
 python manage.py migrate
 python manage.py runserver

 python manage.py startapp core


 agregamos la ruta para core en urls.py
 eliminamos model.py y creamos una carpeta para models

 cramos en utils una clase para cada vez que creamos un model
 una vez creado el model correr el siguiente comando 
ython manage.py makemigrations
