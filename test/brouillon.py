"""#import factory
import sys

from django.test import Client
from django.conf import settings

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oscar.settings")
django.setup()



from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from users.models import Professor
from users.models import Student


settings.configure()"""