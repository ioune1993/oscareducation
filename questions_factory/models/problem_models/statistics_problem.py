# coding=utf-8
import random
import numpy
import yaml

from collections import OrderedDict
from examinations.models import *
from questions_factory.models.problem_form import *
from questions_factory.models.problem_models.problem import *
from skills.models import Skill


class StatisticsProblem(Problem):

    NAME = "StatisticsProblem"

    def __init__(self, nb=10, range=(0, 20), nb_decimal=2):
        super(StatisticsProblem, self).__init__(nb_decimal)
        self.range = range
        self.values = None
        self.nb = nb
        self.gen_values()

    def gen_values(self):
        self.values = [random.randint(self.range[0], self.range[1]) for _ in range(self.nb)]

    def get_sol(self):
        sol = list()
        average = self.round(self.get_average())
        sol.append(average)
        median = self.round(self.get_median())
        sol.append(median)
        standard_deviation = self.round(self.get_standard_deviation())
        sol.append(standard_deviation)
        return sol

    def gen_questions(self, number_of_questions):
        questions = list()
        for _ in range(number_of_questions):
            questions.append((self.new_question(self.get_sol())))
            self.gen_values()
        return questions

    def new_question(self, sol):
        question_desc = "Voici une série de données recueillies pour chaque jour écoulée durant " + str(
            self.nb) + " jours : <br/>" \
                       "<div align=""center"" style=""overflow-x:auto;""><table style=""width:100%;"", style=""height: 100%;"", border=1px, text-align=""center""> <tr> <td align=""center""><b>Numéros de Journée </b></th> <td align=""center""> <b>Valeurs </b></th></tr>"
        n = 1
        for v in self.values:
            question_desc += "<tr><td> journée numéro " + str(n) + "</td>"
            question_desc += "<td align=""center"">" + str(v) + "</td></tr>"
            n += 1
        question_desc += "</table> </div>"

        answers = yaml.dump(OrderedDict([("answers", [sol]), ("type", "text")]))
        question = Question(description=question_desc, answer=answers, source="Génerée automatiquement")
        return question

    @staticmethod
    def make_form(post_values):
        return StatisticsForm(post_values)

    def get_context(self):
        default_context = self.default_context()
        # TODO Get from db if already Context already exist
        # context, created = Context.objects.get_or_create(defaults=default_context, file_name="generated")
        return default_context

    def default_context(self):
        description = "Calculer la moyennne, la médiane et l'écart-type des valeurs données<br/> " \
                      "<b> Attention : </b> les réponses doivent être sous la forme " \
                      "$$ [x_1, x_2, x_3] $$ dans l'ordre suivant : Moyenne, Médiane, Ecart-Type avec " + str(
            self.nb_decimal) + " chiffres après la virgule"
        skill_id = "T4-U5-A1b"
        default_context = Context.objects.create(
            file_name="generated",
            skill=Skill.objects.get(code=skill_id),
            context=description,
            added_by=None
        )
        return default_context

    def get_average(self):
        m = numpy.mean(self.values)
        return m

    def get_median(self):
        m = numpy.median(self.values)
        return m

    def get_standard_deviation(self):
        sd = numpy.std(self.values)
        return sd
