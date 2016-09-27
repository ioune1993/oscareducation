import csv
import requests
from django.core.management.base import BaseCommand

from skills.models import SesamathReference


class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        for file_name in args:
            for row in csv.DictReader(open(file_name, "r"), delimiter=",", quotechar='"'):
                if not row["Emplacement sur site Oscar"] or not row["Emplacement sur site Oscar"].startswith(("http://", "https://")):
                    continue

                # print row["Emplacement sur site Oscar"]
                check = requests.get(row["Emplacement sur site Oscar"])
                if check.status_code != 200:
                    print file_name, row["Emplacement sur site Oscar"], check.status_code
                    continue

                if SesamathReference.objects.filter(on_oscar=row["Emplacement sur site Oscar"]):
                    ref = SesamathReference.objects.get(on_oscar=row["Emplacement sur site Oscar"])
                else:
                    ref = SesamathReference(on_oscar=row["Emplacement sur site Oscar"])

                ref.classe=row["Classe (France)"]
                ref.ressource_kind=row["Ressource"]
                ref.chapitre=row["Chapitre"]
                ref.title=row["Titre"]
                ref.section_kind=row["Fiche/page"]
                ref.year=row["Ann\xc3\xa9e"]
                ref.file_name=row["Nom du fichier"]

                ref.save()
