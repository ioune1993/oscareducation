# encoding: utf-8

import csv
from django.core.management.base import BaseCommand

from skills.models import CodeR


class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        current_section = None
        for file_name in args:
            for row in csv.DictReader(open(file_name, "r"), delimiter=",", quotechar='"'):
                if row.get("Section"):
                    current_section = row["Section"]

                sub_code = row["Code"]
                name = row['Intitul\xc3\xa9']

                code_r = CodeR.objects.filter(section=current_section, sub_code=sub_code)

                if not code_r.exists():
                    code_r = CodeR.objects.create(section=current_section, sub_code=sub_code)
                else:
                    code_r = code_r.first()

                print code_r.code

                code_r.name = name
                code_r.save()
