# encoding: utf-8

import csv
import requests
from django.core.management.base import BaseCommand

from skills.models import SesamathReference

classe_to_digit = {
   "Premi\xc3\xa8re professionnelle": 2,
   "Seconde professionnelle": 2,
   "Seconde": 2,
   "Troisième": 3,
   "Quatrième": 4,
   "Cycle 4 (ann\xc3\xa9es 5, 4 et 3)": 4,
   "Cinquième": 5,
   'Sixi\xc3\xa8me': 6,
   'Cm2': 7,
}

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        for file_name in args:
            for row in csv.DictReader(open(file_name, "r"), delimiter=",", quotechar='"'):
                if not row["Emplacement sur site Oscar"] or not row["Emplacement sur site Oscar"].startswith(("http://", "https://")):
                    continue

                if not row["Titre"].strip():
                    continue

                # print row["Emplacement sur site Oscar"]
                check = requests.get(row["Emplacement sur site Oscar"])
                if check.status_code != 200:
                    print file_name, row["Emplacement sur site Oscar"], check.status_code
                    continue

                on_oscar = row["Emplacement sur site Oscar"].replace("http", "https", 1) if row["Emplacement sur site Oscar"].startswith("http:") else row["Emplacement sur site Oscar"]

                if SesamathReference.objects.filter(on_oscar=row["Emplacement sur site Oscar"]):
                    ref = SesamathReference.objects.get(on_oscar=row["Emplacement sur site Oscar"])
                    if ref.on_oscar.startswith("http:"):
                        ref.on_oscar = ref.on_oscar.replace("http", "https", 1)
                elif SesamathReference.objects.filter(on_oscar=on_oscar):
                    ref = SesamathReference.objects.get(on_oscar=on_oscar)
                else:
                    ref = SesamathReference(on_oscar=row["Emplacement sur site Oscar"])

                ref.classe_int=classe_to_digit[row["Classe (France)"].capitalize().strip()]
                ref.classe=row["Classe (France)"].capitalize()
                ref.ressource_kind=row["Ressource"].capitalize()
                ref.chapitre=row["Chapitre"].capitalize()
                ref.title=row["Titre"].capitalize()
                ref.section_kind=row["Fiche/page"].capitalize()
                ref.year=row["Ann\xc3\xa9e"] if row["Ann\xc3\xa9e"] else None
                ref.file_name=row["Nom du fichier"]

                ref.save()
