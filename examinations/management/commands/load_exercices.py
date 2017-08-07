import os

import shutil

import yaml
import yamlordereddictloader

from django.core.management.base import BaseCommand

from skills.models import Skill
from examinations.models import Context


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in filter(lambda x: x.endswith((".yaml", ".yml")), os.listdir("exercices")):
            yaml.load(open("exercices/" + i), Loader=yamlordereddictloader.Loader)

            file_name = i.split(".")[0]

            if file_name.startswith(("S", "s")):
                real_name = file_name.replace("1_", "I_").replace("2_", "II_").replace("3_", "III_").replace("s", "S")
            else:
                real_name = file_name

            skill_code = real_name.split(".")[0].split("_")[0]

            if Context.objects.filter(file_name=file_name).exists():
                print "updating", file_name, "...", os.path.exists("exercices/" + file_name + ".html")
                exercice = Context.objects.get(file_name=file_name)
            else:
                print "importing", file_name, "..."
                exercice = Context(file_name=file_name)

            try:
                skill = Skill.objects.get(code__iexact=skill_code)
            except Skill.DoesNotExist:
                print "Warning: skill %s does NOT exist in db" % skill_code
                continue

            exercice.skill = skill
            exercice.answer = open("exercices/" + i).read()
            exercice.content = open("exercices/" + file_name + ".html").read() if os.path.exists("exercices/" + file_name + ".html") else None

            exercice.save()

        if not os.path.exists("examinations/static/exercices/"):
            os.makedirs("examinations/static/exercices/")

        for i in filter(lambda x: not x.endswith((".yaml", ".yml", ".html")) and not os.path.isdir("exercices/" + x), os.listdir("exercices")):
            print "saving image", i, "..."
            shutil.copyfile("exercices/" + i, "examinations/static/exercices/" + i)
