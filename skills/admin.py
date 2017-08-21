# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Skill

class SkillAdmin(admin.ModelAdmin):
    pass

admin.site.register(Skill, SkillAdmin)

# Register your models here.
