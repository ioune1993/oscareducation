# encoding: utf-8

from datetime import datetime

from django.db import models
from django.core.urlresolvers import reverse

from promotions.models import Student


class Skill(models.Model):
    code = models.CharField(max_length=20, unique=True, db_index=True)

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    stage = models.ForeignKey("promotions.Stage")
    section = models.CharField(max_length=255)

    depends_on = models.ManyToManyField('Skill')

    image = models.CharField(max_length=255, null=True, blank=True)

    oscar_synthese = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['code']

    def __unicode__(self):
        return "%s [%s]" % (self.code, self.stage)

    def mermaid_graph(self):
        to_return = []
        def recurse_depends(skill):
            for dependancy in skill.depends_on.all():
                for top_dependancy in recurse_depends(dependancy):
                    yield top_dependancy
                yield "%s-->%s" % (dependancy.code, skill.code)
                yield '%s[<a style="color: white" href="%s">%s</a>]' % (dependancy.code, reverse("professor_skill_detail_view", args=(dependancy.code,)), dependancy.code)

        def recurse_is_a_dependacy_for(skill):
            for s in skill.skill_set.all():
                for top_dependancy in recurse_is_a_dependacy_for(s):
                    yield top_dependancy
                yield "%s-->%s" % (skill.code, s.code)
                yield '%s[<a style="color: white" href="%s">%s</a>]' % (s.code, reverse("professor_skill_detail_view", args=(s.code,)), s.code)

        for i in recurse_is_a_dependacy_for(self):
            if i not in to_return:
                to_return.append(i)

        for i in recurse_depends(self):
            if i not in to_return:
                to_return.append(i)

        to_return.append("style %s fill:#F58025;" % self.code)

        return to_return


class PedagogicalRessource(models.Model):
    skill = models.ForeignKey(Skill)

    title = models.CharField(max_length=255)
    duration = models.CharField(max_length=10)
    difficulty = models.PositiveSmallIntegerField()

    class Meta:
        abstract = True


class VideoSkill(PedagogicalRessource):
    url = models.URLField()


class KhanAcademyVideoSkill(models.Model):
    skill = models.ForeignKey(Skill)
    youtube_id = models.CharField(max_length=25)
    url = models.URLField()


class ExerciceSkill(PedagogicalRessource):
    questions = models.FileField(upload_to="pedagogique_ressources/exercices/questions/")
    answers = models.FileField(upload_to="pedagogique_ressources/exercices/answers/", blank=True, null=True, verbose_name=u"Réponses (optionnel)")


class ExternalLinkSkill(PedagogicalRessource):
    url = models.URLField()


class StudentSkill(models.Model):
    student = models.ForeignKey(Student)
    skill = models.ForeignKey(Skill)
    tested = models.DateTimeField(default=None, null=True)
    acquired = models.DateTimeField(default=None, null=True)
    # bad: doesn't support regression

    def __unicode__(self):
        return "%s - %s - %s" % (self.student, self.skill, "green" if self.acquired else ("orange" if self.tested else "white"))

    def go_down_visitor(self, function):
        # protective code against loops in skill tree
        already_done = set()

        def traverse(student_skill):
            function(student_skill)

            for sub_student_skill in StudentSkill.objects.filter(skill__in=student_skill.skill.depends_on.all(), student=self.student):
                if sub_student_skill.id not in already_done:
                    already_done.add(sub_student_skill.id)
                    traverse(sub_student_skill)

        traverse(self)

    def go_up_visitor(self, function):
        # protective code against loops in skill tree
        already_done = set()

        def traverse(student_skill):
            function(student_skill)

            for sub_student_skill in StudentSkill.objects.filter(skill__in=student_skill.skill.skill_set.all(), student=self.student):
                if sub_student_skill.id not in already_done:
                    already_done.add(sub_student_skill.id)
                    traverse(sub_student_skill)

        traverse(self)

    def validate(self):
        def validate_student_skill(student_skill):
            student_skill.acquired = datetime.now()
            student_skill.save()

        self.go_down_visitor(validate_student_skill)

    def unvalidate(self):
        def unvalidate_student_skill(student_skill):
            student_skill.acquired = None
            student_skill.tested = datetime.now()
            student_skill.save()

        self.go_up_visitor(unvalidate_student_skill)

    def default(self):
        self.acquired = None
        self.tested = None
        self.save()
