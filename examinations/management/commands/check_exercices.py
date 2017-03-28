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

        for exercice in Exercice.objects.filter(testable_online=True):
            with launch_ipdb_on_exception():
                for number, (question, answers) in enumerate(exercice.get_questions().items()):
                    if answers["type"] == "text":
                        for answer in answers["answers"]:
                            assert exercice.check_answers({
                                str(number): answer
                            })["answers"][number]["correct"] == True

                        assert exercice.check_answers({
                            str(number): "this is not a valid answer"
                        })["answers"][number]["correct"] == False
                    elif answers["type"] == "checkbox":
                        pass
                    elif answers["type"] == "graph":
                        pass
                    elif answers["type"] == "radio":
                        pass
                    elif answers["type"] == "math-simple":
                        pass
                    elif answers["type"] == "math-advanced":
                        pass
                    else:
                        raise Exception("Exercice %s answers type is wrong: %s" % (exercice, answers.get("type")))

        from ipdb import set_trace; set_trace()
