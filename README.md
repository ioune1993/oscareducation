# Development environment

    apt-get install python-virtualenv

    git clone https://github.com/psycojoker/oscar
    cd oscar
    virtualenv ve
    source ve/bin/activate
    pip install -r requirements-frozen.txt
    python manage.py makemigrations
    python manage.py migrate
    # you need a csv for skills
    python manage.py import_skills file.csv
    python manange.py load_exercices

    python manage.py createsuperuser  # create an admin, it will be used to create the admin

    python manange.py runserver

Go to `http://127.0.0.1:8000/admin`, there create a "Prof" (green +), there,
click on "green +" again to start a popup in which you'll create a new user
(for example "prof" with password "prof"), validate, select field is auto
field, valide, you have a prof user, log out and go back on "/" to log.
