from django.test import TestCase
from questions_factory.models import *
import json
from questions_factory.models.problem_generator import ProblemGenerator


class NormalBehaviour(TestCase):
    def test_problem_generator_creation_succeed(self):
        gen = ProblemGenerator()
        self.assertTrue(isinstance(gen, ProblemGenerator))


class UnexpectedBehaviour(TestCase):
    def test_problem_raises_value_error(self):
        with self.assertRaises(ValueError) as context:
            problem_set = problem_settings("foo", "bar", "Interrzger", "Ratdqdional", [9687, 20], None)
            ProblemGenerator.factory(problem_set)
        self.assertTrue('Wrong problem type' in context.exception)


def problem_settings(problem, problem_description, domain, image, range, val):
    settings = {
        "generator_name": problem,
        "desc": problem_description,
        "domain": domain,
        "image": image,
        "range": range,
        "val": val,
        "nb_decimal": "3"
    }
    return settings
