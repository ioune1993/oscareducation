# coding=utf-8

from examinations.models import *
import yaml

from oscar.settings import STATIC_URL
from questions_factory.models.problem_form import *
from questions_factory.models.problem_models.problem import *
from collections import OrderedDict
import random
import math

from skills.models import Skill


class AreaProblem(Problem):

    NAME = "AreaProblem"

    default_triangle = ['base (b)', 'hauteur (h)']
    default_square = 'côté (c)'
    default_rectangle = ['longueur (L)', 'largeur (l)']
    default_rhombus = ['grande diagonale (d1)', 'petite diagonale (d2)']
    default_quadrilateral = ['côté (a)', 'côté (b)', 'côté (c)', 'côté (d)', 'angle(A)', 'angle (C)']
    default_trapezium = ['grande base (B)', 'petite base (b)', 'hauteur (h)']
    default_circle = 'rayon (r)'
    default_parallelogram = ['base (b)', 'hauteur (h)']
    default_regular_polygon = ['nombre de côtés (n)', 'côté(c)']
    object_type = None
    object_name = None

    def __init__(self, object_type, range_from, range_to, nb_decimal):
        super(AreaProblem, self).__init__(nb_decimal)
        if object_type != 'triangle'            \
            and object_type != 'square'   \
            and object_type != 'rectangle'      \
            and object_type != 'rhombus'       \
            and object_type != 'trapezium'      \
            and object_type != 'circle'\
            and object_type != 'parallelogram' \
            and object_type != 'regular_polygon' \
            and object_type != 'quadrilateral':
                raise ValueError
        self.object_type = object_type
        self.figure = None
        self.range_from = range_from
        self.range_to = range_to
        # self.unit = unit
        self.surname = ''
        self.gen_values()


    def gen_values(self):
        # round values XXX
        # units XXX
        if self.object_type == 'square':
            self.object_name = 'du carre'
            self.surname = 'square'
            side_a = random.randint(self.range_from, self.range_to)
            self.figure = [(self.default_square, side_a)]
        elif self.object_type == 'triangle':
            self.object_name = 'du triangle'
            self.surname = 'triangle'
            self.figure = [(self.default_triangle[0], random.randint(self.range_from, self.range_to)),
                           (self.default_triangle[1], random.randint(self.range_from, self.range_to))]
        elif self.object_type == 'rhombus':
            self.object_name = 'du losange'
            self.surname = 'rhombus'
            diagonal_g = random.randint(self.range_from, self.range_to)
            diagonal_p = random.randint(self.range_from, diagonal_g)
            self.figure = [(self.default_rhombus[0], diagonal_g),
                           (self.default_rhombus[1], diagonal_p)]
        elif self.object_type == 'rectangle':
            self.object_name = 'du rectangle'
            self.surname = 'rectangle'
            length = random.randint(self.range_from, self.range_to)
            width = random.randint(self.range_from, length)
            self.figure = [(self.default_rectangle[0], length),
                           (self.default_rectangle[1], width)]
        elif self.object_type == 'trapezium':
            self.object_name = 'du trapeze'
            self.surname = 'trapezium'
            base_g = random.randint(self.range_from, self.range_to)
            base_p = random.randint(self.range_from, base_g)
            height = random.randint(self.range_from, self.range_to)
            self.figure = [(self.default_trapezium[0], base_g),
                           (self.default_trapezium[1], base_p),
                           (self.default_trapezium[2], height)]
        elif self.object_type == 'quadrilateral':
            self.object_name = 'du quadrilatère'
            self.surname = 'quadrilateral'
            side_a = random.randint(self.range_from, self.range_to)
            side_b = random.randint(self.range_from, self.range_to)
            side_c = random.randint(self.range_from, self.range_to)
            side_d = random.randint(self.range_from, self.range_to)
            angle_a = self.round(random.uniform(math.pi / 2, math.pi))
            angle_c = self.round(random.uniform(math.pi / 2, math.pi))
            self.figure = [(self.default_quadrilateral[0], side_a),
                           (self.default_quadrilateral[1], side_b),
                           (self.default_quadrilateral[2], side_c),
                           (self.default_quadrilateral[3], side_d),
                           (self.default_quadrilateral[4], angle_a),
                           (self.default_quadrilateral[5], angle_c)]
        elif self.object_type == 'circle':
            self.object_name = 'du cercle'
            self.surname = 'circle'
            radius = random.randint(self.range_from, self.range_to)
            self.figure = [(self.default_circle[0], radius)]

        elif self.object_type == 'parallelogram':
            self.object_name = 'du parallélogramme'
            self.surname = 'parallelogram'
            self.figure = [(self.default_parallelogram[0], random.randint(self.range_from, self.range_to)),
                           (self.default_parallelogram[1], random.randint(self.range_from, self.range_to))]
        elif self.object_type == 'regular_polygon':
            num_side = random.randint(5, 10)
            side_size = random.randint(self.range_from, self.range_to)
            if num_side == 5:
                self.surname = 'pentagon'
                self.object_name = 'du pentagone'
                self.figure = [(self.default_regular_polygon[0], num_side),
                               (self.default_regular_polygon[1], side_size)]
            if num_side == 6:
                self.surname = 'hexagon'
                self.object_name = 'de l\'hexagone'
                self.figure = [(self.default_regular_polygon[0], num_side),
                               (self.default_regular_polygon[1], side_size)]
            if num_side == 7:
                self.surname = 'heptagon'
                self.object_name = 'de l\'heptagone'
                self.figure = [(self.default_regular_polygon[0], num_side),
                               (self.default_regular_polygon[1], side_size)]
            if num_side == 8:
                self.surname = 'octogon'
                self.object_name = 'de l\' octogon'
                self.figure = [(self.default_regular_polygon[0], num_side),
                               (self.default_regular_polygon[1], side_size)]
            if num_side == 9:
                self.surname ='enneagon'
                self.object_name = 'de l\'enneagone'
                self.figure = [(self.default_regular_polygon[0], num_side),
                               (self.default_regular_polygon[1], side_size)]
            if num_side == 10:
                self.surname ='decagon'
                self.object_name = 'du decagone'
                self.figure = [(self.default_regular_polygon[0], num_side),
                               (self.default_regular_polygon[1], side_size)]
        else:
            raise ValueError

    @staticmethod
    def make_form(post_values):
        return AreaProblemForm(post_values)

    def get_desc(self):
        pass

    def get_sol(self):
        if self.object_type == 'square':
            return self.round(self.figure[0][1] * self.figure[0][1])  # c^2
        elif self.object_type == 'circle':
            return self.round(math.pow(self.figure[0][1],2)*math.pi)  # pir^2
        elif self.object_type == 'rectangle':
            return self.round(self.figure[0][1] * self.figure[1][1])  # l*L
        elif self.object_type == 'quadrilateral':
            return self.round((0.5 * self.figure[0][1] * self.figure[3][1] * math.sin(math.radians(self.figure[4][1]))) + \
                    (0.5 * self.figure[1][1] * self.figure[2][1] * math.sin(math.radians(self.figure[5][1]))))
            # (a*d*sin(ab)/2) + (b*c*sin(bc)/2)
        elif self.object_type == 'rhombus':
            return self.round(2 * math.sqrt(math.pow(self.figure[0][1], 2) + math.pow(self.figure[1][1], 2)))  # 2sqr(d^2+D^2)
        elif self.object_type == 'trapezium':
            g_base = self.figure[0][1]
            p_base = self.figure[1][1]
            return self.round((g_base+p_base) * self.figure[2][1] / 2)
        elif self.object_type == 'triangle':
            return self.round(float(self.figure[0][1]) * self.figure[1][1] / 2)  # base * hauteur / 2
        elif self.object_type == 'parallelogram':
            return self. round(self.figure[0][1] * self.figure[1][1])  # 2 *a+ 2*b
        elif self.object_type == 'regular_polygon':
            number_side = self.figure[0][1]
            side_size = self.figure[1][1]
            return self.round(number_side * (math.pow(side_size, 2)) / (4 * math.tan(math.pi / number_side)))
        else:
            raise ValueError

    def gen_questions(self, number_of_questions):
        questions = list()
        for _ in range(number_of_questions):
            questions.append((self.new_question(self.get_sol())))
            self.gen_values()
        return questions

    def new_question(self, sol):
        question_desc = '<img style = "max-width: 600px;" src=\"' + str(STATIC_URL) + 'img/Figures/' + self.surname + '.png\" /><br>'
        question_desc += 'Calculer l\'aire ' + self.object_name + ' dont les parametres sont:<ul>'
        for e in self.figure:
            question_desc += '<br><li>%s = %s</li>' % (e[0], e[1])
        question_desc += '</ul>'
        answers = yaml.dump(OrderedDict([("answers", [sol]), ("type", "text")]))
        question = Question(description=question_desc, answer=answers, source="Génerée automatiquement")
        return question

    def get_context(self):
        default_context = self.default_context()
        # TODO Get from db if already Context already exist
        # context, created = Context.objects.get_or_create(defaults=default_context, file_name="generated")
        return default_context

    @staticmethod
    def default_context():
        description = "Calcul d'aire"
        skill_id = "T4-U5-A1b" # ??
        default_context = Context.objects.create(
            file_name="generated",
            skill=Skill.objects.get(code=skill_id),
            context=description,
            added_by=None
        )
        return default_context
