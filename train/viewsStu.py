# encoding: utf-8

import json

from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST
from django.db import transaction
from django.db.models import Q

# from examinations import generation
from examinations.models import TestStudent, Answer, TestExercice
from skills.models import StudentSkill, Skill, Section, CodeR, Relations, CodeR_relations
from end_test_poll.models import StudentPoll
from end_test_poll.forms import StudentPollForm
from resources.models import KhanAcademy, Sesamath, Resource


from utils import user_is_student


@user_is_student
def dashboard(request):
    return render(request, "student/dashboard.haml", {})


@user_is_student
def pass_test(request, pk):
    """A Student takes a Test"""
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
    irint(lesson_resource_khanacademy)
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
    """Saves the Student answers to a Context in a Test in the corresponding Answer"""
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
            """Returns the n'th occurrence of s splitted with the delimiter."""
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
                    # key has the form "graph-0-point-1-Y" for type_question-id_question-type_answer-id_answer
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
        is_correct = answer.evaluate()

        student_skill = StudentSkill.objects.get(student=request.user.student, skill=test_exercice.skill)

        if is_correct == 1:
            student_skill.validate(
                who=request.user,
                reason="Réponse à une question.",
                reason_object=test_exercice,
            )
        elif is_correct == 0:
            student_skill.unvalidate(
                who=request.user,
                reason="Réponse à une question.",
                reason_object=test_exercice,
            )

    # update student skills, then redirect to self
    return HttpResponseRedirect(reverse("student_pass_test", args=(test_student.id,)))


@require_POST
@user_is_student
def start_test(request, pk):
    """
    The Student starts a test that he can access
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


def skill_pedagogic_ressources(request, type, slug):
    """skill = get_object_or_404(Skill, code=slug)

    list_resource_id = list()
    # ManyToMany relation from Skill to Resource
    for skill_object in Skill.objects.all():
        for skill_object_resource in skill_object.resource.all():
            list_resource_id.append(skill_object_resource.id)

    personal_resource = Resource.objects.filter(added_by__professor__lesson__students=request.user.student, section="personal_resource", id__in=list_resource_id)

    return render(request, "professor/skill/update_pedagogical_resources.haml", {
        "object": skill,
        "skill": skill,
        "personal_resource": personal_resource,
    })"""

    if type == 'skill':
        base = get_object_or_404(Skill, code=slug)
    elif type == 'section':
        base = get_object_or_404(Section, id=slug)
    else:
        # type == 'coder'
        base = get_object_or_404(CodeR, id=slug)

    personal_resource = base.resource.filter(section="personal_resource")
    lesson_resource = base.resource.filter(section="lesson_resource")
    exercice_resource = base.resource.filter(section="exercice_resource")
    other_resource = base.resource.filter(section="other_resource")

    exercice_resource_sesamath = list()
    lesson_resource_sesamath = list()
    lesson_resource_khanacademy = list()

    sori_skills_lesson_resources = list()
    sori_skills_exercice_resources = list()
    sori_skills_other_resources = list()

    sori_skills_lesson_resource_sesamath = list()
    sori_skills_lesson_resource_khanacademy = list()
    sori_skills_exercice_resource_sesamath = list()

    sori_coder_lesson_resources = list()
    sori_coder_exercice_resources = list()
    sori_coder_other_resources = list()

    sori_coder_lesson_resource_sesamath = list()
    sori_coder_lesson_resource_khanacademy = list()
    sori_coder_exercice_resource_sesamath = list()

    # Sorting the different type of resources by category (personal, lesson, exercice or other)
    # and by type (khanacademy, sesamath or other)

    for exo in lesson_resource:
        if exo.content.get('from') and exo.content['from'] == "skills_sesamathskill":
            resource = get_object_or_404(Sesamath, pk=exo.content['referenced'])
            lesson_resource_sesamath.append([exo.pk, resource])
            lesson_resource = lesson_resource.exclude(pk=exo.pk)

        elif exo.content.get('from') and exo.content['from'] == "skills_khanacademyvideoskill":
            resource = get_object_or_404(KhanAcademy, pk=exo.content['referenced'])
            lesson_resource_khanacademy.append([exo.pk, resource])
            lesson_resource = lesson_resource.exclude(pk=exo.pk)

    for exo in exercice_resource:
        if exo.content.get('from') and exo.content['from'] == "skills_sesamathskill":
            resource = get_object_or_404(Sesamath, pk=exo.content['referenced'])
            exercice_resource_sesamath.append([exo.pk, resource])
            exercice_resource = exercice_resource.exclude(pk=exo.pk)

    # Do the same operation for similar or identical resources :
    # Some Skill or CodeR can be similar or identical to other Skill or CodeR
    # We have to display the resources of those as well

    # We achieve this only if we have either a Skill or a CodeR.
    # If it is a Section, we don't display the similar/identical resources
    # First step : is base a Skill or a CodeR ?
    if isinstance(base, Skill):
        # Begin with the Skills, same step is done for CodeR a bit further

        # Retrieve all the similar and identical Relations for Skills
        skills_from = Relations.objects.filter(Q(relation_type__in=['similar_to', 'identic_to'], from_skill=base.id))
        skills_to = Relations.objects.filter(Q(relation_type__in=['similar_to', 'identic_to'], to_skill=base.id))

        # This list will gather all the similar or 'identic' Skills
        # (similar_or_identic = sori)
        sori_skills = list()
        for skill_from in skills_from:
            sori_skills.append(skill_from.to_skill)
        for skill_to in skills_to:
            sori_skills.append(skill_to.from_skill)

        # Get the associated resources for these Skills
        # We need to keep them separated by section to ease their use in the template

        for skill in sori_skills:
            lesson = skill.resource.filter(section="lesson_resource")
            if lesson:
                sori_skills_lesson_resources.append([skill, lesson])
            exercice = skill.resource.filter(section="exercice_resource")
            if exercice:
                sori_skills_exercice_resources.append([skill, exercice])
            other = skill.resource.filter(section="other_resource")
            if other:
                sori_skills_other_resources.append([skill, other])

        # sori_skills_lesson_resources has resources of different types, we need to distinguish them
        for skill in sori_skills_lesson_resources:
            # Lists to regroup resources together
            sesamath_list = list()
            khan_list = list()

            for res in skill[1]:
                if res.content.get('from') and res.content['from'] == "skills_sesamathskill":
                    resource = get_object_or_404(Sesamath, pk=res.content['referenced'])
                    sesamath_list.append([res.pk, resource])
                    skill[1] = skill[1].exclude(pk=res.pk)

                elif res.content.get('from') and res.content['from'] == "skills_khanacademyvideoskill":
                    resource = get_object_or_404(KhanAcademy, pk=res.content['referenced'])
                    khan_list.append([res.pk, resource])
                    skill[1] = skill[1].exclude(pk=res.pk)

            # If we have emptied the ressources in the Skill, we remove it from the list
            if not skill[1]:
                sori_skills_lesson_resources.remove(skill)

            # Once resources are sorted, we can add them with the associated Skill
            if sesamath_list:
                sori_skills_lesson_resource_sesamath.append([skill[0], sesamath_list])
            if khan_list:
                sori_skills_lesson_resource_khanacademy.append([skill[0], khan_list])

        # sori_skills_exercice_resources has resources of different types, we need to distinguish them
        for skill in sori_skills_exercice_resources:
            # List to regroup resources together
            sesamath_list = list()

            for res in skill[1]:
                if res.content.get('from') and res.content['from'] == "skills_sesamathskill":
                    resource = get_object_or_404(Sesamath, pk=res.content['referenced'])
                    sesamath_list.append([res.pk, resource])
                    skill[1] = skill[1].exclude(pk=res.pk)

            # If we have emptied the ressources in the Skill, we remove it from the list
            if not skill[1]:
                sori_skills_exercice_resources.remove(skill)

            # Once resources are sorted, we can add them with the associated Skill
            if sesamath_list:
                sori_skills_exercice_resource_sesamath.append([skill[0], sesamath_list])

    if isinstance(base, CodeR) or isinstance(base, Skill):
        # Repeat this operation for the CodeR
        # TODO : Group these steps as a function for Skill and CodeR
        # Retrieve all the CodeR related to the current Skill or to the current CodeR

        if isinstance(base, Skill):
            related_coder = CodeR.objects.filter(skill=base.id)
        else:
            coder_from = CodeR_relations.objects.filter(
                Q(relation_type__in=['similar_to', 'identic_to'], from_coder=base.id))
            coder_to = CodeR_relations.objects.filter(
                Q(relation_type__in=['similar_to', 'identic_to'], to_coder=base.id))

            # This list will gather all the similar or 'identic' CodeR
            related_coder = list()
            for coder_from in coder_from:
                related_coder.append(coder_from.to_coder)
            for coder_to in coder_to:
                related_coder.append(coder_to.from_coder)
                # Case where we look for CodeR similar or identic to a CodeR

        # Get the associated resources for these CodeR

        for coder in related_coder:
            lesson = coder.resource.filter(section="lesson_resource")
            if lesson:
                sori_coder_lesson_resources.append([coder, lesson])
            exercice = coder.resource.filter(section="exercice_resource")
            if exercice:
                sori_coder_exercice_resources.append([coder, exercice])
            other = coder.resource.filter(section="other_resource")
            if other:
                sori_coder_other_resources.append([coder, other])

        # sori_skills_lesson_resources has resources of different types, we need to distinguish them
        for coder in sori_coder_lesson_resources:
            # Lists to regroup resources together
            sesamath_list = list()
            khan_list = list()

            for res in coder[1]:
                if res.content.get('from') and res.content['from'] == "skills_sesamathskill":
                    resource = get_object_or_404(Sesamath, pk=res.content['referenced'])
                    sesamath_list.append([res.pk, resource])
                    coder[1] = coder[1].exclude(pk=res.pk)

                elif res.content.get('from') and res.content['from'] == "skills_khanacademyvideoskill":
                    resource = get_object_or_404(KhanAcademy, pk=res.content['referenced'])
                    khan_list.append([res.pk, resource])
                    coder[1] = coder[1].exclude(pk=res.pk)

            # If we have emptied the ressources in the Skill, we remove it from the list
            if not coder[1]:
                sori_coder_lesson_resources.remove(coder)

            # Once resources are sorted, we can add them with the associated Skill
            if sesamath_list:
                sori_coder_lesson_resource_sesamath.append([coder[0], sesamath_list])
            if khan_list:
                sori_coder_lesson_resource_khanacademy.append([coder[0], khan_list])

        # sori_coder_exercice_resources has resources of different types, we need to distinguish them
        for coder in sori_coder_exercice_resources:
            # List to regroup resources together
            sesamath_list = list()

            for res in coder[1]:
                if res.content.get('from') and res.content['from'] == "skills_sesamathskill":
                    resource = get_object_or_404(Sesamath, pk=res.content['referenced'])
                    sesamath_list.append([res.pk, resource])
                    coder[1] = coder[1].exclude(pk=res.pk)

            # If we have emptied the ressources in the CodeR, we remove it from the list
            if not coder[1]:
                sori_coder_exercice_resources.remove(coder)

            # Once resources are sorted, we can add them with the associated CodeR
            if sesamath_list:
                sori_coder_exercice_resource_sesamath.append([coder[0], sesamath_list])


    sesamath_references_manuals = Sesamath.objects.filter(ressource_kind__iexact="Manuel")
    sesamath_references_cahiers = Sesamath.objects.filter(ressource_kind__iexact="Cahier")

    return render(request, "professor/skill/update_pedagogical_resources.haml", {
        "sesamath_references_manuals": sesamath_references_manuals,
        "sesamath_references_cahier": sesamath_references_cahiers,
        "base": base,
        "personal_resources": personal_resource,
        "other_resources": other_resource,
        "exercice_resources": exercice_resource,
        "exercice_resource_sesamath": exercice_resource_sesamath,
        "lesson_resources": lesson_resource,
        "lesson_resource_sesamath": lesson_resource_sesamath,
        "lesson_resource_khanacademy": lesson_resource_khanacademy,
        "type": type,
        "sori_skills_exercice_resources": sori_skills_exercice_resources,
        "sori_skills_lesson_resources": sori_skills_lesson_resources,
        "sori_skills_other_resources": sori_skills_other_resources,
        "sori_skills_lesson_resource_sesamath": sori_skills_lesson_resource_sesamath,
        "sori_skills_lesson_resource_khanacademy": sori_skills_lesson_resource_khanacademy,
        "sori_skills_exercice_resource_sesamath": sori_skills_exercice_resource_sesamath,
        "sori_coder_exercice_resources": sori_coder_exercice_resources,
        "sori_coder_lesson_resources": sori_coder_lesson_resources,
        "sori_coder_other_resources": sori_coder_other_resources,
        "sori_coder_lesson_resource_sesamath": sori_coder_lesson_resource_sesamath,
        "sori_coder_lesson_resource_khanacademy": sori_coder_lesson_resource_khanacademy,
        "sori_coder_exercice_resource_sesamath": sori_coder_exercice_resource_sesamath,
    })
