# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField
from datetime import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import yaml
import yamlordereddictloader


class Context(models.Model):
    """
    [FR] Contexte

    Contains a list of :model:`examinations.Question` (at least one).
    """

    context = models.TextField(blank=True, null=True,
                               help_text="The general description related to the Question(s), not mandatory.")
    skill = models.ForeignKey("skills.Skill")

    added_by = models.ForeignKey(User, null=True,
                                 help_text="The Professor who created this Context and its Question(s)")
    # TODO: added_by must be NOT NULL

    approved = models.BooleanField(default=True, help_text="True if in a correct format, False otherwise")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date of creation")
    modified_at = models.DateTimeField(auto_now=True, help_text="Date of the last modification")
    testable_online = models.BooleanField(default=True, help_text="True if can be graded automatically, False otherwise")
    file_name = models.CharField(max_length=255, null=True, blank=True,
                                 help_text="\"submitted\" if created online,"
                                           " \"adapted\" if modified for a Test,"
                                           " \"[a_file_name]\" if the exercice is stored in a file"
                                           " (method not used anymore)")

    def get_questions(self):
        """Get all the questions attached to this Context."""
        list_questions = set()
        questions = set()
        for list_question in List_question.objects.filter(context=self.id):
            list_questions.add(list_question.question.id)
        for question in Question.objects.filter(id__in=list_questions):
            questions.add(question)
        return questions


class List_question(models.Model):
    """List of questions

        Link between Contexts and Questions.

    """

    context = models.ForeignKey('Context')
    """A Context"""
    question = models.ForeignKey('Question')
    """A Question"""


class Question(models.Model):
    """[FR] Question

        Represents a Question, that must belong
        to a Context.

    """
    # @todo after migration add type question filed from answer yaml structure

    description = models.TextField(blank=True, null=True)
    """The description is where states the question itself"""
    answer = models.TextField()
    """The list of possible true answers, as well as false answers, depending on the type.
        For now, the type is also included in this field."""
    source = models.CharField(max_length=255, null=True, blank=True)
    """Information that can only the Professors"""

    def get_answer(self):
        # Load YAML answer
        if self.answer:
            return yaml.load(self.answer, Loader=yamlordereddictloader.Loader)

        return {}


class Answer(models.Model):
    """[FR] Réponses

        The answers from a student, through a test,
        corresponding to Contexts (of Question(s))
        that belong to that test

    """

    raw_answer = JSONField(null=True, blank=True)  # let's store json
    """The answers the student provided to all the Question(s) belonging to a Context"""
    from_test_hybride = models.BooleanField(default=False)
    """Depreciated"""
    automatic = models.BooleanField(default=False)
    """If we already succeed in a Context which the Skill used our Context Skill as prerequisite,
        we automatically succeed to answer to this Context, whatever our raw_answer was"""
    test_student = models.ForeignKey("TestStudent")
    """The TestStudent (the test itself) corresponding to our answers"""
    test_exercice = models.ForeignKey("TestExercice")
    """The TestExercice (which Context in the test) corresponding to our answers"""
    answer_datetime = models.DateTimeField(auto_now_add=True)
    """The date we submitted our answers"""


class TestStudent(models.Model):
    """A student test

        The Test of a particular Student.

    """
    student = models.ForeignKey("users.Student")
    """The Student"""
    test = models.ForeignKey("Test")
    """The Test"""
    finished = models.BooleanField(default=False)
    """True if the Student has finished the Test, False otherwise"""
    started_at = models.DateTimeField(null=True)
    """The date the Student started the Test"""
    finished_at = models.DateTimeField(null=True)
    """The date the Student finished the Test"""


class TestExercice(models.Model):
    """A test context

        Represents the link between a Test and its Context(s)
        of Question(s).

    """
    test = models.ForeignKey("Test")
    """The Test"""
    exercice = models.ForeignKey("Context", null=True)
    """A Context that belongs to the Test"""
    skill = models.ForeignKey("skills.Skill")
    """The Skill of the Context, necessary in case there is no Context ready
        for this Skill"""
    created_at = models.DateTimeField(auto_now_add=True)
    """The date the Context was added to the Test"""
    variables = models.TextField(null=True, blank=True)
    """Unused field"""
    rendered_content = models.TextField(null=True, blank=True)
    """Unused field"""
    testable_online = models.BooleanField(default=True)
    """True if this Context is graded automatically, False otherwise"""


class BaseTest(models.Model):
    """Base for the Tests

        This is the common part of the Tests,
        whether "classic" or offline

    """
    name = models.CharField(max_length=255, verbose_name="Nom")
    """The test name"""
    lesson = models.ForeignKey("promotions.Lesson")
    """The Lesson in which this test stands"""
    skills = models.ManyToManyField("skills.Skill")
    """The Skill(s) tested in this test"""
    created_at = models.DateTimeField(auto_now_add=True)
    """The date the test was created"""


class Test(BaseTest):
    """[FR] Test

        A test created with Oscar, linked with
        a suite of Contexts, to evaluate a Student.

    """
    running = models.BooleanField(default=True)
    """True while it is open (available for students), becomes False when closed by the Professor"""
    enabled = models.BooleanField(default=True)
    """True if the test is visible, False if invisible (not to confuse with "running")"""
    fully_testable_online = models.BooleanField(default=True)
    """True if all the Contexts in the Test can be graded automatically"""

    type = models.CharField(max_length=255, choices=(
        ("skills", "skills"),
        ("dependencies", "dependencies"),
        ("skills-dependencies", "skills-dependencies"),
    ))
    """The type test: it can test the Skills themselves, their prerequisites, or both"""

    def can_change_exercice(self):
        # None of the students has started its test yet.
        return not self.teststudent_set.filter(started_at__isnull=False).exists()

    def add_student(self, student):
        """ subscribe new student in prof created tests """

        TestStudent.objects.create(
            test=self,
            student=student
        )

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


class TestFromClass(BaseTest):
    """[FR] Test hors-ligne

        This test is done in class, not with Oscar.
        Its purpose is to encode the results online.

    """
    pass


class TestSkillFromClass(models.Model):
    """[FR] Compétence de test hors-ligne

        This is the link between a TestFromClass
        and its Skill(s)

    """
    test = models.ForeignKey("TestFromClass")
    """The offline Test"""
    skill = models.ForeignKey("skills.Skill")
    """A Skill tested by the offline Test"""
    student = models.ForeignKey("users.Student")
    """The student that passed the offline Test"""
    result = models.CharField(max_length=10, choices=(
        ("good", "acquise"),
        ("bad", "non acquise"),
        ("unknown", "inconnu"),
    ))
    """The Skill result for the Student with the offline Test"""

    created_at = models.DateTimeField(auto_now_add=True)