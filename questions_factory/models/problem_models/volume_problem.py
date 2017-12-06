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


class VolumeProblem(Problem):

    NAME = "VolumeProblem"

    default_cube = 'cote (a)'
    default_cylinder = ['rayon de la base (r)', 'hauteur (h)']
    default_prism = ['base (b)', 'hauteur de la base (h)', 'hauteur (l)']
    default_cone = ['rayon de la base (r)', 'hauteur (h)']
    default_pyramid = ['longueur de la base (l)', 'largeur de la base (w)', 'hauteur (h)']
    object_type = None
    object_name = None

    def __init__(self, object_type, range_from, range_to, nb_decimal):
        super(VolumeProblem, self).__init__(nb_decimal)
        if object_type != 'cube'            \
            and object_type != 'cylinder'   \
            and object_type != 'prism'      \
            and object_type != 'cone'       \
                and object_type != 'pyramid':
                raise ValueError
        self.object_type = object_type
        self.figure = None
        self.range_from = range_from
        self.range_to = range_to
        self.gen_values()

    def gen_values(self):
        # round values XXX
        # units XXX
        base_length = random.randint(self.range_from, self.range_to)
        base_width = random.randint(self.range_from, self.range_to)
        height = random.randint(self.range_from, self.range_to)

        if self.object_type == 'cube':
            self.object_name = 'du cube'
            self.figure = [(self.default_cube, base_length)]
        elif self.object_type == 'cylinder':
            self.object_name = 'du cylindre'
            self.figure = [(self.default_cylinder[0], base_length),  # radius
                           (self.default_cylinder[1], height)]
        elif self.object_type == 'prism':
            self.object_name = 'du prisme'
            self.figure = [(self.default_prism[0], base_length),
                           (self.default_prism[1], base_width),  # triangle height
                           (self.default_prism[2], height)]
        elif self.object_type == 'cone':
            self.object_name = 'du cone'
            self.figure = [(self.default_cone[0], base_length),  # radius
                           (self.default_cone[1], height)]
        elif self.object_type == 'pyramid':
            self.object_name = 'de la pyramide'
            self.figure = [(self.default_pyramid[0], base_length),
                           (self.default_pyramid[1], base_width),
                           (self.default_pyramid[2], height)]
        else:
            raise ValueError

    @staticmethod
    def make_form(post_values):
        return VolumeProblemForm(post_values)

    def get_sol(self):
        if self.object_type == 'cube':
            return self.round(pow(self.figure[0][1], 3))
        elif self.object_type == 'cylinder':
            return self.round(math.pi * pow(self.figure[0][1], 2) * self.figure[1][1])
        elif self.object_type == 'prism':
            return self.round(0.5 * self.figure[0][1] * self.figure[1][1] * self.figure[2][1])
        elif self.object_type == 'cone':
            return self.round((math.pi * pow(self.figure[0][1], 2) * (self.figure[1][1] / 3)))
        elif self.object_type == 'pyramid':
            return self.round((self.figure[0][1] * self.figure[1][1] * self.figure[2][1]) / 3)
        else:
            raise ValueError

    def gen_questions(self, number_of_questions):
        questions = list()
        for _ in range(number_of_questions):
            questions.append((self.new_question(self.get_sol())))
            self.gen_values()
        return questions

    def new_question(self, sol):
        question_desc = '<img src=\"' + str(STATIC_URL) + 'img/Figures/' + self.object_type + '.png\" /><br>'
        question_desc += 'Calculer le volume ' + self.object_name + ' dont les parametres sont:<ul>'
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
        description = "Calcul de volume dans des figures en trois dimensions"
        skill_id = "T4-U5-A1b" # ??
        default_context = Context.objects.create(
            file_name="generated",
            skill=Skill.objects.get(code=skill_id),
            context=description,
            added_by=None
        )
        return default_context
