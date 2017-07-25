# Development environment

## Installation
You only need to perform these commands once: Install `virtualenv`,
clone the repository, and create a new virtual environment in it.
```sh
$ apt-get install python-virtualenv
$ git clone https://github.com/ioune1993/oscareducation.git
$ cd oscar
$ virtualenv ve
```

Then, enter in the virtual environment, and install all the requirements
```sh
$ source ve/bin/activate
$ pip install -r requirements-oscar2.txt
```

Once all the steps above done, run the server with:
```sh    
$ python manage.py runserver
```

You can now access the website: `http://127.0.0.1:8000`.

The administration is on `http://127.0.0.1:8000/admin`. You can
create a new "Prof" (green +), there, click on "green +" again to start a 
popup in which you'll create a new user (for example "prof" with password "prof"),
validate, select field is auto field, validate, you now have a prof user.
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
is used with .rst files. First install the tool (don't
forget to enter in the virtual environment first).
```sh
$ apt-get install sphinx
```
Examples of code documentation can be found in `doc-example.py`.
These conventions must be respected to allow the proper
documentation generation.

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