# encoding: utf-8

from django.db import models

from promotions.models import Student


class StudentPoll(models.Model):
    student = models.ForeignKey(Student)

    student_age = models.PositiveIntegerField(verbose_name=u"Mon âge")

    at_school_on_computer = models.BooleanField(verbose_name=u"à l'école sur ordinateur")
    at_school_on_tablette = models.BooleanField(verbose_name=u"à l'école sur tablette")
    at_school_on_smartphone = models.BooleanField(verbose_name=u"à l'école sur smartphone")

    at_home_on_computer = models.BooleanField(verbose_name=u"à la maison sur ordinateur")
    at_home_on_tablette = models.BooleanField(verbose_name=u"à la maison sur ordinateur")
    at_home_on_smartphone = models.BooleanField(verbose_name=u"à la maison sur ordinateur")

    on_smartphone_somewhere_else = models.BooleanField(verbose_name=u"ailleurs sur mon smartphone (par exemple dans le bus)")

    easy_to_connect_and_understand = models.PositiveIntegerField(verbose_name=u"Je me suis facilement connecté·e à Oscar et j'ai tout de suite compris ce qu'il fallaire faire :")

    difficulties = models.TextField(verbose_name=u"As-tu rencontré des difficultés ? Si oui, lesquelles ?")

    enjoyed_oscar = models.PositiveIntegerField(verbose_name=u"As-tu aimé utiliser Oscar ?")

    why = models.TextField(verbose_name=u"Pourquoi ?")

    my_teacher_should_use_oscar_more = models.BooleanField(verbose_name=u"Aimerais-tu que ton enseignant·e travaille plus souvent avec Oscar ?")

    is_oscar_usefull = models.TextField(verbose_name=u"Oscar te semble-t'il utile ? Si oui, pourquoi ?")

    saw_the_updated_skills_after_test = models.BooleanField(verbose_name=u"Après le test, tu as vu que tes compétences étaient mises à jour (avec des disques coloriés en orange ou vert) :")

    # Si oui, tu as compris que :
    meaning_orange_circles = models.TextField(verbose_name=u"Ronds oranges =")
    meaning_green_circles = models.TextField(verbose_name=u"Ronds verts =")
    meaning_white_circles = models.TextField(verbose_name=u"Ronds blancs =")

    # Tu as vu que tes compétences étaient mises à jour et...
    update_skills_motivated_me = models.BooleanField(verbose_name=u"cela t'a motivé")
    update_skills_i_understood = models.BooleanField(verbose_name=u"cela t'a démotivé")
    update_skills_i_havent_understood = models.BooleanField(verbose_name=u"pas compris")
    update_skills_havent_saw_it = models.BooleanField(verbose_name=u"pas vu tes compétences mises à jour")
    update_skills_other = models.TextField(verbose_name=u"autre :")

    what_on_oscar_to_better_learn_math = models.TextField(verbose_name=u"Qu'aimerais-tu avoir sur Oscar pour mieux apprendre les maths ?")
