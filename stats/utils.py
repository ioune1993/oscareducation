from django.contrib.auth.decorators import user_passes_test


def user_is_superuser(function):
    return user_passes_test(lambda x: x.is_superuser)(function)
