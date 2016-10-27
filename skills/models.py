# encoding: utf-8

from datetime import datetime

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


from promotions.models import Student


class Skill(models.Model):
    code = models.CharField(max_length=20, unique=True, db_index=True)

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    section = models.CharField(max_length=255)

    depends_on = models.ManyToManyField('Skill')

    image = models.CharField(max_length=255, null=True, blank=True)

    oscar_synthese = models.TextField(null=True, blank=True)

    modified_by = models.ForeignKey(User, null=True)

    class Meta:
        ordering = ['code']

    def __unicode__(self):
        return self.code

    def mermaid_graph(self):
        to_return = []
        def recurse_depends(skill):
            for dependancy in skill.depends_on.all():
                for top_dependancy in recurse_depends(dependancy):
                    yield top_dependancy
                yield "%s-->%s" % (dependancy.code, skill.code)
                yield '%s[<a style="color: white" href="%s">%s</a>]' % (dependancy.code, reverse("professor:skill_detail", args=(dependancy.code,)), dependancy.code)

        def recurse_is_a_dependacy_for(skill):
            for s in skill.skill_set.all():
                for top_dependancy in recurse_is_a_dependacy_for(s):
                    yield top_dependancy
                yield "%s-->%s" % (skill.code, s.code)
                yield '%s[<a style="color: white" href="%s">%s</a>]' % (s.code, reverse("professor:skill_detail", args=(s.code,)), s.code)

        for i in recurse_is_a_dependacy_for(self):
            if i not in to_return:
                to_return.append(i)

        for i in recurse_depends(self):
            if i not in to_return:
                to_return.append(i)

        to_return.append("style %s fill:#F58025;" % self.code)

        return to_return


class SkillHistory(models.Model):
    skill = models.ForeignKey(Skill)
    student = models.ForeignKey(Student)
    datetime = models.DateTimeField(auto_now_add=True)
    value = models.CharField(max_length=255, choices=(
        ('unknown', 'Inconnu'),
        ('acquired', 'Acquise'),
        ('not acquired', 'None Acquise'),
    ))

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    reason_object = GenericForeignKey('content_type', 'object_id')
    reason = models.CharField(max_length=255)

    by_who = models.ForeignKey(User)

    class Meta:
        ordering = ['datetime']


class PedagogicalRessource(models.Model):
    skill = models.ForeignKey(Skill)

    title = models.CharField(max_length=255)
    duration = models.CharField(max_length=10)
    difficulty = models.PositiveSmallIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    added_by = models.ForeignKey(User, null=True)

    class Meta:
        abstract = True


class VideoSkill(PedagogicalRessource):
    url = models.URLField()


class KhanAcademyVideoSkill(models.Model):
    skill = models.ForeignKey(Skill)
    youtube_id = models.CharField(max_length=25)
    url = models.URLField()

    reference = models.ForeignKey("skills.KhanAcademyVideoReference", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    added_by = models.ForeignKey(User, null=True)


class KhanAcademyVideoReference(models.Model):
    subject = models.CharField(max_length=255)
    topic = models.CharField(max_length=255, blank=True, null=True)
    tutorial = models.CharField(max_length=255)
    youtube_id = models.CharField(max_length=25, unique=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100)
    duration = models.PositiveSmallIntegerField()
    fr_date_added = models.DateField(null=True, blank=True)
    linked_skills = models.ManyToManyField(KhanAcademyVideoSkill)

    class Meta:
        ordering = ['subject', 'topic', 'title']


class SesamathReference(models.Model):
    classe_int = models.PositiveSmallIntegerField()
    classe = models.CharField(max_length=255)
    # cahier, manuel
    ressource_kind = models.CharField(max_length=255)
    chapitre = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    # "Fiche/Page"
    section_kind = models.CharField(max_length=255)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    file_name = models.CharField(max_length=255)
    on_oscar = models.URLField(unique=True)

    def ressource_kind_with_year(self):
        if self.year:
            return u"%s - %s" % (self.year, self.ressource_kind)
        return self.ressource_kind

    class Meta:
        ordering = [
            'classe_int',
            'year',
            'ressource_kind',
            'chapitre',
            'section_kind',
        ]


class SesamathSkill(models.Model):
    skill = models.ForeignKey(Skill)
    reference = models.ForeignKey(SesamathReference)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    added_by = models.ForeignKey(User, null=True)

    class Meta:
        ordering = [
            'reference__classe_int',
            'reference__ressource_kind',
            'reference__chapitre',
            'reference__section_kind',
        ]


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
        return u"%s - %s - %s" % (self.student, self.skill, "green" if self.acquired else ("orange" if self.tested else "white"))

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

    def validate(self, who, reason, reason_object):
        def validate_student_skill(student_skill):
            SkillHistory.objects.create(
                skill=self.skill,
                student=self.student,
                value="acquired",
                by_who=who,
                reason=reason if student_skill == self else "Déterminé depuis une réponse précédente.",
                reason_object=reason_object,
            )

            student_skill.acquired = datetime.now()
            student_skill.save()

        self.go_down_visitor(validate_student_skill)

    def unvalidate(self, who, reason, reason_object):
        def unvalidate_student_skill(student_skill):
            SkillHistory.objects.create(
                skill=self.skill,
                student=self.student,
                value="not acquired",
                by_who=who,
                reason=reason if student_skill == self else "Déterminé depuis une réponse précédente.",
                reason_object=reason_object,
            )

            student_skill.acquired = None
            student_skill.tested = datetime.now()
            student_skill.save()

        self.go_up_visitor(unvalidate_student_skill)

    def default(self, who, reason, reason_object):
        SkillHistory.objects.create(
            skill=self.skill,
            student=self.student,
            value="unknown",
            by_who=who,
            reason=reason,
            reason_object=reason_object,
        )

        self.acquired = None
        self.tested = None
        self.save()

    def recommanded_to_learn(self):
        if self.acquired or not self.tested:
            return False

        for skill in self.skill.depends_on.all():
            skill = StudentSkill.objects.get(student=self.student, skill=skill)
            if not skill.acquired and skill.tested:
                return False

        return True


class GlobalResources(models.Model):
    title = models.CharField(max_length=255, verbose_name="titre")
    file = models.FileField(verbose_name="fichier")

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    added_by = models.ForeignKey(User)


class Resource(models.Model):
    skill = models.ForeignKey(Skill)

    title = models.CharField(max_length=255, verbose_name="Titre")
    author = models.CharField(max_length=255, null=True, blank=True, verbose_name="Auteur")

    kind = models.CharField(max_length=255, verbose_name="Object")

    text = models.TextField(null=True, blank=True, verbose_name="Texte")

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    added_by = models.ForeignKey(User)

    def files(self):
        return ResourceFile.objects.filter(resource=self)

    def links(self):
        return ResourceLink.objects.filter(resource=self)


class ResourcePart(models.Model):
    resource = models.ForeignKey(Resource)
    kind = models.CharField(max_length=255)

    title = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    added_by = models.ForeignKey(User)


class ResourceLink(ResourcePart):
    link = models.URLField()


class ResourceFile(ResourcePart):
    file = models.FileField()
