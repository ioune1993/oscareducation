import re


def needs_to_be_generated(exercice_body):
    return bool(re.search(r"{ *[a-zA-Z-_] *}", exercice_body))
