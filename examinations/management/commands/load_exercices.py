import os

import shutil

import yaml
import yamlordereddictloader

from django.core.management.base import BaseCommand

from skills.models import Skill
from examinations.models import Exercice


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in filter(lambda x: x.endswith((".yaml", ".yml")), os.listdir("exercices")):
            yaml.load(open("exercices/" + i), Loader=yamlordereddictloader.Loader)
            skill_code = i.split(".")[0].split("_")[0]

            skill = Skill.objects.get(code__iexact=skill_code)
            file_name = i.split(".")[0]

            if Exercice.objects.filter(file_name=file_name).exists():
                print "updating", file_name, "..."
                exercice = Exercice.objects.get(file_name=file_name)
            else:
                print "importing", file_name, "..."
                exercice = Exercice(file_name=file_name)

            exercice.skill = skill
            exercice.answer = open("exercices/" + i).read()
            exercice.content = open("exercices/" + file_name + ".html") if os.path.exists("exercices/" + file_name + ".html") else None,

            exercice.save()

        if not os.path.exists("examinations/static/exercices/"):
            os.makedirs("examinations/static/exercices/")

        for i in filter(lambda x: not x.endswith((".yaml", ".yml", ".html")) and not os.path.isdir("exercices/" + x), os.listdir("exercices")):
            print "saving image", i, "..."
            shutil.copyfile("exercices/" + i, "examinations/static/exercices/" + i)
