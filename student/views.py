from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST

from examinations.models import TestStudent

from utils import user_is_student


@user_is_student
def dashboard(request):
    return render(request, "student/dashboard.haml", {})


@user_is_student
def pass_test(request, pk):
    test_student = get_object_or_404(TestStudent, pk=pk)

    if test_student.student != request.user.student:
        raise PermissionDenied()

    # test is not already started, ask student to start it
    if not test_student.started_at:
        return render(request, "examinations/pass_test.haml", {
            "test": test_student.test,
            "test_student": test_student,
        })

    if request.method == "POST":
        # if POST -> answer check, validate question(s), update answers to TestExercice, update student skills, then redirect to self
        return HttpResponse("answer")


    # the order_by here is used to make the order of the exercices deterministics
    # so each student will have the exercices in the same order
    next_not_answered_test_exercice = test_student.test.testexercice_set.exclude(id__in=test_student.answer_set.all()).order_by('created_at').first()

    if next_not_answered_test_exercice is None:
        # TODO validate test
        pass

    if next_not_answered_test_exercice.exercice is None:
        # TODO try to grab an exercice
        pass

    return render(request, "examinations/take_exercice.haml", {
        "test_exercice": next_not_answered_test_exercice,
    })


@require_POST
@user_is_student
def start_test(request, pk):
    test_student = get_object_or_404(TestStudent, pk=pk)

    if test_student.student != request.user.student:
        raise PermissionDenied()

    test_student.started_at = datetime.now()
    test_student.save()

    return HttpResponseRedirect(reverse('student_pass_test', args=(test_student.pk,)))
