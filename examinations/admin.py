from django.contrib import admin
from .models import Test, Exercice


class TestAdmin(admin.ModelAdmin):
    pass

admin.site.register(Test, TestAdmin)


class ExerciceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Exercice, ExerciceAdmin)
