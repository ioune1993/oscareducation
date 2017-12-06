import abc


class Problem(object):
    def __init__(self, nb_decimal=2):
        self.nb_decimal = int(nb_decimal)
        pass

    def round(self, number):
        return round(number, self.nb_decimal)

    @abc.abstractmethod
    def get_sol(self):
        """Return the solution of the problem"""

    @abc.abstractmethod
    def gen_values(self):
        """Generate new random values for the problem"""

    @abc.abstractmethod
    def gen_questions(self, number_of_questions):
        """Generate questions for use in context"""

    @abc.abstractmethod
    def make_form(self):
        """Generate the associated form"""
