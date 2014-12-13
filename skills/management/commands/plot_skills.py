import os
from django.core.management.base import BaseCommand

from skills.models import Skill


class Command(BaseCommand):
    args = '<csv file>'
    help = 'Import skills tree out of a csv file'

    def handle(self, *args, **options):
        result = "\n"
        result += "digraph skills {\n"

        result += '    ranksep=2; size = "7.5,7.5";\n'
        result += '    graph [ dpi = 300 ];\n'
        result += '    {\n'
        result += '        node [shape=plaintext, fontsize=16];\n'
        result += '        3 -> 2 -> 1;\n'
        result += '    }\n'

        for skill in Skill.objects.order_by("-level", "-code"):
            for dep in skill.depends_on.all():
                result += '    "%s" -> "%s";\n' % (skill.code, dep.code)

        for level in [3, 2, 1]:
            result += '    {\n'
            result += '        rank = same;\n'
            result += '        %s;\n' % level
            for skill in Skill.objects.filter(level=level):
                result += '        "%s";\n' % skill.code
            result += '    }\n'

        result += "}\n"

        open("dot/skills.dot", "w").write(result)
        os.system("cd dot && dot -Tpng skills.dot > skills.png")
