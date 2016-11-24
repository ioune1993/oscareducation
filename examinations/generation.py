import re
import random

VARIABLES_REGEX = r"{ *([a-zA-Z-_]+) *}"


class PositiveIntegerVariable(object):
    def __init__(self):
        self.value = None

    def _generate_value(self):
        self.value = random.randint(1, 10)

    def __eq__(self, a):
        # XXX meh
        if isinstance(a, self.__class__):
            return True

        return False

    def get_value(self):
        if self.value is None:
            self._generate_value()

        return self.value


def needs_to_be_generated(exercice_body):
    return bool(re.search(VARIABLES_REGEX, exercice_body))


def get_variable_list(exercice_body):
    return {x: PositiveIntegerVariable() for x in re.findall(VARIABLES_REGEX, exercice_body)}


def replace_variables(exercice_body, variables):
    for variable, value in variables.items():
        exercice_body = re.sub(r"{ *%s *}" % variable, str(value.get_value()), exercice_body)

    return exercice_body


def render(exercice_body):
    if not needs_to_be_generated(exercice_body):
        return exercice_body

    variables = get_variable_list(exercice_body)

    return replace_variables(exercice_body, variables)
