from fractions import Fraction

from django.test import TestCase
import numpy
from hamcrest import *

from questions_factory.models import ArithmeticPolynomialSecondDegree
from questions_factory.models.problem_generator import ProblemGenerator


class NormalBehaviour(TestCase):
    @staticmethod
    def test_get_solution_integer_rational_problem():
        val = [1, -3, 2]
        problem = create_problem("Integer", "Rational", [0, 20], val)
        [x_1, _] = problem.get_sol()
        assert_that(x_1, equal_to("1,2"))

    @staticmethod
    def test_get_solution_integer_integer_problem():
        val = [1, -3, 2]
        problem = create_problem("Integer", "Integer", [0, 10], val)
        [x_1, _] = problem.get_sol()
        assert_that(x_1, equal_to("1,2"))

    @staticmethod
    def test_get_val_integer_rational_problem():
        val = [1, -3, 2]
        problem = create_problem("Integer", "Rational", [0, 20], val)
        assert_that([1, -3, 2], equal_to(problem.get_val()))

    @staticmethod
    def test_get_solution_with_rational_range():
        problem = create_problem("Rational", "Rational", [1, 1, 20])
        assert_that([[]], contains(problem.get_sol()))

    @staticmethod
    def test_get_value_with_integer_solution():
        problem = create_problem("Rational", "Integer")
        assert_that(problem.get_val(), only_contains(instance_of(int)))


class ComplexImageProblems(TestCase):
    @staticmethod
    def test_get_solution_random_val_integer_complex_problem():
        problem = create_problem("Integer", "Complex", [0, 20])
        val = problem.get_val()
        ans = numpy.roots(val).tolist()
        ans = round(ans)
        assert_that(problem.get_sol(), has_item(str(ans[0]) + ',' + str(ans[1])))

    @staticmethod
    def test_get_solution_random_val_rational_complex_problem():
        problem = create_problem("Rational", "Complex", [0, 20])
        val = problem.get_val()
        ans = numpy.roots(val)
        ans = round(ans)
        assert_that(problem.get_sol(), has_item(str(ans[0]) + ',' + str(ans[1])))

    @staticmethod
    def test_high_number_solutions_rational_complex_problem():
        for i in range(0, 100):
            problem = create_problem("Rational", "Complex", [0, 20])
            val = problem.get_val()
            ans = numpy.roots(val)
            ans = round(ans)
            assert_that(problem.get_sol(), has_item(str(ans[0]) + ',' + str(ans[1])))

    @staticmethod
    def test_high_number_solutions_integer_complex_problem():
        for i in range(0, 100):
            problem = create_problem("Integer", "Complex", [0, 20])
            val = problem.get_val()
            ans = numpy.roots(val)
            ans = round(ans)
            assert_that(problem.get_sol(), has_item(str(ans[0]) + ',' + str(ans[1])))


class UnexpectedBehaviour(TestCase):
    def test_wrong_domain_value_raise_error(self):
        with self.assertRaises(ValueError):
            create_problem("Wrong_val", "Rational")

    def test_wrong_image_value_raise_error(self):
        with self.assertRaises(ValueError):
            problem = create_problem("Integer", "Wrong val")
            problem.get_sol()


class ComputeSol(TestCase):
    def test_negative_rho_with_integer_domain(self):
        problem = create_problem("Integer", "Complex", [0, 20])
        problem.val[0] = 2
        problem.val[1] = 0
        problem.val[2] = 4
        assert_that(problem.compute_sol() is None)

    def test_negative_rho_with_rational_domain(self):
        problem = create_problem("Rational", "Complex", [0, 20])
        problem.val[0] = 2
        problem.val[1] = 0
        problem.val[2] = 4
        assert_that(problem.compute_sol() is None)

    def test_fraction_sol(self):
        problem = create_problem("Integer", "Rational", [-20, 20], [-4, 8, -3])
        assert_that(problem.compute_sol(), equal_to(['\\frac{3}{2},\\frac{1}{2}', '\\frac{1}{2},\\frac{3}{2}']))


class ProblemSettings(TestCase):
    def test_get_problem_description(self):
        val = [1, -3, 2]
        problem = create_problem("Integer", "Rational", [0, 20], val)
        assert_that("Polynomial second degree", equal_to(problem.get_desc()))


# Sub Methods Test
class AnsWithFracTests(TestCase):
    def test_simplify_fract_false(self):
        result = ArithmeticPolynomialSecondDegree.ans_with_frac(2, 1, False)
        assert_that(r"\frac{2}{1}" == result)

    def test_simplify_fract_true(self):
        result = ArithmeticPolynomialSecondDegree.ans_with_frac(2, 1, True)
        f = Fraction(2, 1)
        assert_that(str(f.numerator) == result)

    def test_simplify_root_false(self):
        val = [1, -1, -2]
        problem = create_problem("Integer", "Rational", [0, 20], val)
        result = problem.ans_with_root(9, "+", 1, -1, -2, False)
        assert_that(result, equal_to(r"\frac{1+\sqrt{9}}{2}"))

    def test_simplify_root_true_1(self):
        val = [-1, -3, 3]
        problem = create_problem("Integer", "Rational", [0, 20], val)
        result = problem.ans_with_root(21, "+", -1, -3, 3, True)
        assert_that(result, equal_to(r"\frac{-3-\sqrt{21}}{2}"))

    def test_simplify_root_true_2(self):
        val = [2, 39, 12]
        problem = create_problem("Integer", "Rational", [0, 20], val)
        result = problem.ans_with_root(problem.rho(2, 39, 12), "-", 2, 39, 12, True)
        assert_that(result, equal_to(r"\frac{-39-5\sqrt{57}}{4}"))

    def test_reduced_sqrt(self):
        result = ArithmeticPolynomialSecondDegree.reduced_sqrt(28)
        assert_that(result, equal_to((2, 7)))
        result = ArithmeticPolynomialSecondDegree.reduced_sqrt(10)
        assert_that(result, equal_to((1, 10)))

    def test_common_divisor(self):
        result = ArithmeticPolynomialSecondDegree.common_divisor(4, 6, 2)
        assert_that(result, equal_to((2, 3, 1)))
        result = ArithmeticPolynomialSecondDegree.common_divisor(5, 7, 2)
        assert_that(result, equal_to((5, 7, 2)))
        result = ArithmeticPolynomialSecondDegree.common_divisor(2, 2, 6)
        assert_that(result, equal_to((1, 1, 3)))
        result = ArithmeticPolynomialSecondDegree.common_divisor(10, 2, -12)
        assert_that(result, equal_to((5, 1, -6)))

    def test_den_not_one(self):
        ans = ArithmeticPolynomialSecondDegree.ans_with_frac(4, 5, True)
        assert_that(ans, equal_to(r'\frac{4}{5}'))


class SpecificCasesTests(TestCase):
    def test_last_option_compute_sol(self):
        val = [Fraction(4, 2), Fraction(5, 2), Fraction(4, 3)]
        problem = create_problem("Rational", "Rational", [0, 20], val)
        problem.compute_sol()
        assert_that(True)

    def test_numneg_modulo_debominator_compute_sol(self):
        val = [Fraction(-4, 2), Fraction(5, 2), Fraction(4, 3)]
        problem = create_problem("Rational", "Rational", [0, 20], val)
        problem.compute_sol()
        assert_that(True)


# Utils


def new_arithmetic_dict():
    dict = {"problem": "Arithmetic_Polynomial_Second_degree", "desc": "blabla"}
    return dict


def create_problem(domain="Integer", image="Rational", range=[0, 20], val=None):
    dict = new_arithmetic_dict()
    dict["generator_name"] = "ArithmeticProblem"
    dict["domain"] = domain
    dict["image"] = image
    dict['range_from'] = range[0]
    dict['range_to'] = range[1]
    if val:
        dict["val"] = val
    dict["nb_decimal"] = "3"
    problem = ProblemGenerator.factory(dict)
    return problem


def round(list):
    new_list = []
    for x in list:
        if isinstance(x, complex):
            new_list.append(complex("{0:.2f}".format(x)))
        elif isinstance(x, float):
            new_list.append(float("{0:.2f}".format(x)))
    return new_list
