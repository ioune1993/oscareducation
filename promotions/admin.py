from django.contrib import admin
from .models import Lesson, Stage
# @TODO Import Professor, Student ; need to adapt/correct/...


"""class ProfessorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Professor, ProfessorAdmin)


class StudentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Student, StudentAdmin)
"""

class LessonAdmin(admin.ModelAdmin):
    pass


admin.site.register(Lesson, LessonAdmin)


class StageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Stage, StageAdmin)
