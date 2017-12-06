# coding=utf-8
from django.test import TestCase
from hamcrest import equal_to, assert_that

from examinations.models import *
from questions_factory.models import SimpleInterestProblem, ProblemGenerator


class SolutionsTests(TestCase):
    def test_time_placed_year_rate_year(self):
        problem = create_problem("year", "year")
        self.assertTrue(problem.get_sol() == problem.round(problem.amount * problem.time * problem.rate))

    def test_time_placed_month_rate_month(self):
        problem = create_problem("month", "month")
        self.assertTrue(problem.get_sol() == problem.round(problem.amount * problem.time * problem.rate))

    def test_time_placed_month_rate_year(self):
        problem = create_problem("month", "year")
        self.assertTrue(problem.get_sol() == problem.round(problem.amount * (problem.time / 12.0) * problem.rate))

    def test_time_placed_year_rate_month(self):
        problem = create_problem("year", "month")
        self.assertTrue(problem.get_sol() == problem.round(problem.amount * problem.time * 12.0 * problem.rate))


class GeneratingQuestionsTests(TestCase):

    def setUp(self):
        from test.factories.skill import SkillFactory
        from test.factories.skill import SectionFactory
        SectionFactory.create(id=28, name="UAA5: Deuxième degré").save()
        SkillFactory.create(id=342, code="T4-U5-A1b",
                            name="", description="",
                            image="area-chart", oscar_synthese=None, modified_by_id=None, section_id=28)

    def test_time_placed_year_rate_year(self):
        problem = create_problem("year", "year")
        questions = problem.gen_questions(5)
        self.assertTrue(isinstance(problem.get_context(), Context))
        for question in questions:
            self.assertTrue(isinstance(question, Question))
            self.assertTrue(question.description is not None)

    def test_time_placed_month_rate_month(self):
        problem = create_problem("month", "month")
        questions = problem.gen_questions(5)
        self.assertTrue(isinstance(problem.get_context(), Context))
        for question in questions:
            self.assertTrue(isinstance(question, Question))
            self.assertTrue(question.description is not None)

    def test_time_placed_month_rate_year(self):
        problem = create_problem("month", "year")
        questions = problem.gen_questions(5)
        self.assertTrue(isinstance(problem.get_context(), Context))
        for question in questions:
            self.assertTrue(isinstance(question, Question))
            self.assertTrue(question.description is not None)

    def test_time_placed_year_rate_month(self):
        problem = create_problem("year", "month")
        questions = problem.gen_questions(5)
        self.assertTrue(isinstance(problem.get_context(), Context))
        for question in questions:
            self.assertTrue(isinstance(question, Question))
            self.assertTrue(question.description is not None)


class InstanceTests(TestCase):
    def test_of_instantiation_via_generator(self):
        problem = create_problem()
        self.assertTrue(isinstance(problem, SimpleInterestProblem))

    def test_of_raw_instantiation(self):
        problem = SimpleInterestProblem("year", "year")
        self.assertTrue(isinstance(problem, SimpleInterestProblem))

    def test_of_instantiation_with_wrong_values(self):
        with self.assertRaises(ValueError):
            SimpleInterestProblem("wrong", "year")
        with self.assertRaises(ValueError):
            SimpleInterestProblem("year", "wrong")
        with self.assertRaises(ValueError):
            SimpleInterestProblem("month", "wrong")
        with self.assertRaises(ValueError):
            SimpleInterestProblem("wrong", "month")
        with self.assertRaises(ValueError):
            SimpleInterestProblem("wrong", "wrong")

# Utils


def create_problem(time_placed="year", type_rate="year"):
    values = new_interest_values()
    values["generator_name"] = "SimpleInterestProblem"
    values["time_placed"] = time_placed
    values["type_rate"] = type_rate
    values["nb_decimal"] = "3"
    problem = ProblemGenerator.factory(values)
    return problem


def new_interest_values():
    return {"problem": "Simple_Interest_Problem"}
