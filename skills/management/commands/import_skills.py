import csv
from django.core.management.base import BaseCommand


from skills.models import Skill

class Command(BaseCommand):
    args = '<csv file>'
    help = 'Import skills tree out of a csv file'

    def handle(self, *args, **options):
        # Skill.objects.all().delete()

        for row in csv.DictReader(open(args[0], "r"), delimiter=",", quotechar='"'):
            Skill.objects.create(
                name=row['Intitul\xc3\xa9'],
                description=row['Commentaires'],
                stage=row['\xc3\x89tape'],
                code=row['Code'],
                level=row['Niveau'],
            )
