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

    def validate(self):
        def recursivly_validate_student_skills(student_skill):
            student_skill.acquired = datetime.now()
            student_skill.save()

            for sub_student_skill in StudentSkill.objects.filter(skill__in=student_skill.skill.depends_on.all()):
                recursivly_validate_student_skills(sub_student_skill)

        recursivly_validate_student_skills(self)

    def unvalidate(self):
        def recursivly_unalidate_student_skills(student_skill):
            student_skill.acquired = None
            student_skill.tested = datetime.now()
            student_skill.save()

            for sub_student_skill in StudentSkill.objects.filter(skill__in=student_skill.skill.skill_set.all()):
                recursivly_unalidate_student_skills(sub_student_skill)

        recursivly_unalidate_student_skills(self)
