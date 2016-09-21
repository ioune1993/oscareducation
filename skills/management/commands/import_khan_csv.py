import csv
from django.core.management.base import BaseCommand

from skills.models import KhanAcademyVideoReference


class Command(BaseCommand):
    args = '<csv file>'
    help = 'Import khan csv video references'

    def handle(self, *args, **options):
        for row in csv.DictReader(open(args[0], "r"), delimiter=",", quotechar='"'):
            if row["Domain"] != "Math":
                continue

            if not row["fr"]:
                continue

            if KhanAcademyVideoReference.objects.filter(youtube_id=row["fr"]).exists():
                khan = KhanAcademyVideoReference.objects.get(youtube_id=row["fr"])
            else:
                khan = KhanAcademyVideoReference(youtube_id=row["fr"])

            khan.subject = row["Subject"]
            khan.topic = row["Topic"]
            khan.tutorial = row["Tutorial"]
            khan.title = row["title"]
            khan.slug = row["slug"]
            khan.duration = row["duration"]
            khan.fr_date_added = row["fr_date_added"] if row["fr_date_added"] else None

            khan.save()
