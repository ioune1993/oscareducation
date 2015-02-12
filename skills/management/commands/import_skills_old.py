import csv
from django.core.management.base import BaseCommand


from skills.models import Skill

class Command(BaseCommand):
    args = '<csv file>'
    help = 'Import skills tree out of a csv file'

    def handle(self, *args, **options):
        # Skill.objects.all().delete()

        dependancies = {}

        for row in csv.DictReader(open(args[0], "r"), delimiter=",", quotechar='"'):

            Skill.objects.create(
                name=row['Nom'],
                description=row['Commentaires'],
                code=row['Code'],
                level=row['Niveau'],
                section="",
            )

            for next_ in filter(lambda x: x, {row["suivant1"], row["suivant2"], row["suivant3"]}):
                dependancies.setdefault(row["Code"], []).append(next_)

        for key, value in filter(lambda (x, y): y, dependancies.iteritems()):
            skill = Skill.objects.get(code=key)
            for dep in value:
                Skill.objects.get(code=dep).depends_on.add(skill)
