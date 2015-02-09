import os
import yaml
import yamlordereddictloader
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in filter(lambda x: x.endswith((".yaml", ".yml")), os.listdir("exercices")):
            print yaml.load(open("exercices/" + i), Loader=yamlordereddictloader.Loader)
