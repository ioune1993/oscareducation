# encoding: utf-8

import json
import yaml
import yamlordereddictloader

from collections import OrderedDict

from django.db import models

from promotions.models import Lesson
from skills.models import Skill, StudentSkill


class Test(models.Model):
    name = models.CharField(max_length=255)
    lesson = models.ForeignKey(Lesson)
    skills = models.ManyToManyField(Skill)
    created_at = models.DateTimeField(auto_now_add=True)

    type = models.CharField(max_length=255, choices=(
        ("skills", "skills"),
        ("dependencies", "dependencies"),
        ("skills-dependencies", "skills-dependencies"),
    ))

    def display_test_type(self):
        if self.type == "skills":
            return "compétences"
        if self.type == "dependencies":
            return "prérequis"
        if self.type == "skills-dependencies":
            return "compétences et prérequis"

    def generate_skills_test(self):
        for skill in self.skills.all():
            TestExercice.objects.create(
                test=self,
                skill=skill,
            )

    def generate_dependencies_test(self):
        to_test_skills = []

        def recursivly_get_skills_to_test(skill):
            for i in skill.depends_on.all():
                if i not in to_test_skills:
                    to_test_skills.append(i)
                    recursivly_get_skills_to_test(i)

        for skill in self.skills.all():
            recursivly_get_skills_to_test(skill)

        for skill in to_test_skills:
            TestExercice.objects.create(
                test=self,
                skill=skill,
            )

    def generate_skills_dependencies_test(self):
        to_test_skills = []

        def recursivly_get_skills_to_test(skill):
            for i in skill.depends_on.all():
                if i not in to_test_skills:
                    to_test_skills.append(i)
                    recursivly_get_skills_to_test(i)

        for skill in self.skills.all():
            recursivly_get_skills_to_test(skill)

            TestExercice.objects.create(
                test=self,
                skill=skill,
            )

        for skill in to_test_skills:
            if TestExercice.objects.filter(skill=skill, test=self).exists():
                continue

            TestExercice.objects.create(
                test=self,
                skill=skill,
            )

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['created_at']


class Exercice(models.Model):
    file_name = models.CharField(max_length=255, unique=True)
    content = models.TextField(null=True, blank=True)
    answer = models.TextField()
    skill = models.ForeignKey(Skill)

    def __unicode__(self):
        return "on %s" % self.skill.code

    def get_questions(self):
        return yaml.load(self.answer, Loader=yamlordereddictloader.Loader)

    def is_valid(self, answers):
        for number, (key, value) in enumerate(self.get_questions().items()):
            answer = answers.get(str(number))
            answer = answer.strip().replace(" ", "") if isinstance(answer, basestring) else answer
            if value["type"] == "text":
                if not answer in value["answers"]:
                    return False
            elif value["type"] == "radio":
                if str(number) not in answers or not value["answers"].values()[int(answers[str(number)])]:
                    return False
            elif value["type"] == "checkbox":
                checkbox_answers = answers.getlist(str(number))
                for checkbox_number, is_correct in enumerate(value["answers"].values()):
                    if is_correct and str(checkbox_number) not in checkbox_answers:
                        return False
                    if not is_correct and str(checkbox_number) in checkbox_answers:
                        return False
            else:
                assert False

        return True


class TestExercice(models.Model):
    test = models.ForeignKey(Test)
    # it can happen that we need to test something but that we don't have an
    # exercice ready for it
    exercice = models.ForeignKey(Exercice, null=True)
    # therefor we need to remember which skill we are testing
    skill = models.ForeignKey(Skill)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "on test %s on skill %s" % (self.test.name, self.skill.code)

    class Meta:
        ordering = ['-skill__code']


class TestStudent(models.Model):
    student = models.ForeignKey("promotions.Student")
    test = models.ForeignKey(Test)
    finished = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)

    class Meta:
        ordering = ['test__created_at']

    def get_state(self):
        if not self.started_at:
            return "pas encore commencé"
        elif not self.finished_at:
            return "commencé"
        else:
            return "fini"

    def __unicode__(self):
        return u"on %s (%s)" % (self.student, self.get_state())


class Answer(models.Model):
    raw_answer = models.TextField(null=True, blank=True)  # let's store json

    # we might no know the answer if we want the teacher to correct the test by
    # hand
    correct = models.NullBooleanField()

    # if the answer is generated because the top skill was ok
    automatic = models.BooleanField(default=False)

    test_student = models.ForeignKey(TestStudent)
    test_exercice = models.ForeignKey(TestExercice)

    answer_datetime = models.DateTimeField(auto_now_add=True)

    def get_answers(self):
        """
        Here student_answers is in this form:

            [["1", "1"], ["0", "1"], ["2", "0"]]

        It's a json list of list where:

        * the first item of the list of list is the question number
        * the second one is the student answer

        This format sucks and should probably be modified to something like:

            [1, 1, 0]

        Or:

            {1: 1, 0: 1, 2: 0}

        Questions is in this form:

            OrderedDict({
                "this is the question summary" : {
                    "type": "question_type",
                    "answers": OrderedDict({
                        "questions 1 (right answer)": True,
                        "questions 2 (bad answer)": False,
                    })
                }
            })
        """

        if not self.test_exercice.exercice:
            return []

        result = OrderedDict()
        questions = yaml.load(self.test_exercice.exercice.answer, Loader=yamlordereddictloader.Loader)
        student_answers = dict(json.loads(self.raw_answer))

        for number, (question, answers) in enumerate(questions.items()):
            # XXX do all types
            student_answer = int(student_answers[str(number)])
            result[question] = {
                "type": answers["type"],
                "answer": answers["answers"].items()[student_answer][0],
                "correct": filter(lambda x: x[1], answers["answers"].items())[0][0],
           }

        return result

    def create_other_valide_answers(self):
        def add_correct_answer_to_skill(student_skill):
            # don't re-add an answer for myself
            if student_skill.skill == self.test_exercice.skill:
                return

            test_exercice = TestExercice.objects.filter(
                skill=student_skill.skill,
                test=self.test_student.test,
            )

            if not test_exercice.exists():
                return
            else:
                assert test_exercice.count() == 1
                test_exercice = test_exercice[0]

            # protection to avoid creating too much answers
            if Answer.objects.filter(test_student=self.test_student, test_exercice=test_exercice).exists():
                return

            Answer.objects.create(
                automatic=True,
                test_student=self.test_student,
                test_exercice=test_exercice,
                correct=True,
            )

        StudentSkill.objects.get(student=self.test_student.student, skill=self.test_exercice.skill).go_down_visitor(add_correct_answer_to_skill)

    def create_other_invalide_answers(self):
        def add_incorrect_answer_to_student_skill(student_skill):
            # don't re-add an answer for myself
            if student_skill.skill == self.test_exercice.skill:
                return

            test_exercice = TestExercice.objects.filter(
                skill=student_skill.skill,
                test=self.test_student.test,
            )

            if not test_exercice.exists():
                return
            else:
                assert test_exercice.count() == 1
                test_exercice = test_exercice[0]

            # protection to avoid creating too much answers
            if Answer.objects.filter(test_student=self.test_student, test_exercice=test_exercice).exists():
                return

            Answer.objects.create(
                automatic=True,
                test_student=self.test_student,
                test_exercice=test_exercice,
                correct=False,
            )

        StudentSkill.objects.get(student=self.test_student.student, skill=self.test_exercice.skill).go_up_visitor(add_incorrect_answer_to_student_skill)
