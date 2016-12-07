# encoding: utf-8

import json
import random
from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.db import transaction

from skills.models import Skill, StudentSkill, SkillHistory
from examinations.models import Test, Answer, TestExercice, TestStudent
from examinations import generation

from promotions.models import Lesson, Student
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

        # assign exercices when it's possible
        for test_exercice in test.testexercice_set.all():
            exercices = test_exercice.skill.exercice_set.filter(approved=True, testable_online=True)
            if not exercices.exists():
                if test.fully_testable_online:
                    test.fully_testable_online = False
                    test.save()

                test_exercice.testable_online = False

                # switch to offline exercices
                exercices = test_exercice.skill.exercice_set.filter(approved=True, testable_online=False)

                if not exercices.exists():
                    test_exercice.save()
                    continue

            test_exercice.exercice = exercices[random.choice(range(exercices.count()))]

            if generation.needs_to_be_generated(test_exercice.exercice.content):
                variables = generation.get_variable_list(test_exercice.exercice.content)
                test_exercice.rendered_content = generation.render(test_exercice.exercice.content, variables)
                test_exercice.variables = json.dumps(variables)

            test_exercice.save()


        test.save()

    return HttpResponse(str(test.id))


def lesson_test_online_insert_results(request, lesson_pk, pk):
    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    test = get_object_or_404(Test, pk=pk)

    if request.method == "POST":
        second_run = []
        print request.POST.items()

        with transaction.atomic():
            for key in filter(lambda x: x.startswith(("good", "bad", "unknown")), request.POST.values()):
                result, student, test_exercice = key.split("_", 2)
                print result, student, test_exercice
                student = Student.objects.get(pk=student)
                test_exercice = TestExercice.objects.select_related("skill").get(pk=test_exercice)
                test_student = TestStudent.objects.get(student=student, test=test)

                answer, _ = Answer.objects.get_or_create(
                    from_test_hybride=True,
                    test_exercice=test_exercice,
                    test_student=test_student,
                )

                student_skill = StudentSkill.objects.get(
                    student=student,
                    skill=test_exercice.skill,
                )

                reasons = {
                    "who": request.user,
                    "reason": "Exercice hors lignes pour un test hybride",
                    "reason_object": answer,
                }

                if result == "good":
                    student_skill.validate(**reasons)
                    answer.correct = True
                elif result == "bad":
                    student_skill.unvalidate(**reasons)
                    answer.correct = False
                else:
                    answer.correct = None

                answer.save()

                second_run.append([result, student_skill])

            # I redo a second run here because we can end up in a situation where
            # the teacher has enter value that would be overwritten by the
            # recursive walk and we want the resulting skills to match the teacher
            # input
            for result, student_skill in second_run:
                if result not in ("good", "bad"):
                    continue

                if result == "good":
                    student_skill.acquired = datetime.now()
                elif result == "bad":
                    student_skill.acquired = None
                    student_skill.tested = datetime.now()

                SkillHistory.objects.create(
                    skill=student_skill.skill,
                    student=student_skill.student,
                    value="acquired" if result == "good" else "not acquired",
                    by_who=request.user,
                    reason="Exercice hors lignes pour un test hybride (seconde passe)",
                    reason_object=answer,
                )

                student_skill.save()

        return HttpResponseRedirect(reverse('professor:lesson_test_online_detail', args=(lesson.pk, test.pk)))

    return render(request, "professor/lesson/test/online/fill.haml", {
        "lesson": lesson,
        "test": test,
    })
