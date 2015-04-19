import csv
from django.core.management.base import BaseCommand

from skills.models import Skill


class Command(BaseCommand):
    args = '<csv file>'
    help = 'Import skills tree out of a csv file'

    def handle(self, *args, **options):
        # Skill.objects.all().delete()

        dependancies = {}
        rubrique = ''

        for row in csv.DictReader(open(args[0], "r"), delimiter=",", quotechar='"'):

            rubrique = row['Rubrique'] if row['Rubrique'] else rubrique

            Skill.objects.create(
                name=row['Intitul\xc3\xa9'],
                description=row['Commentaires'],
                stage=row['\xc3\x89tape'],
                code=row['Code'],
                level=row['Niveau'],
                section=rubrique,
            )

            for next_ in filter(lambda x: x.startswith("S"), {row["suivant1"], row["suivant2"], row["suivant3"]}):
                dependancies.setdefault(row["Code"], []).append(next_)

        for key, value in filter(lambda (x, y): y, dependancies.iteritems()):
            skill = Skill.objects.get(code=key)
            for dep in value:
                Skill.objects.get(code=dep).depends_on.add(skill)
