import json
import random

from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST
from django.db import transaction

from examinations.models import TestStudent, Answer, TestExercice
from skills.models import StudentSkill, Skill

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

    if test_student.finished:
        return render(request, "examinations/test_finished.haml", {
            "test_student": test_student
        })

    # the order_by here is used to make the order of the exercices deterministics
    # so each student will have the exercices in the same order
    next_not_answered_test_exercice = TestExercice.objects.filter(test=test_student.test).exclude(answer__in=test_student.answer_set.all()).order_by('created_at').first()

    if request.method == "POST":
        # There is normally not way for a student to answer another exercice
        return validate_exercice(request, test_student, next_not_answered_test_exercice)

    if next_not_answered_test_exercice is None:
        test_student.finished = True
        test_student.finished_at = datetime.now()
        test_student.save()

        return render(request, "examinations/test_finished.haml", {
            "test_student": test_student
        })

    if next_not_answered_test_exercice.exercice is None and next_not_answered_test_exercice.skill.exercice_set.all().exists():
        with transaction.atomic():
            count = next_not_answered_test_exercice.skill.exercice_set.count()
            exercice = next_not_answered_test_exercice.skill.exercice_set.all()[random.choice(range(count))]
            next_not_answered_test_exercice.exercice = exercice
            next_not_answered_test_exercice.save()

    return render(request, "examinations/take_exercice.haml", {
        "test_exercice": next_not_answered_test_exercice,
    })


# not a view
def validate_exercice(request, test_student, test_exercice):
    if test_exercice.exercice is None:
        is_correct = request.POST.get("value") == "validate"
        raw_answer = None

    else:
        is_correct = test_exercice.exercice.is_valid(request.POST)
        raw_answer = json.dumps(filter(lambda x: x[0].isdigit(), request.POST.items()), indent=4)

    print is_correct

    with transaction.atomic():
        answer = Answer.objects.create(
            correct=is_correct,
            raw_answer=raw_answer,
            test_student=test_student,
            test_exercice=test_exercice,
        )

        student_skill = StudentSkill.objects.get(student=request.user.student, skill=test_exercice.skill)

        if is_correct:
            answer.create_other_valide_answers()
            student_skill.validate()
        else:
            answer.create_other_invalide_answers()
            student_skill.unvalidate()

    # update student skills, then redirect to self
    return HttpResponseRedirect(reverse("student_pass_test", args=(test_student.id,)))


@require_POST
@user_is_student
def start_test(request, pk):
    test_student = get_object_or_404(TestStudent, pk=pk)

    if test_student.student != request.user.student:
        raise PermissionDenied()

    test_student.started_at = datetime.now()
    test_student.save()

    return HttpResponseRedirect(reverse('student_pass_test', args=(test_student.pk,)))


@user_is_student
def skill_pedagogic_ressources(request, skill_code):
    skill = get_object_or_404(Skill, code=skill_code)

    return render(request, "student/skill_pedagogic_ressources.haml", {
        "skill": skill,
        "template_url": "skills/ressources/%s.html" % skill.code
    })
