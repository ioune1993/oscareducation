# Development environment

## Installation

### Database
First, install PostgreSQL version 9.4 or above
(installation instructions depends on your OS).
Then we advise you to install a tool such as
`pgAdmin` to administrate the database, `DbVisualizer`
visualize the database schema and
`PyCharm Community Edition` a python IDE. By default,
as it is stated in `oscar/settings.py`, the database
name is 'oscar', accessible from `localhost:5432`, with
the user 'oscar' and the password 'oscar'. So, create a
PostgreSQL server with a database, with the parameters 
you chose or the default parameters stated above if you 
do not intend to change the `oscar/settings.py`.

### Django
You only need to perform these commands once:
Install `virtualenv`, clone the repository, and
create a new virtual environment in it. Python
will be used in version 2.7. `ve` is the folder
where the virtual environment will be stored
```sh
$ apt-get install python-virtualenv
$ git clone https://github.com/ioune1993/oscareducation.git
$ cd oscareducation
$ virtualenv --python=/usr/bin/python2.7 ve
```

Then, enter in the virtual environment, and install
all the requirements
```sh
$ source ve/bin/activate
$ pip install -r requirements-oscar2.txt
```
Then adding fields into your database
```sh
$ python manage.py makemigrations
$ python manage.py migrate
```
If the second command does not create the fields, and report 
that there are missing relations, use the `makemigrations.sh` 
script to make the migrations for each app one by one (and then 
do the second command). This is unfortunate, but this a known 
bug in Django that can happen.

Then optionally with `pgAdmin` 
import the SQL data file 'oscar-data.sql' to obtain a sample 
of data in order to test the website.

Finally create a superuser account
```sh
$ python manage.py createsuperuser
```
and follow the steps

Once all the steps above done, run the server with:
```sh    
$ python manage.py runserver
```

You can now access the website: `http://127.0.0.1:8000`.

The administration is on `http://127.0.0.1:8000/admin`. You can
create a new "Professor" (green +) (and later, Students the same way), there, click on "green +" again to start a 
popup in which you'll create a new user (for example "prof" with password "prof"),
validate, select field is auto field, validate, you now have a prof user.
Then, edit this professor by providing him/her an email address (because
you need to confirm his/her email, you can use a temporary address in your tests).
Log out and go back on "/" to log.

Now, whenever you want to run the website again, you
only need to enter in you virtual environment and run
the Django server:
```sh
$ source ve/bin/activate
$ python manage.py runserver
```

## Documentation
To consult the Oscar documentation, open the
`documentation/build/html/index.html` file.

In order to generate the documentation, the `sphinx`
is used with .rst files. Examples of code documentation
can be found in `doc-example.py`. These conventions must
be respected to allow the proper documentation generation.

To generate the HTML documentation, run this command being in
the `documentation` folder:
```sh
$ make html
```

When you add code files to the project, they must be added to
the modules described in the .rst files, located in the
`documentation/source` folder.

The `conf.py` file in the `documentation/source` contains the
configuration for the `sphinx` tool.
