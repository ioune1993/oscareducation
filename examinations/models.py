# encoding: utf-8

import json
import yaml
import yamlordereddictloader

from collections import OrderedDict

from django.db import models
from django.contrib.auth.models import User

from examinations import generation
from promotions.models import Lesson
from skills.models import Skill, StudentSkill

EMPTY_ENV = {
    "locals": None,
    "globals": None,
    "__name__": None,
    "__name__": None,
    "__file__": None,
    "__builtins__": None
}


class BaseTest(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom")
    lesson = models.ForeignKey(Lesson)
    skills = models.ManyToManyField(Skill)
    created_at = models.DateTimeField(auto_now_add=True)

    def prerequisistes(self):
        selected_skills = self.skills.all()

        return [x.skill for x in self.testexercice_set.exclude(skill__in=selected_skills).order_by('-skill__stage__level', '-skill__code')]

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['created_at']


class Test(BaseTest):
    running = models.BooleanField(default=True)
    fully_testable_online = models.BooleanField(default=True)

    type = models.CharField(max_length=255, choices=(
        ("skills", "skills"),
        ("dependencies", "dependencies"),
        ("skills-dependencies", "skills-dependencies"),
    ))

    def can_change_exercice(self):
        # not one has started its test
        return not self.teststudent_set.filter(started_at__isnull=False).exists()

    def testexercice_with_skills(self):
        return self.testexercice_set.select_related("skill").order_by('-skill__code')

    def teststudent_with_student(self):
        return self.teststudent_set.select_related("student", "student__user")

    def testexercice_testable_online(self):
        return self.testexercice_set.filter(testable_online=True).select_related("skill")

    def testexercice_testable_offline(self):
        return self.testexercice_set.filter(testable_online=False, exercice__isnull=False).select_related("skill")

    def add_student(self, student):
        TestStudent.objects.create(
            test=self,
            student=student
        )

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
                # we don't add dependancies that can't be tested online
                if i not in to_test_skills and skill.exercice_set.filter(testable_online=True).exists():
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


class TestFromClass(BaseTest):
    def get_skills_with_encoded_values(self):
        result = []

        students = self.lesson.students.all()
        skills = self.skills.all()
        encoded_values = {(x.student, x.skill): x for x in self.testskillfromclass_set.all().select_related("skill", "student").order_by("id")}

        for student in students:
            result.append((student, [(skill, encoded_values.get((student, skill))) for skill in skills]))

        return result


class TestSkillFromClass(models.Model):
    test = models.ForeignKey(TestFromClass)
    skill = models.ForeignKey(Skill)
    student = models.ForeignKey("promotions.Student")
    result = models.CharField(max_length=10, choices=(
        ("good", "acquise"),
        ("bad", "non acquise"),
        ("unknown", "inconnu"),
    ))

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('test', 'skill', 'student')
        ordering = ['student', 'skill__code']


class Exercice(models.Model):
    file_name = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    answer = models.TextField()
    skill = models.ForeignKey(Skill)

    testable_online = models.BooleanField(default=True)

    approved = models.BooleanField(default=True)

    added_by = models.ForeignKey(User, null=True)
    modified_by = models.ForeignKey(User, null=True, related_name="modified_exercices_set")

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"test_exercice.exercice n° %s on %s" % (self.id, self.skill.code)

    def get_questions(self):
        if self.answer:
            return yaml.load(self.answer, Loader=yamlordereddictloader.Loader)

        return {}

    def check_answers(self, answers):
        result = {
            "answers": []
        }

        for number, (question, value) in enumerate(self.get_questions().items()):
            result_answer = {"type": value["type"], "value": value, "correct": True, "question": question}
            result["answers"].append(result_answer)

            answer = answers.get(str(number))
            result_answer["answer"] = answer
            answer = answer.strip().replace(" ", "").lower().encode("Utf-8") if isinstance(answer, basestring) else answer
            result_answer["answer_cleaned"] = answer

            if value["type"] == "text":
                if isinstance(answer, (int, float)):
                    answer = str(answer)

                result_answer["correct_answers"] = [unicode(x).lower().strip().encode("Utf-8") for x in value["answers"]]
                if answer not in [x.replace(" ", "") for x in result_answer["correct_answers"]]:
                    result_answer["correct"] = False

            elif value["type"].startswith("math"):
                result_answer["correct_answers"] = [unicode(x).strip().lower().encode("Utf-8") for x in value["answers"]]
                if answer not in [x.replace(" ", "") for x in result_answer["correct_answers"]]:
                    result_answer["correct"] = False

            elif value["type"] == "radio":
                result_answer["correct_answers"] = value["answers"].values()

                # if no answer
                if str(number) not in answers:
                    result_answer["correct"] = False
                # if the student answer is not a valid answer don't fail
                elif int(answers[str(number)]) > len(value["answers"].values()):
                    result_answer["correct"] = False
                elif value["answers"].values()[int(answers[str(number)])] != True:
                    result_answer["correct"] = False

            elif value["type"] == "graph":
                result_answer["answers"] = []
                points_student_answers = []
                points_good_answers = []

                # first we need to get all student answer and all good answers
                for subnumber, graph_answers in enumerate(value["answers"]):
                    if graph_answers["graph"]["type"] == "point":
                        X = answers.get("graph-%s-point-%s-X" % (number, subnumber), "")
                        Y = answers.get("graph-%s-point-%s-Y" % (number, subnumber), "")

                        X = int(X) if X.isdigit() else None
                        Y = int(Y) if Y.isdigit() else None

                        points_student_answers.append({"X": X, "Y": Y})
                        points_good_answers.append(graph_answers["graph"]["coordinates"])
                    else:
                        assert False

                # now we need to see if the student answers are in the good answers
                for point in points_student_answers:
                    print point
                    result_answer["answers"].append({
                        "answer": point,
                        "correct": True,
                        "type": "point",
                    })
                    if point not in points_good_answers:
                        result_answer["answers"][-1]["correct"] = False
                        result_answer["answers"][-1]["correct_answer"] = None
                    else:
                        points_good_answers.remove(point)
                        result_answer["answers"][-1]["correct_answer"] = point

                # and for all bad answers lets put a correct answer next to it
                for i in result_answer["answers"]:
                    if i["correct_answer"] is None:
                        i["correct_answer"] = points_good_answers.pop()

                result_answer["correct"] = all([x["correct"] for x in result_answer["answers"]])

            elif value["type"] == "checkbox":
                # this case is only for the verication script
                if not hasattr(answers, "getlist"):
                    checkbox_answers = answers.get(str(number), [])
                    if not isinstance(checkbox_answers, list):
                        checkbox_answers = [checkbox_answers]
                else:
                    checkbox_answers = answers.getlist(str(number))

                result_answer["correct_answers"] = value["answers"]
                for checkbox_number, is_correct in enumerate(value["answers"].values()):
                    if is_correct and str(checkbox_number) not in checkbox_answers:
                        result_answer["correct"] = False
                    if not is_correct and str(checkbox_number) in checkbox_answers:
                        result_answer["correct"] = False
            else:
                assert False

        result["is_valid"] = all([x["correct"] for x in result["answers"]])
        return result


class TestExercice(models.Model):
    test = models.ForeignKey(Test)
    # it can happen that we need to test something but that we don't have an
    # exercice ready for it
    exercice = models.ForeignKey(Exercice, null=True)
    # therefor we need to remember which skill we are testing
    skill = models.ForeignKey(Skill)
    created_at = models.DateTimeField(auto_now_add=True)

    variables = models.TextField(null=True, blank=True)
    rendered_content = models.TextField(null=True, blank=True)

    testable_online = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.testable_online = bool(self.exercice and self.exercice.testable_online)
        super(TestExercice, self).save(*args, **kwargs)

    def get_content(self):
        if self.rendered_content:
            return self.rendered_content

        return self.exercice.content

    def get_questions(self):
        if not self.variables:
            return self.exercice.get_questions()

        variables = json.loads(self.variables)

        result = OrderedDict()
        for key, value in self.exercice.get_questions().items():
            if generation.needs_to_be_generated(key):
                key = generation.render(key, variables)

            if value["type"] == "text":
                value = value.copy()
                answers = []
                for i in value["answers"]:
                    if generation.needs_to_be_generated(i):
                        i = generation.render(i, variables)
                        i = eval(i, EMPTY_ENV)

                    answers.append(i)

                value["answers"] = answers

            result[key] = value

        return result

    def is_valid(self, answers):
        return self.exercice.check_answers(answers)["is_valid"]

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

    def test_exercice_answer_for_offline_test(self):
        answers = {x.test_exercice: x for x in self.answer_set.all().select_related("test_exercice")}

        return [(x, answers.get(x)) for x in TestExercice.objects.filter(test=self.test, testable_online=False, exercice__isnull=False)]

    def has_offline_answers(self):
        return self.answer_set.filter(test_exercice__testable_online=False).exists()

    def get_maybe_answer_list(self):
        answers = {x.test_exercice: x for x in self.answer_set.all().select_related("test_exercice").order_by("-test_exercice__skill__code")}

        return [answers.get(x) for x in TestExercice.objects.filter(test=self.test).order_by("-skill__code")]

    def get_state(self):
        if not self.started_at:
            return u"pas encore commencé"
        elif not self.finished_at:
            return u"commencé"
        else:
            return u"fini"

    def __unicode__(self):
        return u"on %s (%s)" % (self.student, self.get_state())


class Answer(models.Model):
    raw_answer = models.TextField(null=True, blank=True)  # let's store json

    # we might no know the answer if we want the teacher to correct the test by
    # hand
    correct = models.NullBooleanField()

    from_test_hybride = models.BooleanField(default=False)

    # if the answer is generated because the top skill was ok
    automatic = models.BooleanField(default=False)

    test_student = models.ForeignKey(TestStudent)
    test_exercice = models.ForeignKey(TestExercice)

    answer_datetime = models.DateTimeField(auto_now_add=True)

    def get_answers(self):
        """
        Here student_answers is in this form:

            {"1": 1, "0": "some text", "2": [1, 2]}

        * key is the sub question number
        * value is student answer
        * json saves key as strings, otherwises they would be ints

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

        if not self.test_exercice.testable_online:
            return []

        if not self.test_exercice.exercice:
            return []

        result = OrderedDict()
        questions = yaml.load(self.test_exercice.exercice.answer, Loader=yamlordereddictloader.Loader)
        student_answers = json.loads(self.raw_answer)

        for number, (question, answers) in enumerate(questions.items()):
            student_answer = student_answers[str(number)]

            if answers["type"] == "radio":
                result[question] = {
                    "type": answers["type"],
                    "answer": answers["answers"].items()[student_answer][0] if student_answer is not None else "",
                    "is_correct": answers["answers"].items()[student_answer][1] if student_answer is not None else False,
                    "correct": filter(lambda x: x[1], answers["answers"].items())[0][0],
                }
            elif answers["type"] == "text" or answers["type"].startswith("math"):
                result[question] = {
                    "type": answers["type"],
                    "answer": student_answer,
                    "is_correct": student_answer in answers["answers"],
                    "correct": answers["answers"],
                }
            elif answers["type"] == "checkbox":
                result[question] = {
                    "type": answers["type"],
                    "answer": [answers["answers"].items()[int(x)][0] for x in student_answer],
                    "is_correct": [x[0] for x in enumerate(answers["answers"].items()) if x[1][1]] == student_answer,
                    "correct": [x[0] for x in answers["answers"].items() if x[1]],
                }
            elif answers["type"] == "graph":
                r = []
                points_student_answers = []
                points_good_answers = []

                # first we need to get all student answer and all good answers
                for subnumber, graph_answers in enumerate(answers["answers"]):
                    if graph_answers["graph"]["type"] == "point":
                        X = student_answer["graph-%s-point-%s-X" % (number, subnumber)]
                        Y = student_answer["graph-%s-point-%s-Y" % (number, subnumber)]

                        X = int(X) if X.isdigit() else None
                        Y = int(Y) if Y.isdigit() else None

                        points_student_answers.append({"X": X, "Y": Y})
                        points_good_answers.append(graph_answers["graph"]["coordinates"])
                    else:
                        assert False

                # now we need to see if the student answers are in the good answers
                for point in points_student_answers:
                    print point
                    r.append({
                        "answer": dict(point),
                        "correct": True,
                        "type": "point",
                    })
                    if point not in points_good_answers:
                        r[-1]["correct"] = False
                        r[-1]["correct_answer"] = None
                    else:
                        points_good_answers.remove(point)
                        r[-1]["correct_answer"] = point

                # and for all bad answers lets put a correct answer next to it
                for i in r:
                    if i["correct_answer"] is None:
                        i["correct_answer"] = points_good_answers.pop()

                result[question] = {
                    "type": answers["type"],
                    "answers": r,
                    "is_correct": all([x["correct"] for x in r]),
                }
            else:
                print "Warning: unknown question type:", question, answers, self, self.test_exercice.exercice

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

    class Meta:
        ordering = ["-test_exercice__skill__code"]
