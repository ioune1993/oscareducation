from django.contrib import admin
from .models import Professor, Student, Lesson, Stage


class ProfessorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Professor, ProfessorAdmin)


class StudentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Student, StudentAdmin)


class LessonAdmin(admin.ModelAdmin):
    pass


admin.site.register(Lesson, LessonAdmin)


class StageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Stage, StageAdmin)
