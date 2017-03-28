from django.core.management.base import BaseCommand

from examinations.models import Exercice


class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        for exercice in Exercice.objects.all():
            from ipdb import launch_ipdb_on_exception
            with launch_ipdb_on_exception():
                exercice.check_answers({})
