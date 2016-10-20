# encoding: utf-8

import json

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.db import transaction

from skills.models import Skill, StudentSkill
from examinations.models import Test

from promotions.models import Lesson
from promotions.utils import user_is_professor


@user_is_professor
def lesson_test_online_add(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    return render(request, "professor/lesson/test/online/add.haml", {
        "lesson": lesson,
        "stages": lesson.stages_in_unchronological_order(),
    })


@user_is_professor
@require_POST
def lesson_test_online_close_open(request, lesson_pk, pk):
    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    test = get_object_or_404(Test, pk=pk)

    test.running = not test.running
    test.save()

    return HttpResponseRedirect(reverse("professor:lesson_test_list", args=(lesson.pk,)))


@require_POST
@user_is_professor
def lesson_test_add_json(request):
    # TODO: a professor can only do this on one of his lesson
    # TODO: use django form

    data = json.load(request)

    lesson = get_object_or_404(Lesson, id=data["lesson"])

    if request.user.professor not in lesson.professors.all():
        raise PermissionDenied()

    with transaction.atomic():
        test = Test.objects.create(
            lesson=lesson,
            name=data["name"],
            type=data["type"],
        )

        for skill_id in data["skills"]:
            test.skills.add(Skill.objects.get(code=skill_id))

        for student in lesson.students.all():
            test.add_student(student)

        if data["type"] == "skills":
            test.generate_skills_test()
        elif data["type"] == "dependencies":
            test.generate_dependencies_test()
        elif data["type"] == "skills-dependencies":
            test.generate_skills_dependencies_test()
        else:
            raise Exception()

        test.save()

    return HttpResponse("ok")
