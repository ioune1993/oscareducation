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
                        number_of_checkboxs = len(answers["answers"])
                        true_false = (True, False)
                        # generate all number of possibilies matrice
                        bin_matrix = [(a, b, c, d, e, f, g) for a in true_false
                                                            for b in true_false
                                                            for c in true_false
                                                            for d in true_false
                                                            for e in true_false
                                                            for f in true_false
                                                            for g in true_false]

                        # reduce the number of possibilies to the number of checkbox
                        bin_matrix = [x[:number_of_checkboxs] for x in bin_matrix[:number_of_checkboxs]]

                        correct_answer = [str(n) for n, j in enumerate(answers["answers"].values()) if j]

                        for line in bin_matrix:
                            assert exercice.check_answers({
                                str(number): [str(n) for n, j in enumerate(line) if j]
                            })["answers"][number]["correct"] == (line == correct_answer)

                        # obviously broken answer
                        exercice.check_answers({
                            str(number): map(str, range(1500))
                        })

                    elif answers["type"] == "radio":
                        for radio_number, i in enumerate(answers["answers"].values()):
                            assert exercice.check_answers({
                                str(number): radio_number
                            })["answers"][number]["correct"] == i

                        assert exercice.check_answers({
                            str(number): "9999999"
                        })["answers"][number]["correct"] == False

                    elif answers["type"] == "graph":
                        pass
                    elif answers["type"] == "math-simple":
                        pass
                    elif answers["type"] == "math-advanced":
                        pass
                    else:
                        raise Exception("Exercice %s answers type is wrong: %s" % (exercice, answers.get("type")))

        from ipdb import set_trace; set_trace()
