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


class PythagorasProblem(Problem):

    NAME = "PythagorasProblem"

    default_triangle_rectangle = ['côté (a)', 'côté (b)']
    object_type = 'triangle_rectangle'
    object_name = 'du triangle rectangle'
    surname = 'right_triangle'

    def __init__(self, range_from, range_to, nb_decimal=2):
        super(PythagorasProblem, self).__init__(nb_decimal)
        self.figure = None
        self.range_from = range_from
        self.range_to = range_to
        # self.unit = unit
        #self.surname = ''
        self.gen_values()


    def gen_values(self):
        side_a = random.randint(self.range_from, self.range_to)
        side_b = random.randint(self.range_from, self.range_to)
        self.figure = [(self.default_triangle_rectangle[0], side_a),
                       (self.default_triangle_rectangle[1], side_b)]

    @staticmethod
    def make_form(post_values):
        return PythagorasProblemForm(post_values)

    def get_desc(self):
        pass

    def get_sol(self):
        if self.object_type == 'triangle_rectangle':
            return self.round(math.sqrt(math.pow(self.figure[0][1],2) + math.pow(self.figure[1][1],2)))  # c = sqrt(a^2+b^2)
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
        question_desc += 'Trouvez, en utilisant le Théorème de Pythagore, la longueur du côté (c) ' + self.object_name + ', dont les paramètres sont:<ul>'
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
        description = "Calcul de l'hypothénus d'un triangle rectangle"
        skill_id = "T4-U5-A1b" # needs a corresponding skill id
        default_context = Context.objects.create(
            file_name="generated",
            skill=Skill.objects.get(code=skill_id),
            context=description,
            added_by=None
        )
        return default_context
