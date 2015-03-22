from datetime import datetime

from django.db import models

from promotions.models import Student


class Skill(models.Model):
    code = models.CharField(max_length=20, unique=True, db_index=True)

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    level = models.PositiveIntegerField(db_index=True)
    stage = models.CharField(max_length=255)
    section = models.CharField(max_length=255)

    depends_on = models.ManyToManyField('Skill')

    def __unicode__(self):
        return "%s [%s]" % (self.code, self.level)


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
