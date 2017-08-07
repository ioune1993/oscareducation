# encoding: utf-8

import json
import re

from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST
from django.db import transaction

# from examinations import generation
from examinations.models import TestStudent, Answer, TestExercice
from skills.models import StudentSkill, Skill
from resources.models import Resource
from end_test_poll.models import StudentPoll
from end_test_poll.forms import StudentPollForm


from utils import user_is_student


@user_is_student
def dashboard(request):
    return render(request, "student/dashboard.haml", {})


@user_is_student
def pass_test(request, pk):
    test_student = get_object_or_404(TestStudent, pk=pk)

    if test_student.student != request.user.student:
        raise PermissionDenied()

    if not test_student.test.running:
        return render(request, "examinations/test_closed.haml", {
            "test": test_student.test,
            "test_student": test_student,
        })

    # test is not already started, ask student to start it
    if not test_student.started_at:
        return render(request, "examinations/pass_test.haml", {
            "test": test_student.test,
            "test_student": test_student,
        })

    if test_student.finished:
        pool_form = None
        # TODO: poll disabled due to lack of the table in the DB
        """
        if not StudentPoll.objects.filter(student=test_student.student).exists():
            pool_form = StudentPollForm(request.POST) if request.method == "POST" else StudentPollForm()

            if request.method == "POST" and pool_form.is_valid():
                StudentPoll.objects.create(student=test_student.student, lesson=test_student.student.lesson_set.first(), **pool_form.cleaned_data)
                return HttpResponseRedirect(reverse('student_dashboard'))
            print pool_form.errors
        """
        return render(request, "examinations/test_finished.haml", {
            "test_student": test_student,
            "pool_form": pool_form,
        })

    # the order_by here is used to make the order of the exercices deterministics
    # so each student will have the exercices in the same order
    next_not_answered_test_exercice = TestExercice.objects.filter(test=test_student.test, exercice__isnull=False, testable_online=True).exclude(answer__in=test_student.answer_set.all()).order_by('created_at').first()

    if request.method == "POST":
        # There is normally no way for a student to answer another exercice
        return validate_exercice(request, test_student, next_not_answered_test_exercice)

    if next_not_answered_test_exercice is None or next_not_answered_test_exercice.exercice is None:
        test_student.finished = True
        test_student.finished_at = datetime.now()
        test_student.save()

        pool_form = None
        # TODO: poll disabled due to lack of the table in the DB
        #if not StudentPoll.objects.filter(student=test_student.student).exists():
        #    pool_form = StudentPollForm()

        return render(request, "examinations/test_finished.haml", {
            "test_student": test_student,
            #"pool_form": pool_form,
        })

    return render(request, "examinations/take_exercice.haml", {
        "test_exercice": next_not_answered_test_exercice,
    })


# not a view
def validate_exercice(request, test_student, test_exercice):
    raw_answer = None
    is_correct = False
    if test_exercice.exercice is None:
        raw_answer = None
        is_correct = False

    else:
        """
        raw_answer JSON format:
        correct : 1 if True, 0 if False, -1 if not corrected yet
        [
            {
                "0": {
                    "response": [
                        "some_response", "some_other_response"
                    ],
                    "correct": 1
                },
                "1": {
                    "response": [
                        "some_response"
                    ],
                    "correct": -1
                }
            }
        ]
        """
        # Help function
        def get_occurence(s, delimiter, occurence):
            """Returns the n'th occurrence of the s splitted with the delimiter."""
            return s.split(delimiter)[occurence]

        raw_answer = {}
        for number, question in enumerate(test_exercice.exercice.get_questions()):
            raw_answer[number] = {"response": [], "correct": -1}
            data = question.get_answer()
            if data["type"] == "checkbox":
                raw_answer[number]["response"] = list(map(int, request.POST.getlist(str(number))))
            elif data["type"] == "radio":
                if str(number) in request.POST:
                    raw_answer[number]["response"] = [int(request.POST[str(number)])]
                else:
                    # The Student did not select an answer
                    raw_answer[number]["response"] = -1
            elif data["type"] == "text":
                raw_answer[number]["response"] = [request.POST[str(number)]]
            elif data["type"].startswith("math"):
                raw_answer[number]["response"] = [request.POST[str(number)]]
            elif data["type"] == "graph":
                graph_list = list()
                for key, value in request.POST.items():
                    #key has the form "graph-0-point-1-Y" for type_question-id_question-type_answer-id_answer
                    if key == "csrfmiddlewaretoken":
                        continue
                    # If the graph element is read for the first time (a graph element may contain several coordinates)
                    pointNumber = get_occurence(key, "-", 2) + get_occurence(key, "-", 3)
                    doesExist = False
                    for elem in graph_list:
                        if "type" in elem:
                            if elem["type"] == str(pointNumber):
                                doesExist = True
                    if (len(request.POST.items())-1)/2 > len(graph_list) and not doesExist:
                        graph_list.append({"type": pointNumber})

                    # Case 1 : A point
                    if get_occurence(key, "-", 2) == "point":
                        # Format: graph-inputNumber-point-coordinate
                        # Neither X or Y have been read yet: initialization
                        for elem in graph_list:
                            if elem.get("type") == pointNumber:
                                nextElem = elem
                        if not nextElem.get("coordinates"):
                            nextElem["coordinates"] = {"X": 0, "Y": 0}
                        # Get the coordinate (X or Y, order is not guaranteed)
                        coordinate = get_occurence(key, "-", 4)
                        # First case : the X coordinate
                        if coordinate == "X":
                            nextElem["coordinates"]["X"] = value
                        # Then the Y coordinate
                        elif coordinate == "Y":
                            nextElem["coordinates"]["Y"] = value

                raw_answer[number]["response"] = graph_list

            elif data["type"] == "professor":
                raw_answer[number]["response"] = [request.POST[str(number)]]
            else:
                raise Exception()

            # Perform the correction
            raw_answer[number]["correct"] = question.evaluate(raw_answer[number]["response"])

        # The Student answers are embedded in a list, in a way that they can be extended if needed
        raw_answer = [raw_answer]
        raw_answer = json.dumps(raw_answer, indent=4)

    with transaction.atomic():
        answer = Answer.objects.create(
            raw_answer=raw_answer,
            test_student=test_student,
            test_exercice=test_exercice,
        )

        # Evaluates the answer of the whole attached Context to assess the related Skill
        is_correct = answer.evaluate

        student_skill = StudentSkill.objects.get(student=request.user.student, skill=test_exercice.skill)

        if is_correct:
            student_skill.validate(
                who=request.user,
                reason="Réponse à une question.",
                reason_object=test_exercice,
            )
        else:
            # Up traversal does not work, disabled
            """
            student_skill.unvalidate(
                who=request.user,
                reason="Réponse à une question.",
                reason_object=test_exercice,
            )
            """

    # update student skills, then redirect to self
    return HttpResponseRedirect(reverse("student_pass_test", args=(test_student.id,)))


@require_POST
@user_is_student
def start_test(request, pk):
    """
    The student starts a test that he can access
    and is not closed yet.
    """
    test_student = get_object_or_404(TestStudent, pk=pk)

    if test_student.student != request.user.student:
        raise PermissionDenied()

    if not test_student.test.running:
        return render(request, "examinations/test_closed.haml", {
            "test": test_student.test,
            "test_student": test_student,
        })

    test_student.started_at = datetime.now()
    test_student.save()

    return HttpResponseRedirect(reverse('student_pass_test', args=(test_student.pk,)))


def skill_pedagogic_ressources(request, slug):
    skill = get_object_or_404(Skill, code=slug)

    personal_resource = Resource.objects.filter(added_by__professor__lesson__students=request.user.student, section="personal_resource", skill=skill)

    return render(request, "professor/skill/update_pedagogical_resources.haml", {
        "object": skill,
        "skill": skill,
        "personal_resource": personal_resource,
    })
