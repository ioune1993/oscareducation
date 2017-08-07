# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Professor,Student

class ProfessorAdmin(admin.ModelAdmin):
    search_fields = ('user',)
    list_display = ('user','is_pending','code')

class StudentAdmin(admin.ModelAdmin):
    search_fields = ('user',)
    list_display = ('user','is_pending','code','code_created_at')

admin.site.register(Professor,ProfessorAdmin)
admin.site.register(Student,StudentAdmin)
# Register your models here.
