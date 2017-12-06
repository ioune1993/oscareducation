# coding=utf-8
from django.test import TestCase
from examinations.models import *
from questions_factory.models import PythagorasProblem, ProblemGenerator
import math


class ResultTest(TestCase):
    def test_pythagoras_result(self):
        problem = create_problem()
        self.assertTrue(problem.get_sol() == problem.round(math.sqrt(math.pow(problem.figure[0][1],2) + math.pow(problem.figure[1][1],2))))


class GeneratingQuestionsTests(TestCase):
    def setUp(self):
        from test.factories.skill import SkillFactory
        from test.factories.skill import SectionFactory
        SectionFactory.create(id=28, name="UAA5: Deuxième degré").save()
        SkillFactory.create(id=342, code="T4-U5-A1b",
                            name="", description="",
                            image="area-chart", oscar_synthese=None, modified_by_id=None, section_id=28)

    def test_pythagoras_generation(self):
        problem = create_problem()
        questions = problem.gen_questions(5)
        self.assertTrue(isinstance(problem.get_context(), Context))
        for question in questions:
            self.assertTrue(isinstance(question, Question))
            self.assertTrue(question.description is not None)


class InstanceTests(TestCase):
    def test_generator(self):
        problem = create_problem()
        self.assertTrue(isinstance(problem, PythagorasProblem))

    def test_raw_instance(self):
        problem = PythagorasProblem(4, 14)
        self.assertTrue(isinstance(problem, PythagorasProblem))

    def test_wrong_values_instanciation(self):
        with self.assertRaises(ValueError):
            PythagorasProblem("yolo", 3)


class ErrorTests(TestCase):
    def test_get_sol_with_wrong_object_type(self):
        problem = create_problem()
        problem.object_type = "Fizz"
        with self.assertRaises(ValueError):
            problem.get_sol()


class MethodTests(TestCase):
    def test_get_description(self):
        problem = create_problem()
        result = problem.get_desc()
        self.assertTrue(result is None)


def create_problem(range_from=1, range_to=20):
    values = {"problem": "PythagorasProblem"}
    values["generator_name"] = "PythagorasProblem"
    values["range_from"] = range_from
    values["range_to"] = range_to
    values["nb_decimal"] = "3"
    problem = ProblemGenerator.factory(values)
    return problem
