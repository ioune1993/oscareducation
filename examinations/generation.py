import re

VARIABLES_REGEX = r"{ *([a-zA-Z-_]+) *}"


class PositiveIntegerVariable(object):
    def __eq__(self, a):
        if isinstance(a, self.__class__):
            return True

        return False


def needs_to_be_generated(exercice_body):
    return bool(re.search(VARIABLES_REGEX, exercice_body))


def get_variable_list(exercice_body):
    return {x: PositiveIntegerVariable() for x in re.findall(VARIABLES_REGEX, exercice_body)}
