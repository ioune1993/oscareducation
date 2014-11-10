from django.contrib import admin
from .models import Skill, StudentSkill


class SkillAdmin(admin.ModelAdmin):
    pass


admin.site.register(Skill, SkillAdmin)


class StudentSkillAdmin(admin.ModelAdmin):
    pass


admin.site.register(StudentSkill, StudentSkillAdmin)
