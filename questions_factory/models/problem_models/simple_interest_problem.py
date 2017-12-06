# coding=utf-8
from examinations.models import *
import yaml

from questions_factory.models.problem_form import *
from questions_factory.models.problem_models.problem import *
from collections import OrderedDict
import random

from skills.models import Skill


class SimpleInterestProblem(Problem):

    NAME = "SimpleInterestProblem"

    def __init__(self, time_placed, type_rate, nb_decimal=2):
        super(SimpleInterestProblem, self).__init__(nb_decimal)
        if time_placed != "year" and time_placed != "month":
            raise ValueError
        if type_rate != "year" and type_rate != "month":
            raise ValueError
        self.amount = None
        self.rate = None
        self.time = None
        self.time_placed = time_placed  # year, month
        self.type_rate = type_rate  # year, month
        self.gen_values()

    def gen_values(self):
        self.amount = random.randint(5, 200000)
        self.rate = self.round(random.random())
        self.time = random.randint(1, 30)

    @staticmethod
    def make_form(post_values):
        return SimpleInterestForm(post_values)

    def get_sol(self):
        if self.time_placed == self.type_rate:
            return self.round(self.amount * self.time * self.rate)
        elif self.time_placed == "month" and self.type_rate == "year":
            return self.round((self.amount * (self.time/12.0) * self.rate))
        elif self.time_placed == "year" and self.type_rate == "month":
            return self.round((self.amount * (self.time*12.0) * self.rate))

    def gen_questions(self, number_of_questions):
        questions = list()
        for _ in range(number_of_questions):
            questions.append((self.new_question(self.get_sol())))
            self.gen_values()
        return questions

    def new_question(self, sol):
        time_unit = "mois" if self.time_placed == "month" else "ans"
        rate_unit = "mois" if self.type_rate == "month" else "ans"
        question_desc = "Si nous déposons à la banque une somme s'élevant à " + str(self.amount) + " euros " \
            "pour une durée de " + str(self.time) + " " + str(time_unit) + " à " \
            "un taux de " + str(self.rate) + "% par " + str(rate_unit) + ", quelle somme d'intérêts obtiendrons-nous " \
            "à la fin de cette période ? Arrondir à la " + str(self.nb_decimal) + "e décimale."
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
        description = "Calcul d'intérêt simple. \n" \
                      "Calculer un taux d'intérêt pour un placement en banque à taux fixe " \
                      "pour une durée " \
                      "déterminée, sachant que l'intérêt reçu n'est pas repris en compte pour le calcul " \
                      "de la somme d'intérêt suivante."
        skill_id = "T4-U5-A1b"
        default_context = Context.objects.create(
            file_name="generated",
            skill=Skill.objects.get(code=skill_id),
            context=description,
            added_by=None
        )
        return default_context



