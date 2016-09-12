import csv
from django.core.management.base import BaseCommand

from skills.models import Skill
from promotions.models import Stage


class Command(BaseCommand):
    args = '<csv file>'
    help = 'Import skills tree out of a csv file'

    def handle(self, *args, **options):
        dependancies = {}
        rubrique = ''

        to_link_to_stage = {}
        level_stages = {}

        for row in csv.DictReader(open(args[0], "r"), delimiter=",", quotechar='"'):

            if not filter(None, row.values()):
                continue

            rubrique = row['Rubrique'] if row['Rubrique'] else rubrique

            if Skill.objects.filter(code=row["Code"]).exists():
                skill = Skill.objects.get(code=row["Code"])
                skill.depends_on.clear()
                print "update", row["Code"]
            else:
                skill = Skill()
                print "create", row["Code"]
                skill.code = row["Code"]

            level = row['Niveau']

            stage_name = row['\xc3\x89tape'].strip().decode("Utf-8")

            if Stage.objects.filter(level=level, name=stage_name).exists():
                stage = Stage.objects.get(level=level, name=stage_name)
                stage.name = stage_name
            else:
                stage = Stage.objects.create(name=stage_name, level=level)

            if stage not in to_link_to_stage:
                to_link_to_stage[stage] = []

            if level not in level_stages:
                level_stages[level] = stage

            to_link_to_stage[stage].append(skill)

            skill.name=row['Intitul\xc3\xa9']
            skill.description=row['Commentaires']
            skill.section=rubrique
            skill.image=row["Image FontAwesome"]

            skill.save()

            for next_ in filter(lambda x: x, {row["suivant1"], row["suivant2"], row["suivant3"]}):
                dependancies.setdefault(row["Code"], []).append(next_)

        for key, value in filter(lambda (x, y): y, dependancies.iteritems()):
            print "on", key
            skill = Skill.objects.get(code=key)
            for dep in value:
                print " *", dep, "->", key
                Skill.objects.get(code=dep).depends_on.add(skill)

        for stage, skills in to_link_to_stage.items():
            print ("[Stage] Linking [%s]\n   -> %s" % (stage.name, "\n   -> ".join(sorted([x.code for x in skills])).encode("Utf-8")))
            stage.skills.clear()
            stage.skills.add(*skills)

        first_stage = level_stages[str(1)]
        print (u"[Stage] '%s' is the first stage (previous_stage is None)" % first_stage).encode("Utf-8")
        first_stage.previous_stage = None
        first_stage.save()

        sorted_stages = [x[1] for x in sorted(level_stages.items(), key=lambda x: x[0])]

        for previous_stage, next_stage in zip(sorted_stages, sorted_stages[1:]):
            print (u"[Stage] '%s' depends on '%s'" % (next_stage, previous_stage)).encode("Utf-8")

            next_stage.previous_stage = previous_stage
            next_stage.save()
