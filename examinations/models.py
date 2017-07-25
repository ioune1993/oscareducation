# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField
from datetime import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Context(models.Model):
    """[FR] Contexte

        Whenever a Question is created, it is contained
        in a Context. A Context contains a list of
        Questions (at least one).

    """

    context = models.TextField(blank=True, null=True)
    """The Question(s) context, not mandatory."""
    skill = models.ForeignKey("skills.Skill")
    """The Skill to which the Context belongs"""

    added_by = models.ForeignKey(User, null=True)
    """The author of this Context and its Question(s)"""
    # TODO: added_by must be NOT NULL

    approved = models.BooleanField(default=True)
    """True if the question is in a correct format, False otherwise"""
    created_at = models.DateTimeField(auto_now_add=True)
    """Date of creation"""
    modified_at = models.DateTimeField(auto_now=True)
    """Date of the last modification"""
    testable_online = models.BooleanField(default=True)
    """True if the Context can be graded automatically, False otherwise"""
    file_name = models.CharField(max_length=255, null=True, blank=True)
    """The file/media attached to the Context, not mandatory"""


class List_question(models.Model):
    """List of questions

        Link between Contexts and Questions

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
    """The list of possible true answers, as well as false answers, depending on the type"""
    source = models.CharField(max_length=255, null=True, blank=True)
    """???"""


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
    """[

    """
    name = models.CharField(max_length=255, verbose_name="Nom")
    lesson = models.ForeignKey("promotions.Lesson")
    skills = models.ManyToManyField("skills.Skill")
    created_at = models.DateTimeField(auto_now_add=True)


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
    """The type test: it can test the Skills themselves, their prerequisites, or bot"""


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