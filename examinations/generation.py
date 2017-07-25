import re
import random

VARIABLES_REGEX = r"{ *([a-zA-Z-_]+) *}"


class PositiveIntegerVariable(object):
    def __init__(self):
        self.value = None

    def _generate_value(self):
        self.value = random.randint(1, 10)

    def get_value(self):
        if self.value is None:
            self._generate_value()

        return self.value


def needs_to_be_generated(exercice_body):

    if exercice_body is None:
        return False
    return bool(re.search(VARIABLES_REGEX, exercice_body))


def get_variable_list(exercice_body):
    return {x.lower(): PositiveIntegerVariable().get_value() for x in re.findall(VARIABLES_REGEX, exercice_body)}


def render(exercice_body, variables):
    if not needs_to_be_generated(exercice_body):
        return exercice_body

    for variable, value in variables.items():
        exercice_body = re.sub(r"{ *%s *}" % variable, str(value), exercice_body, flags=re.IGNORECASE)

    return exercice_body
