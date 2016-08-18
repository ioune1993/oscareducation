import csv
from django.core.management.base import BaseCommand

from skills.models import Skill
from promotions.models import Stage


STAGES_ORDER = [
    u'\xe9tape I (1\xa1 degr\xe9 primaire)',
    u'\xe9tape II (2\xa1 et 3\xa1 degr\xe9s primaire)',
    u'\xe9tape III (1\xa1 degr\xe9 secondaire)',
    u'3\xe8me ann\xe9e CPEONS',
    u'4\xe8me ann\xe9e CPEONS',
    u'5\xe8me ann\xe9e CPEONS',
    u'6\xe8me ann\xe9e CPEONS',
]


class Command(BaseCommand):
    args = '<csv file>'
    help = 'Import skills tree out of a csv file'

    def handle(self, *args, **options):
        dependancies = {}
        rubrique = ''

        to_link_to_stage = {}

        for row in csv.DictReader(open(args[0], "r"), delimiter=";", quotechar='"'):

            rubrique = row['Rubrique'] if row['Rubrique'] else rubrique

            if Skill.objects.filter(code=row["Code"]).exists():
                skill = Skill.objects.get(code=row["Code"])
                skill.depends_on.clear()
                print "update", row["Code"]
            else:
                skill = Skill()
                print "create", row["Code"]
                skill.code = row["Code"]

            if Stage.objects.filter(level=row['Niveau']).exists():
                stage = Stage.objects.get(level=row['Niveau'])
                stage.name = row['\xc3\x89tape']
            else:
                stage = Stage.objects.create(name=row['\xc3\x89tape'], level=row['Niveau'])

            if stage not in to_link_to_stage:
                to_link_to_stage[stage] = []

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

        first_stage = Stage.objects.get(name=STAGES_ORDER[0])
        print (u"[Stage] '%s' is the first stage (previous_stage is None)" % first_stage).encode("Utf-8")
        first_stage.previous_stage = None
        first_stage.save()

        for previous_stage, next_stage in zip(STAGES_ORDER, STAGES_ORDER[1:]):
            next_stage = Stage.objects.get(name=next_stage)
            previous_stage = Stage.objects.get(name=previous_stage)

            print (u"[Stage] '%s' depends on '%s'" % (next_stage, previous_stage)).encode("Utf-8")

            next_stage.previous_stage = previous_stage
            next_stage.save()
