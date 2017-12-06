# coding=utf-8
import random
from collections import OrderedDict

from fractions import Fraction
import numpy
import math

from examinations.models import *
from questions_factory.models.problem_form import *
from questions_factory.models.problem_models.problem import *
from skills.models import Skill


class ArithmeticPolynomialSecondDegree(Problem):

    NAME = "ArithmeticProblem"

    def __init__(self, domain, image, range=(0, 20), val=None, nb_decimal=2):
        super(ArithmeticPolynomialSecondDegree, self).__init__(nb_decimal)
        self.desc = "Polynomial second degree"
        self.domain = domain
        self.image = image
        self.range = range
        if val and len(val) == 3:
            self.val = val
        else:
            self.gen_new_values()

    def gen_new_values(self):
        self.val = list()
        self.gen_values()

    def gen_values(self):
        if self.image == "Integer":
            self.gen_values_from_sol()
        elif self.domain == "Integer":
            for i in range(3):
                self.val.append(random.randint(self.range[0], self.range[1]))
        elif self.domain == "Rational":
            for i in range(3):
                num, den = random.randint(self.range[0], self.range[1]), random.randint(self.range[0], self.range[1])
                if den == 0:
                    den = 1
                self.val.append(Fraction(num, den))
        else:
            raise ValueError("Wrong value for domain: ", self.domain)
        if self.val[0] == 0:
            self.val[0] = 1

    def gen_values_from_sol(self):
        # Max_val for value is rng_range³
        # TODO What range should we put ?
        sol = [random.randint(-5, 5), random.randint(-5, 5)]
        sum, prod = sol[0] + sol[1], sol[0] * sol[1]
        # For polynom of type ax²+bx+c
        a = random.randint(-5, 5)
        b = -1 * sum * a
        c = prod * a
        self.val = [a, b, c]

    def get_desc(self):
        return self.desc

    def get_val(self):
        return self.val

    @staticmethod
    def round(list):
        new_list = []
        for x in list:
            if isinstance(x, complex):
                new_list.append(complex("{0:.2f}".format(x)))
            elif isinstance(x, float):
                new_list.append(float("{0:.2f}".format(x)))
        return new_list

    def get_sol(self):
        tmp_sol = numpy.roots(self.val).tolist()
        sol = ""
        if self.image == "Rational" or self.image == "Integer":
            if self.rho(self.val[0], self.val[1], self.val[2]) > 0:
                sol = (self.compute_sol())
            else:
                return []
        elif self.image == "Complex":
            tmp_sol = self.round(tmp_sol)
            sol = [str(tmp_sol[0]) + ',' + str(tmp_sol[1]), str(tmp_sol[1]) + ',' + str(tmp_sol[0])]
        else:
            raise ValueError("Wrong value for image:", self.image)

        #  return self.round(sol)
        return sol

    @staticmethod
    def rho(a, b, c):
        return b ** 2 - 4 * a * c

    def compute_sol(self):
        # For ax²+bx+c
        if self.domain == "Rational":
            a, b, c = self.remove_fract()
        else:
            a, b, c = self.val
        rho = self.rho(a, b, c)
        if rho < 0 and (self.domain == "Integer" or self.domain == "Rational"):
            return None
        sqrt_rho = math.sqrt(rho)
        num_neg = -1 * b - math.sqrt(rho)
        num_pos = -1 * b + math.sqrt(rho)
        if self.domain == "Integer" or self.image == "Integer":
            num_neg = int(num_neg)
            num_pos = int(num_pos)
        den = 2 * a

        if sqrt_rho.is_integer():
            if num_neg % den == 0:
                ans1 = self.simple_answer(num_neg, den)
            else:
                ans1 = self.ans_with_frac(num_neg, den, True)
            if num_pos % den == 0:
                ans2 = self.simple_answer(num_pos, den)
            else:
                ans2 = self.ans_with_frac(num_pos, den, True)
        else:
            ans1 = self.ans_with_root(rho, "-", a, b, c, True)  # .format(-1 * self.val[1], rho, 2 * self.val[2])
            ans2 = self.ans_with_root(rho, "+", a, b, c, True)  # .format(-1 * self.val[1], rho, 2 * self.val[2])
        return [ans1 + ',' + ans2, ans2 + ',' + ans1]

    def new_question(self, sol):
        question_desc = "Calculer les racines de: "
        if self.domain == "Integer":
            equation = ("{:-d}x²{:+d}x{:+d}".format(self.val[0], self.val[1], self.val[2]))
        elif self.domain == "Rational":
            equation = ("({:s})x²+({:s})x+({:s})".format(str(self.val[0]), str(self.val[1]), str(self.val[2])))
        equation = self.pretty_polynomial_string(equation)
        question_desc += equation
        # if sol.__len__() > 1:
        #     sol = tuple(sol)
        # else:
        #     sol = sol[0]
        answers = yaml.dump(OrderedDict([("answers", sol), ("type", "math-advanced")]))
        question = Question(description=question_desc, answer=answers, source="Génerée automatiquement")
        return question

    def gen_questions(self, number_of_questions):
        questions = list()
        for _ in range(number_of_questions):
            # We only want problems having a solution
            # TODO : Avoid looping
            while not self.get_sol():
                self.gen_new_values()
            questions.append((self.new_question(self.get_sol())))
            # TODO : Check if no two problems the same
            self.gen_new_values()
        return questions

    def get_context(self):
        default_context = self.default_context()
        # TODO Get from db if already Context already exist
        # context, created = Context.objects.get_or_create(defaults=default_context, file_name="generated")
        return default_context

    def remove_fract(self):
        num_a, den_a = self.val[0].numerator, self.val[0].denominator
        num_b, den_b = self.val[1].numerator, self.val[1].denominator
        num_c, den_c = self.val[2].numerator, self.val[2].denominator

        return self.common_divisor(num_a * den_b * den_c, num_b * den_a * den_c, num_c * den_a * den_b)

    @staticmethod
    def default_context():
        description = "Calculer les racines $$ x_1, x_2 $$ d'un polyonme du second degré <br/> " \
                      "<b> Attention : </b> les réponses doivent être sous la forme " \
                      "$$ x_1, x_2 $$ les réponses sous formes de fractions doivent être simplifiés au maximum <br/>" \
                      "utilisez le clavier spécial pour taper vos réponses sous formes d'équations"
        skill_id = "T4-U5-A1b"
        default_context = Context.objects.create(
            file_name="generated",
            skill=Skill.objects.get(code=skill_id),
            context=description,
            added_by=None
        )
        return default_context

    @staticmethod
    def make_form(post_values):
        return ArithmeticForm(post_values)

    def ans_with_root(self, rho, sign, a, b, c, simplify=False):
        if not simplify:
            return r"\frac{" + str(-1 * b) + sign + "\sqrt{" + str(rho) + "}}{" + str(2 * a) + "}"
        else:
            (factor_root, reduced) = self.reduced_sqrt(rho)
            (num_1, num_2, den) = self.common_divisor(-1 * b, factor_root, 2 * a)

            if den < 0:
                num_1 *= -1
                den *= -1
                num_2 *= -1

            if num_2 < 0:
                if sign == "-":
                    num_2 *= -1
                    sign = "+"
                else:
                    sign = ""
            else:
                if sign == "-":
                    pass
                else:
                    pass

            if den == 1 and num_2 == 1:
                return str(num_1) + sign + "\sqrt{" + str(reduced) + "}"
            elif num_2 == 1:
                return r"\frac{" + str(num_1) + "+" + "\sqrt{" + str(reduced) + "}}{" + str(den) + "}"
            elif num_2 == -1:
                return r"\frac{" + str(num_1) + "-" + "\sqrt{" + str(reduced) + "}}{" + str(den) + "}"
            elif den == 1:
                return str(num_1) + sign + str(num_2) + "\sqrt{" + str(reduced) + "}"
            else:
                return r"\frac{" + str(num_1) + sign + str(num_2) + "\sqrt{" + str(reduced) + "}}{" + str(den) + "}"

    @staticmethod
    def ans_with_frac(num, den, simplify=False):
        if not simplify:
            return r"\frac{" + str(num) + "}{" + str(den) + "}"
        else:
            f = Fraction(int(num), int(den))
            if den == 1:
                return str(f.numerator)
            else:
                return r"\frac{" + str(f.numerator) + "}{" + str(f.denominator) + "}"

    @staticmethod
    def simple_answer(num, den):
        return str(num / den)

    @staticmethod
    # TODO Make it prettier
    def pretty_polynomial_string(string):
        string = re.sub(r"\+-", r"-", string)
        string = "   " + string + "   "
        string = re.sub(r"(\+|-|\s)0x*²*(\+|-|\s)", r"\2", string)
        string = re.sub(r"(\+|-|\s)1(x²*)(\+|-|\s)", r"\2\3", string)
        return string

    @staticmethod
    def reduced_sqrt(n):
        """Return most reduced form of square root
        of n as the couple (coefficient, reduced_form)
        """
        if isinstance(n, int):
            root = int(math.sqrt(n))

            for factor_root in range(root, 1, -1):
                factor = factor_root * factor_root
                if n % factor == 0:
                    reduced = n // factor
                    return factor_root, reduced

        return 1, n

    @staticmethod
    def common_divisor(num_1, num_2, den):
        if isinstance(num_1, int) and isinstance(num_2, int) and isinstance(den, int):
            for div in range(min(abs(num_1), abs(num_2), abs(den)), 1, -1):
                if num_1 % div == 0 and num_2 % div == 0 and den % div == 0:
                    return num_1 / div, num_2 / div, den / div
        return num_1, num_2, den

    # @staticmethod
    # def latex(fraction):
    #     if fraction.numerator != 1:
    #         return r"\frac{" + str(fraction.numerator()) + "}{" + str(fraction.denominator()) + "}"
    #     else:
    #         return str(fraction.numerator)
