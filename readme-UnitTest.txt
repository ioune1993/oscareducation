How to tests with unit tests.

1. enter the command "bash makemigrations.sh" in oscar folder
2. enter the command "python manage.py test NameOfFolderModule/" in oscar folder

(For instance : python manage.py test student/ ) for the case of student.

Normally you obtain something like this :

Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..Not Found: /student/test/start/465
...Not Found: /test/21/start/
.
----------------------------------------------------------------------
Ran 6 tests in 0.927s

OK
Destroying test database for alias 'default'...


-----


It's normal that he didn't find because these pages can't be accessed.
