import string
import random

from django.contrib.auth.decorators import user_passes_test


def generate_random_password(size):
    return ''.join(random.SystemRandom().choice(string.hexdigits) for n in xrange(size))


def user_is_professor(function):
    return user_passes_test(lambda x: hasattr(x, "professor"))(function)


def force_encoding(string):
    try:
        return string.encode("Utf-8")
    except UnicodeDecodeError:
        pass

    try:
        return string.decode("Utf-8")
    except UnicodeDecodeError:
        pass

    try:
        return string.encode("latin")
    except UnicodeDecodeError:
        pass

    return string.decode("latin")
