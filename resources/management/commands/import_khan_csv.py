import csv
import requests
from dateutil.parser import parse
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


            khan.subject = (row["Subject FR"] if row["Subject FR"] else row["Subject"]).strip()
            khan.topic = (row["Topic FR"] if row["Topic FR"] else row["Topic"]).strip()
            khan.tutorial = (row["Tutorial FR"] if row["Tutorial FR"] else row["Tutorial"]).strip()
            khan.slug = row["slug"].strip()
            khan.duration = row["duration"].strip()
            khan.fr_date_added = parse(row["fr_date_added"]) if row["fr_date_added"] else None

            if not khan.title:
                if row["Title FR"]:
                    khan.title = row["Title FR"].strip()
                    print "csv", row["fr"], [khan.title]
                else:
                    content = requests.get("http://fr.khanacademy.org/api/v1/videos/%s" % row["fr"])
                    if content.content == "null":
                        if row["title"]:
                            khan.title = row["title"].strip()
                            print "csv", row["fr"], [khan.title]
                        else:
                            continue
                    else:
                        khan.title = content.json()["translated_title"].strip()
                        print "api", row["fr"], khan.title

            khan.save()
