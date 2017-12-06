# coding=utf-8
from django.test import TestCase
from examinations.models import *
from questions_factory.models import AreaProblem, ProblemGenerator
import math


class SolutionsTests(TestCase):
    def test_square(self):
        problem = create_problem("square")
        self.assertTrue(problem.get_sol() == problem.round(problem.figure[0][1] * problem.figure[0][1]))

    def test_quadrilateral(self):
        problem = create_problem("quadrilateral")
        self.assertTrue(problem.get_sol() == problem.round(
                        0.5 * problem.figure[0][1] * problem.figure[3][1] * math.sin(math.radians(problem.figure[4][1])) +
                        0.5 * problem.figure[1][1] * problem.figure[2][1] * math.sin(math.radians(problem.figure[5][1]))))

    def test_triangle(self):
        problem = create_problem("triangle")
        self.assertTrue(problem.get_sol() == problem.round(float(problem.figure[0][1]) * problem.figure[1][1] / 2))

    def test_circle(self):
        problem = create_problem("circle")
        self.assertTrue(problem.get_sol() == problem.round(math.pow(problem.figure[0][1], 2)*math.pi))

    def test_rectangle(self):
        problem = create_problem("rectangle")
        self.assertTrue(problem.get_sol() == problem.round(problem.figure[0][1] * problem.figure[1][1]))

    def test_rhombus(self):
        problem = create_problem("rhombus")
        self.assertTrue(problem.get_sol() == problem.round(2 * math.sqrt(math.pow(problem.figure[0][1], 2) + math.pow(problem.figure[1][1], 2))))

    def test_trapezium(self):
        problem = create_problem("trapezium")
        self.assertTrue(problem.get_sol() == problem.round((problem.figure[0][1]+problem.figure[1][1]) * problem.figure[2][1] / 2))

    def test_parallelogram(self):
        problem = create_problem("parallelogram")
        self.assertTrue(problem.get_sol() == problem.round(problem.figure[0][1] * problem.figure[1][1]))

    def test_polygon(self):
        for i in range(0,100):
            problem = create_problem("regular_polygon")
            self.assertTrue(problem.get_sol() == problem.round(problem.figure[0][1] * (math.pow(problem.figure[1][1], 2)) / (4 * math.tan(math.pi / problem.figure[0][1]))))


class GeneratingQuestionsTests(TestCase):

    def setUp(self):
        from test.factories.skill import SkillFactory
        from test.factories.skill import SectionFactory
        SectionFactory.create(id=28, name="UAA5: Deuxième degré").save()
        SkillFactory.create(id=342, code="T4-U5-A1b",
                            name="", description="",
                            image="area-chart", oscar_synthese=None, modified_by_id=None, section_id=28)

    def test_square(self):
        problem = create_problem("square")
        questions = problem.gen_questions(5)
        self.assertTrue(isinstance(problem.get_context(), Context))
        for question in questions:
            self.assertTrue(isinstance(question, Question))
            self.assertTrue(question.description is not None)

    def test_quadrilateral(self):
        problem = create_problem("quadrilateral")
        questions = problem.gen_questions(5)
        self.assertTrue(isinstance(problem.get_context(), Context))
        for question in questions:
            self.assertTrue(isinstance(question, Question))
            self.assertTrue(question.description is not None)

    def test_triangle(self):
        problem = create_problem("triangle")
        questions = problem.gen_questions(5)
        self.assertTrue(isinstance(problem.get_context(), Context))
        for question in questions:
            self.assertTrue(isinstance(question, Question))
            self.assertTrue(question.description is not None)

    def test_circle(self):
        problem = create_problem("circle")
        questions = problem.gen_questions(5)
        self.assertTrue(isinstance(problem.get_context(), Context))
        for question in questions:
            self.assertTrue(isinstance(question, Question))
            self.assertTrue(question.description is not None)

    def test_rectangle(self):
        problem = create_problem("rectangle")
        questions = problem.gen_questions(5)
        self.assertTrue(isinstance(problem.get_context(), Context))
        for question in questions:
            self.assertTrue(isinstance(question, Question))
            self.assertTrue(question.description is not None)

    def test_rhombus(self):
        problem = create_problem("rhombus")
        questions = problem.gen_questions(5)
        self.assertTrue(isinstance(problem.get_context(), Context))
        for question in questions:
            self.assertTrue(isinstance(question, Question))
            self.assertTrue(question.description is not None)

    def test_trapezium(self):
        problem = create_problem("trapezium")
        questions = problem.gen_questions(5)
        self.assertTrue(isinstance(problem.get_context(), Context))
        for question in questions:
            self.assertTrue(isinstance(question, Question))
            self.assertTrue(question.description is not None)

    def test_parallelogram(self):
        problem = create_problem("parallelogram")
        questions = problem.gen_questions(5)
        self.assertTrue(isinstance(problem.get_context(), Context))
        for question in questions:
            self.assertTrue(isinstance(question, Question))
            self.assertTrue(question.description is not None)

    def test_polygon(self):
        problem = create_problem("regular_polygon")
        questions = problem.gen_questions(5)
        self.assertTrue(isinstance(problem.get_context(), Context))
        for question in questions:
            self.assertTrue(isinstance(question, Question))
            self.assertTrue(question.description is not None)

    def test_unrecognized_type(self):
        problem = create_problem("regular_polygon")
        problem.object_type = "fizz"
        with self.assertRaises(ValueError):
            problem.get_sol()
        with self.assertRaises(ValueError):
            problem.gen_values()


class InstanceTests(TestCase):
    def test_of_instantiation_via_generator(self):
        problem = create_problem()
        self.assertTrue(isinstance(problem, AreaProblem))

    def test_of_raw_instantiation(self):
        problem = AreaProblem("square", 1, 2, 2)
        self.assertTrue(isinstance(problem, AreaProblem))

    def test_of_instantiation_with_wrong_values(self):
        with self.assertRaises(ValueError):
            AreaProblem("wrong", 1, 2, 3)


class MethodTests(TestCase):
    def test_get_description(self):
        problem = create_problem()
        result = problem.get_desc()
        self.assertTrue(result is None)


# Utils


def create_problem(object_type="square", range_from=1, range_to=10):
    values = new_area_values()
    values["generator_name"] = "AreaProblem"
    values["object_type"] = object_type
    values["range_from"] = range_from
    values["range_to"] = range_to
    values["nb_decimal"] = "3"
    problem = ProblemGenerator.factory(values)
    return problem


def new_area_values():
    return {"problem": "Area_Problem"}
