import re

VARIABLES_REGEX = r"{ *([a-zA-Z-_]+) *}"


def needs_to_be_generated(exercice_body):
    return bool(re.search(VARIABLES_REGEX, exercice_body))


def get_variable_list(exercice_body):
    return {x: None for x in re.findall(VARIABLES_REGEX, exercice_body)}
