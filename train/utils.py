from django.contrib.auth.decorators import user_passes_test


def user_is_student(function):
    return user_passes_test(lambda x: hasattr(x, "student"))(function)

def user_is_professor(function):
    return user_passes_test(lambda x: hasattr(x, "professor"))(function)
