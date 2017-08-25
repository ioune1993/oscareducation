# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Skill, CodeR, Relations, CodeR_relations, Section

class SkillAdmin(admin.ModelAdmin):
    exclude = ('resource',)

class CoderAdmin(admin.ModelAdmin):
    exclude = ('resource',)

class RelationsAdmin(admin.ModelAdmin):
    pass

class CodeR_relationsAdmin(admin.ModelAdmin):
    pass
class SectionAdmin(admin.ModelAdmin):
    exclude = ('resource',)

admin.site.register(Skill, SkillAdmin)

admin.site.register(CodeR, CoderAdmin)

admin.site.register(Relations, RelationsAdmin)

admin.site.register(CodeR_relations, CodeR_relationsAdmin)

admin.site.register(Section, SectionAdmin)

# Register your models here.
