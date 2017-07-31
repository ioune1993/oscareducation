from django.contrib import admin
from .models import Test, Context
# @TODO Context replaces Exercice here, need to adapt


class TestAdmin(admin.ModelAdmin):
    pass

admin.site.register(Test, TestAdmin)


class ContextAdmin(admin.ModelAdmin):
    pass

admin.site.register(Context, ContextAdmin)
