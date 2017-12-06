# coding=utf-8
from django.test import TestCase
from examinations.models import *
from questions_factory.models import VolumeProblem, ProblemGenerator
import math


class SolutionsTests(TestCase):
    def test_cube(self):
        problem = create_problem("cube")
        self.assertTrue(problem.get_sol() == problem.round(pow(problem.figure[0][1], 3)))

    def test_cylinder(self):
        problem = create_problem("cylinder")
        self.assertTrue(problem.get_sol() == problem.round(math.pi * pow(problem.figure[0][1], 2) * problem.figure[1][1]))

    def test_prism(self):
        problem = create_problem("prism")
        self.assertTrue(problem.get_sol() == problem.round(0.5 * problem.figure[0][1] * problem.figure[1][1] * problem.figure[2][1]))

    def test_cone(self):
        problem = create_problem("cone")
        self.assertTrue(problem.get_sol() == problem.round(math.pi * pow(problem.figure[0][1], 2) * (problem.figure[1][1] / 3)))

    def test_pyramid(self):
        problem = create_problem("pyramid")
        self.assertTrue(problem.get_sol() == problem.round((problem.figure[0][1] * problem.figure[1][1] * problem.figure[2][1]) / 3))


class GeneratingQuestionsTests(TestCase):

    def setUp(self):
        from test.factories.skill import SkillFactory
        from test.factories.skill import SectionFactory
        SectionFactory.create(id=28, name="UAA5: Deuxième degré").save()
        SkillFactory.create(id=342, code="T4-U5-A1b",
                            name="", description="",
                            image="area-chart", oscar_synthese=None, modified_by_id=None, section_id=28)

    def test_cube(self):
        problem = create_problem("cube")
        questions = problem.gen_questions(5)
        self.assertTrue(isinstance(problem.get_context(), Context))
        for question in questions:
            self.assertTrue(isinstance(question, Question))
            self.assertTrue(question.description is not None)

    def test_prism(self):
        problem = create_problem("prism")
        questions = problem.gen_questions(5)
        self.assertTrue(isinstance(problem.get_context(), Context))
        for question in questions:
            self.assertTrue(isinstance(question, Question))
            self.assertTrue(question.description is not None)

    def test_pyramid(self):
        problem = create_problem("pyramid")
        questions = problem.gen_questions(5)
        self.assertTrue(isinstance(problem.get_context(), Context))
        for question in questions:
            self.assertTrue(isinstance(question, Question))
            self.assertTrue(question.description is not None)

    def test_cone(self):
        problem = create_problem("cone")
        questions = problem.gen_questions(5)
        self.assertTrue(isinstance(problem.get_context(), Context))
        for question in questions:
            self.assertTrue(isinstance(question, Question))
            self.assertTrue(question.description is not None)

    def test_cylinder(self):
        problem = create_problem("cylinder")
        questions = problem.gen_questions(5)
        self.assertTrue(isinstance(problem.get_context(), Context))
        for question in questions:
            self.assertTrue(isinstance(question, Question))
            self.assertTrue(question.description is not None)


class InstanceTests(TestCase):
    def test_of_instantiation_via_generator(self):
        problem = create_problem()
        self.assertTrue(isinstance(problem, VolumeProblem))

    def test_of_raw_instantiation(self):
        problem = VolumeProblem("cube", 1, 2, 3)
        self.assertTrue(isinstance(problem, VolumeProblem))

    def test_of_instantiation_with_wrong_values(self):
        with self.assertRaises(ValueError):
            VolumeProblem("wrong", 1, 2, -9)


class BadValuesTests(TestCase):
    def test_wrong_type_object(self):
        problem = VolumeProblem("cube", 1, 2, 3)
        problem.object_type = "kek"
        with self.assertRaises(ValueError):
            problem.get_sol()
        with self.assertRaises(ValueError):
            problem.gen_values()

# Utils


def create_problem(object_type="cube", range_from=1, range_to=10):
    values = new_volume_values()
    values["generator_name"] = "VolumeProblem"
    values["object_type"] = object_type
    values["range_from"] = range_from
    values["range_to"] = range_to
    values["nb_decimal"] = "3"
    problem = ProblemGenerator.factory(values)
    return problem


def new_volume_values():
    return {"problem": "Volume_Problem"}
