# encoding: utf-8

import os
import sys
import json
import traceback
import base64
import random
from django.core.files.storage import default_storage
import time
from django.core.files.base import ContentFile
from urlparse import urljoin
from itertools import izip

import yaml
import ruamel.yaml
import mechanize
import yamlordereddictloader
import pandas as pd

from ruamel.yaml.comments import CommentedMap

from base64 import b64decode
from collections import OrderedDict

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, resolve_url
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.views.decorators.http import require_POST
from django.db import transaction
from django.db.models import Count, Q

from skills.models import Skill, StudentSkill, CodeR, Section, Relations, CodeR_relations
from resources.models import KhanAcademy, Sesamath, Resource
from examinations.models import Test, TestStudent, BaseTest, TestExercice, Context, List_question, Question, Answer, \
    TestFromClass
from users.models import Student
from examinations.validate import validate_exercice_yaml_structure

from .models import Lesson, Stage
from .forms import LessonForm, StudentAddForm, SyntheseForm, KhanAcademyForm, StudentUpdateForm, LessonUpdateForm, \
    TestUpdateForm, SesamathForm, ResourceForm, CSVForm
from .utils import generate_random_password, user_is_professor, force_encoding
import csv
from django.http import JsonResponse
import re


@user_is_professor
def dashboard(request):
    """
    Return an HttpResponse to the dashboard of the Professor

    :param request:
    :return:
    """
    return render(request, "professor/dashboard.haml", {
        "lessons": Lesson.objects.filter(professors=request.user.professor).annotate(Count("students")).select_related(
            "stage"),
        "no_menu": True,
    })


@user_is_professor
def lesson_detail(request, pk):
    """
    Get the details of a Lesson (students and heatmap)

    :param request:
    :param pk: primary key of a Lesson
    :return:
    """
    lesson = get_object_or_404(Lesson, pk=pk)

    number_of_students = lesson.students.count()

    skill_to_student_skill = {}
    for student_skill in StudentSkill.objects.filter(student__lesson=lesson).select_related("skill"):
        skill_to_student_skill.setdefault(student_skill.skill, list()).append(student_skill)

    skills_to_heatmap_class = {}

    if lesson.students.count():
        try:
            skills = []
            for stage in lesson.stages_in_unchronological_order():
                skills.extend([x for x in stage.skills.all().order_by('-code')])

            for skill in skills:
                mastered = len([x for x in skill_to_student_skill[skill] if x.acquired])
                not_mastered = len([x for x in skill_to_student_skill[skill] if not x.acquired and x.tested])
                total = mastered + not_mastered

                # normally number_of_students will never be equal to 0 in this loop
                if total == 0:
                    skill.heatmap_class = "mastered_not_enough"
                    continue

                percentage = (float(mastered) / total) if total else 0

                if percentage < 0.25:
                    skills_to_heatmap_class[skill] = "mastered_25"
                elif percentage < 0.5:
                    skills_to_heatmap_class[skill] = "mastered_50"
                elif percentage < 0.75:
                    skills_to_heatmap_class[skill] = "mastered_75"
                else:
                    skills_to_heatmap_class[skill] = "mastered_100"
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            print e
            print "Error: could no calculate heatmap"

    return render(request, "professor/lesson/detail.haml", {
        "lesson": lesson,
        "number_of_students": number_of_students,
        "skills_to_heatmap_class": skills_to_heatmap_class,
    })


@user_is_professor
def lesson_add(request):
    """
    Either return an HttpResponse with a LessonForm or create a new Lesson if POST method

    :param request:
    :return:
    """
    form = LessonForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            lesson = form.save()
            lesson.professors.add(request.user.professor)
            return HttpResponseRedirect(reverse("professor:lesson_student_add", args=(lesson.pk,)))

    return render(request, "professor/lesson/create.haml", {
        "form": form,
    })


@user_is_professor
def lesson_update(request, pk):
    """
    Either return an HttpResponse with a LessonUpdateForm or update a Lesson if POST method

    :param request:
    :param pk:
    :return:
    """
    lesson = get_object_or_404(Lesson, pk=pk)

    form = LessonUpdateForm(request.POST, instance=lesson) if request.method == "POST" else LessonUpdateForm(
        instance=lesson)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("professor:lesson_detail", args=(lesson.pk,)))

    return render(request, "professor/lesson/update.haml", {
        "lesson": lesson,
        "form": form,
    })


@user_is_professor
def lesson_student_add(request, pk):
    """
    Add one or more students to a lesson : either with an XLS file (template provided) or manually

    :param request:
    :param pk: primary key of a Lesson
    :return:
    """
    lesson = get_object_or_404(Lesson, pk=pk)

    # TODO: a professor can only see one of his lesson

    if request.method == "POST":
        # Check the content of request.POST to know if we use a csv file or the manual addition
        if 'csvfile' in request.FILES:
            form = CSVForm(request.POST, request.FILES)
            if form.is_valid():
                xls = pd.ExcelFile(form.cleaned_data["csvfile"])
                sheet = xls.parse(0) # 0 is the sheet number
                try:
                    last_name_column = sheet['NOM']
                    first_name_column = sheet['PRENOM']
                except KeyError:
                    messages.add_message(request, messages.ERROR,
                                         'Erreur : les champs "NOM" et "PRENOM" n\' ont pas été '
                                         'trouvés. Ne modifiez pas la première ligne '
                                         'du fichier !')
                    return render(request, "professor/lesson/student/add.haml", {
                        "lesson": lesson,
                    })

                names = izip(last_name_column, first_name_column)

                line_number = 2
                for last_name,first_name in names:
                    # We use this form to create at the same time the username
                    newStudent = StudentAddForm({
                        "first_name": last_name,
                        "last_name": first_name,
                    })

                    if not newStudent.is_valid():
                        messages.add_message(request, messages.ERROR,
                                             'Erreur : l\'utilisateur à la ligne ' + str(line_number) +
                                             ' n\' a pas de nom ou de prénom. Uniquement les élèves des lignes '
                                             'précédentes ont été importés.')
                        return render(request, "professor/lesson/student/add.haml", {
                            "lesson": lesson,
                        })

                    first_name = newStudent.cleaned_data["first_name"]
                    last_name = newStudent.cleaned_data["last_name"]
                    username = newStudent.generate_student_username()
                    email = newStudent.get_or_generate_email(username)

                    with transaction.atomic():
                        user = User.objects.create_user(username=username,
                                                        email=email,
                                                        password=generate_random_password(15),
                                                        first_name=first_name,
                                                        last_name=last_name)
                        student = Student.objects.create(user=user)
                        student.lesson_set.add(lesson)

                        for stage in lesson.stages_in_unchronological_order():
                            for skill in stage.skills.all():
                                StudentSkill.objects.create(
                                    student=student,
                                    skill=skill,
                                )

                        for test in Test.objects.filter(lesson=lesson, running=True):
                            test.add_student(student)

                        line_number += 1
                if line_number == 2:
                    messages.add_message(request, messages.ERROR, 'Erreur : le fichier ne contient pas d\'élèves.')
                    return render(request, "professor/lesson/student/add.haml", {
                        "lesson": lesson, })
            else:
                messages.add_message(request, messages.ERROR, 'Erreur : le fichier fourni doit être en format .xls.')
                return render(request, "professor/lesson/student/add.haml", {
                    "lesson": lesson, })

            messages.add_message(request, messages.SUCCESS,
                                 str(line_number - 2) + ' utilisateur(s) a/ont été importé(s) avec succès.')

        elif 'last_name_0' in request.POST:
            for i in filter(lambda x: x.startswith("first_name_"), request.POST.keys()):
                number = i.split("_")[-1]
                form = StudentAddForm({
                    "first_name": request.POST["first_name_" + number],
                    "last_name": request.POST["last_name_" + number],
                })

                if not form.is_valid():
                    print "ERROR: on student entry with number %s" % number, form.errors
                    continue

                first_name = form.cleaned_data["first_name"]
                last_name = form.cleaned_data["last_name"]
                username = form.generate_student_username()
                email = form.get_or_generate_email(username)

                with transaction.atomic():
                    user = User.objects.create_user(username=username,
                                                    email=email,
                                                    password=generate_random_password(15),
                                                    first_name=first_name,
                                                    last_name=last_name)

                    student = Student.objects.create(user=user)
                    student.lesson_set.add(lesson)

                    for stage in lesson.stages_in_unchronological_order():
                        for skill in stage.skills.all():
                            StudentSkill.objects.create(
                                student=student,
                                skill=skill,
                            )

                    for test in Test.objects.filter(lesson=lesson, running=True):
                        test.add_student(student)

        return HttpResponseRedirect(reverse("professor:lesson_detail", args=(lesson.pk,)))

    return render(request, "professor/lesson/student/add.haml", {
        "lesson": lesson,
    })


@user_is_professor
def lesson_student_detail(request, lesson_pk, pk):
    """
    Query a Student and a Lesson to display it in the detail page

    :param request:
    :param lesson_pk: primary key of a Lesson
    :param pk: primary key of a Student
    :return:
    """
    # TODO: a professor can only see one of his students

    student = get_object_or_404(Student, pk=pk)

    return render(request, "professor/lesson/student/detail.haml", {
        "lesson": get_object_or_404(Lesson, pk=lesson_pk),
        "student": student,
    })


@user_is_professor
def lesson_student_update(request, lesson_pk, pk):
    """
    Display a form to change a Student's details or submit theses changes

    :param request:
    :param lesson_pk: primary key of a Lesson
    :param pk: primary key of a Student
    :return:
    """
    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    student = get_object_or_404(Student, pk=pk)

    form = StudentUpdateForm(request.POST, instance=student.user) if request.method == "POST" else StudentUpdateForm(
        instance=student.user)

    # TODO: a professor can only see one of his lesson

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("professor:lesson_student_detail", args=(lesson.pk, pk)))

    return render(request, "professor/lesson/student/update.haml", {
        "lesson": lesson,
        "student": student,
        "form": form,
    })


@user_is_professor
def lesson_student_test_detail(request, pk, lesson_pk, test_pk):
    """
    Query a Student, Lesson and a Test and display it in the test detail page

    :param request:
    :param pk: primary key of a Student
    :param lesson_pk: primary key of a Lesson
    :param test_pk: primary key of a Test
    :return:
    """
    # TODO: a professor can only see one of his students

    student = get_object_or_404(Student, pk=pk)
    student_test = get_object_or_404(TestStudent, pk=test_pk)

    return render(request, "professor/lesson/student/test/detail.haml", {
        "lesson": get_object_or_404(Lesson, pk=lesson_pk),
        "student": student,
        "student_test": student_test,
    })


def professor_correct(request):
    """The Professor assess a professor-type Questions for a Student"""
    correction = request.GET.get('correction', None)
    received_id = request.GET.get('id', None)
    list_id = received_id.split("_")
    answer_id = list_id[0]
    index_id = list_id[1]
    answer = Answer.objects.get(id=answer_id)
    result = answer.assess(index_id, int(correction))
    data = {
        "result": result,
    }
    return JsonResponse(data)


def professor_iscorrect(request):
    """Get the correction for a professor-type Questions for a Student"""
    received_id = request.GET.get('id', None)
    list_id = received_id.split("_")
    answer_id = list_id[0]
    index_id = list_id[1]
    answer = Answer.objects.get(id=answer_id)
    correction = answer.get_correction(index_id)
    data = {
        "correction": correction,
    }
    return JsonResponse(data)


def professor_rename_test(request):
    """A Professor renames an existing test"""
    received_id = request.GET.get('id', None)
    name = request.GET.get('name', None)
    test = Test.objects.get(id=received_id)
    test.name = name
    test.save()
    data = {
        "name": name,
    }
    return JsonResponse(data)


def professor_test_add_question(request):
    """The Professor add a question (Context) for a Skill in a Test"""
    received_id = request.GET.get('id', None)
    list_id = received_id.split("_")
    skill = list_id[0]
    test = list_id[1]
    exercice = Context.objects.filter(skill_id=skill)[:1].get().id

    new_test_exercice = None

    with transaction.atomic():
        new_test_exercice = TestExercice.objects.create(
            testable_online=True,
            exercice_id=exercice,
            skill_id=skill,
            test_id=test,
        )
    data = {
        "new_test_exercice_id": new_test_exercice.id,
    }
    return JsonResponse(data)


def professor_test_delete_question(request):
    """The Professor removes a question (Context) from a Test"""
    # TODO: When we remove the last question in an existing Skill, display a message to add at lest one exercice for that Skill
    test_exercice_id = request.GET.get('test_exercice_id', None)

    TestExercice.objects.get(id=test_exercice_id).delete()

    data = {

    }
    return JsonResponse(data)


def professor_test_add_skill(request):
    """The Professor add a Skill (with one Context) in a Test"""
    test_id = request.GET.get('test_id', None)
    skill_id = request.GET.get('skill_id', None)
    # Check if we add a Skill to a Test or a TestFromClass (the latter doesn't need exercices)
    if Test.objects.filter(id=test_id):
        test = Test.objects.get(id=test_id)

        # Add the Skill to the Test
        skill = Skill.objects.get(id=skill_id)
        test.skills.add(skill)

        # We have to create a TestExercice for the Skill
        # In order to do that, we search for an exercice to provide by default
        # If none exists, we will leave it blank

        # Gather exercices related to the Skill concerned
        exercices = skill.context_set.filter(approved=True, testable_online=True)

        # Gather exercices for identical Skills to the Skill concerned
        identical_to_skills = Relations.objects.filter(
            relation_type="identic_to", from_skill=skill)
        identical_from_skills = Relations.objects.filter(
            relation_type="identic_to", to_skill=skill)
        for relation in identical_to_skills:
            exercices = exercices | relation.to_skill.context_set.filter(approved=True, testable_online=True)
        for relation in identical_from_skills:
            exercices = exercices | relation.from_skill.context_set.filter(approved=True, testable_online=True)

        # If no exercice exists, we will leave it blank and the user will have to create one
        if not exercices.exists():
            if test.fully_testable_online:
                test.fully_testable_online = False
                test.save()

            # We check if an offline exercice is available instead
            exercices = skill.context_set.filter(approved=True, testable_online=False)
            for relation in identical_to_skills:
                exercices = exercices | relation.to_skill.context_set.filter(approved=True, testable_online=False)
            for relation in identical_from_skills:
                exercices = exercices | relation.from_skill.context_set.filter(approved=True, testable_online=False)

            if not exercices.exists():
                with transaction.atomic():
                    new_test_exercice = TestExercice.objects.create(
                        testable_online=False,
                        skill=skill,
                        test=test,
                    )
                data = {
                    "new_test_exercice_id": new_test_exercice.id
                }
                #GET OUT
            else:
                exercice = exercices[random.choice(range(exercices.count()))]
                with transaction.atomic():
                    new_test_exercice = TestExercice.objects.create(
                        testable_online=False,
                        exercice=exercice,
                        skill=skill,
                        test=test,
                    )
                data = {
                    "new_test_exercice_id": new_test_exercice.id
                }

        # An exercice exists
        else:
            exercice = exercices[random.choice(range(exercices.count()))]

            # We now create the TestExercice
            with transaction.atomic():
                new_test_exercice = TestExercice.objects.create(
                    testable_online=True,
                    exercice=exercice,
                    skill=skill,
                    test=test,
                )
            data = {
                "new_test_exercice_id": new_test_exercice.id
            }


    #Otherwise, if it is a TestFromClass, we don't need to add an exercice
    else:
        TestFromClass.objects.get(id=test_id).skills.add(Skill.objects.get(id=skill_id))
        data = {}

    return JsonResponse(data)


def professor_test_delete_skill(request):
    """The Professor removes a Skill from a Test, and all the Contexts attached to that Skill in the Test"""
    received_id = request.GET.get('id', None)
    list_id = received_id.split("_")
    skill_id = list_id[0]
    test_id = list_id[1]
    if Test.objects.filter(id=test_id):
        for test_exercice in Test.objects.get(id=test_id).testexercice_set.all():
            # Primary keys (id) are in integer format
            if test_exercice.skill.id == int(skill_id):
                test_exercice.delete()
        Test.objects.get(id=test_id).skills.remove(Skill.objects.get(id=skill_id))

    else:
        TestFromClass.objects.get(id=test_id).skills.remove(Skill.objects.get(id=skill_id))
    data = {
        'skill_id': skill_id,
    }
    return JsonResponse(data)


@user_is_professor
def lesson_test_list(request, pk):
    """
    Query a Lesson to display its associated tests

    :param request:
    :param pk: primary key of a Lesson
    :return:
    """
    lesson = get_object_or_404(Lesson, pk=pk)

    return render(request, "professor/lesson/test/list.haml", {
        "lesson": lesson,
        "all_tests": lesson.basetest_set.order_by('-created_at'),
    })


@user_is_professor
def lesson_test_add(request, pk):
    """
    Query a Lesson to add tests to it

    :param request:
    :param pk: primary key of a Lesson
    :return:
    """
    lesson = get_object_or_404(Lesson, pk=pk)

    return render(request, "professor/lesson/test/add.haml", {
        "lesson": lesson,
    })


@user_is_professor
def lesson_test_update(request, lesson_pk, pk):
    """
    Display a form to update a BaseTest in a Lesson

    :param request:
    :param lesson_pk: primary key of a Lesson
    :param pk: primary key of a BaseTest
    :return:
    """
    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    test = get_object_or_404(BaseTest, pk=pk)

    form = TestUpdateForm(request.POST, instance=test) if request.method == "POST" else TestUpdateForm(instance=test)

    if form.is_valid():
        form.save()
        if hasattr(test, "test"):
            return HttpResponseRedirect(reverse("professor:lesson_test_online_detail", args=(lesson.pk, test.pk,)))
        else:
            return HttpResponseRedirect(reverse("professor:lesson_test_from_class_detail", args=(lesson.pk, test.pk,)))

    return render(request, "professor/lesson/test/update.haml", {
        "lesson": lesson,
        "test": test,
        "form": form,
    })


def lesson_skill_detail(request, lesson_pk, skill_code):
    """
    Query a Lesson and a Skill to display the details of a skill

    :param request:
    :param lesson_pk: primary key of a Lesson
    :param skill_code: code of a Skill
    :return:
    """
    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    skill = get_object_or_404(Skill, code=skill_code)
    student_skills = StudentSkill.objects.filter(student__lesson=lesson, skill=skill).order_by(
        "student__user__last_name", "student__user__first_name")

    number_of_students = student_skills.count()
    number_acquired = student_skills.filter(acquired__isnull=False).count()
    number_not_acquired = student_skills.filter(acquired__isnull=True, tested__isnull=False).count()

    return render(request, "professor/lesson/skill/detail.haml", {
        "lesson": lesson,
        "skill": skill,
        "student_skills": student_skills,
        "number_of_students": number_of_students,
        "number_acquired": number_acquired,
        "number_not_acquired": number_not_acquired,
        "number_not_tested": number_of_students - number_acquired - number_not_acquired,
    })


@require_POST
@user_is_professor
def regenerate_student_password(request):
    """
    Regenerate a password for a student

    :param request:
    :return:
    """
    # TODO : TO DELETE ?
    data = json.load(request)

    student = get_object_or_404(Student, id=data["student_id"])
    new_password = student.generate_new_password()

    # TODO: a professor can only modify this for one of his students

    return HttpResponse(new_password)


def get_encoded_image(encoded_image=None):
    """
    Save the received in request base64 encoded image and return the image path to serve.
    """

    extension = str(encoded_image).split(".")[-1]
    path = default_storage.save('{file_name}.{extension}'.format(file_name=time.time().__str__(),
                                                                 extension=extension),
                                ContentFile(encoded_image.read()))
    return path


@user_is_professor
def update_pedagogical_ressources(request, type, id):
    """
    Display a form to update a Resource
    :param request:
    :param id: id of a Skill, Section or CodeR
    :param type: string containing either "skill", "section" or "coder"
    :return:
    """

    if request.method == "POST" and request.POST["form_type"] == "my_resource":
        data = {}
        data['kind'] = request.POST["type"]
        data['title'] = request.POST["title"]
        data['author'] = request.user.username
        data['comment'] = request.POST["text"]
        data['resources'] = []

        for i in filter(lambda x: x.startswith("link_name"), request.POST.keys()):
            number = i.split("_")[-1]
            resource_data = {}
            resource_data['mediaType'] = "link"
            resource_data['optionalName'] = request.POST["link_name_" + number]
            resource_data['type'] = request.POST["link_type_" + number]
            resource_data['link'] = request.POST["url_" + number]
            data['resources'].append(resource_data)

        for i in filter(lambda x: x.startswith("file_name"), request.POST.keys()):
            number = i.split("_")[-1]
            resource_data = {}
            resource_data['mediaType'] = "file"
            resource_data['optionalName'] = request.POST["file_name_" + number]
            resource_data['type'] = request.POST["file_type_" + number]
            path = get_encoded_image(request.FILES["file_" + number])
            resource_data['file'] = path
            data['resources'].append(resource_data)

        with transaction.atomic():
            new_resource = Resource.objects.create(section=request.POST['section'],
                                                   content=data,
                                                   added_by_id=request.user.id)
            if type == 'skill':
                add_to = Skill.objects.get(id=id)
            elif type == 'section':
                add_to = Section.objects.get(id=id)
            elif type == 'coder':
                add_to = CodeR.objects.get(id=id)
            add_to.resource.add(new_resource)

    elif request.method == "POST" and request.POST["form_type"] == "lesson_khanacademy":
        slug = request.POST["url"].split("/v/")[1]
        if KhanAcademy.objects.filter(slug=slug):
            my_khanacademy_resource = KhanAcademy.objects.get(slug=slug)
        else:
            print("La ressource n'existe pas ...")
        existing_resources = Resource.objects.filter(section=request.POST['section'])
        exist = False
        for res in existing_resources:
            if res.content.get('from') == "skills_khanacademyvideoskill":
                if res.content['referenced'] == my_khanacademy_resource.id:
                    new_resource = res
                    exist = True

        with transaction.atomic():
            if not exist:
                data = {}
                data['from'] = "skills_khanacademyvideoskill"
                data['referenced'] = my_khanacademy_resource.id
                new_resource = Resource.objects.create(section=request.POST['section'], content=data,
                                                       added_by_id=request.user.id)

            if type == 'skill':
                add_to = Skill.objects.get(id=id)
            elif type == 'section':
                add_to = Section.objects.get(id=id)
            elif type == 'coder':
                add_to = CodeR.objects.get(id=id)
            add_to.resource.add(new_resource)

    elif request.method == "POST" and request.POST["form_type"] == "sesamath_reference":
        # TODO Adapter les templates pour minimiser les fichiers utilisés (voir code précédent)

        my_sesamath_resource = get_object_or_404(Sesamath, pk=request.POST['ref_pk'])
        existing_resources = Resource.objects.filter(section=None)
        exist = False
        for res in existing_resources:
            if res.content['from'] == "skills_sesamathskill":
                if res.content['referenced'] == my_sesamath_resource.id:
                    new_resource = res
                    exist = True
        with transaction.atomic():
            if not exist:
                data = {'from': "skills_sesamathskill", 'referenced': my_sesamath_resource.id}
                new_resource = Resource.objects.create(section=request.POST['section'], content=data,
                                                       added_by_id=request.user.id)
            if type == 'skill':
                add_to = Skill.objects.get(id=id)
            elif type == 'section':
                add_to = Section.objects.get(id=id)
            elif type == 'coder':
                add_to = CodeR.objects.get(id=id)
            add_to.resource.add(new_resource)

    if type == 'skill':
        base = get_object_or_404(Skill, id=id)
    elif type == 'section':
        base = get_object_or_404(Section, id=id)
    else:
        # type == 'coder'
        base = get_object_or_404(CodeR, id=id)

    resource_form = ResourceForm()
    KhanAcademy_form = KhanAcademyForm()
    Sesamath_form = SesamathForm()

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
        "resource_form": resource_form,
        "KhanAcademy_form": KhanAcademy_form,
        "sesamath_reference_form": Sesamath_form,
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

    # TODO : TO DELETE
    """
    resource_form = ResourceForm()
    KhanAcademy_form =  KhanAcademyForm()

    personal_resource = skill.resource.filter(added_by_id=request.user,section="personal_resource")
    other_resource = skill.resource.filter(added_by_id=request.user, section="other_resource")
    exercice_resource = skill.resource.filter(added_by_id=request.user, section="exercice_resource")
    lesson_resource = skill.resource.filter(added_by_id=request.user, section="lesson_resource")

    if request.method == "GET":
        return render(request, "professor/skill/update_pedagogical_resources.haml", {
            "resource_form": resource_form,
            "khanacademy_skill_form": khanacademy_skill_form,
            "khanacademy_references": khanacademy_references,
            "sesamath_reference_form": sesamath_reference_form,
            "sesamath_references_manuals": sesamath_references_manuals,
            "sesamath_references_cahiers": sesamath_references_cahiers,
            "synthese_form": synthese_form,
            "personal_resource": personal_resource,
            "object": skill,
        })

    assert request.method == "POST"

    assert int(request.POST["added_by"]) == request.user.pk

    if request.POST["form_type"] in ("personal_resource", "lesson_resource", "exercice_resource", "other_resource"):
        with transaction.atomic():
            resource_form = ResourceForm(request.POST, request.FILES)

            if resource_form.is_valid():
                resource = resource_form.save()

                if not resource.author:
                    resource.author = unicode(request.user.professor)
                    resource.save()

                for i in filter(lambda x: x.startswith("link_link_"), request.POST.keys()):
                    number = i.split("_")[-1]
                    link = request.POST["link_link_" + number]
                    title = request.POST["link_title_" + number]
                    if not title:
                        try:
                            b = mechanize.Browser()
                            b.open(link)
                            title = b.title()
                        except Exception as e:
                            import traceback
                            traceback.print_exc(file=sys.stdout)
                            print e
                            print "Fail to get title for %s" % link

                    rlf = ResourceForm({
                        "resource": resource.pk,
                        "link": link,
                        "title": force_encoding(title),
                        "kind": request.POST["link_kind_" + number],
                        "added_by": request.user.pk,
                    })

                    if rlf.is_valid():
                        rlf.save()
                    else:
                        raise Exception("Resource Link is unvalid: %s" % rlf.errors)

                for i in filter(lambda x: x.startswith("file_file_"), request.FILES.keys()):
                    number = i.split("_")[-1]
                    rff = ResourceForm({
                        "resource": resource.pk,
                        "title": force_encoding(request.POST["file_title_" + number]),
                        "kind": request.POST["file_kind_" + number],
                        "added_by": request.user.pk,
                    },{
                        "file": request.FILES["file_file_" + number],
                    })

                    if rff.is_valid():
                        rff.save()
                    else:
                        raise Exception("Resource Link is unvalid: %s" % rff.errors)

                return HttpResponseRedirect(reverse('professor:skill_update_pedagogical_ressources', args=(skill.code,)))

            else:
                print resource_form.errors

    elif request.POST["form_type"] == "khanacademy_skill":
        khanacademy_skill_form = KhanAcademyForm(request.POST)

        if khanacademy_skill_form.is_valid():
            ref = khanacademy_skill_form.reference
            KhanAcademy.objects.create(
                youtube_id=ref.youtube_id,
                url="https://fr.khanacademy.org/v/%s" % ref.slug,
                skill=skill,
                added_by=request.user,
                reference=ref,
            )
            return HttpResponseRedirect(reverse('professor:skill_update_pedagogical_ressources', args=(skill.code,)))

    elif request.POST["form_type"] == "sesamath_reference":
        sesamath_reference_form = SesamathForm(request.POST)

        if sesamath_reference_form.is_valid():
            ref = Sesamath.objects.get(id=sesamath_reference_form.cleaned_data["ref_pk"])
            Sesamath.objects.create(
                skill=skill,
                reference=ref,
                added_by=request.user,
            )
            return HttpResponseRedirect(reverse('professor:skill_update_pedagogical_ressources', args=(skill.code,)))

    elif request.POST["form_type"] == "synthese_form":
        synthese_form = SyntheseForm(request.POST)
        if synthese_form.is_valid():
            skill.oscar_synthese = synthese_form.cleaned_data["synthese"]
            skill.modified_by = request.user
            skill.save()
            return HttpResponseRedirect(reverse('professor:skill_update_pedagogical_ressources', args=(skill.code,)))

    return render(request, "professor/skill/update_pedagogical_resources.haml", {
        "resource_form": resource_form,
        "khanacademy_skill_form": khanacademy_skill_form,
        "khanacademy_references": khanacademy_references,
        "sesamath_reference_form": sesamath_reference_form,
        "sesamath_references_manuals": sesamath_references_manuals,
        "sesamath_references_cahiers": sesamath_references_cahiers,
        "synthese_form": synthese_form,
        "personal_resource": personal_resource,
        "object": skill,
    })
    """


@user_is_professor
def remove_pedagogical_ressources(request, type, id_type, kind, id):
    """
    Remove a Sesamath, KhanAcademy or Resource object
    :param request:
    :param type: contains "skill", "section" or "coder"
    :param id_type: id of Skill, Section or CodeR
    :param kind: value equal either to "sesamath", "khanAcademy" or "resource"
    :param id: id of a Resource
    :return:
    """
    if not Resource.objects.filter(id=id):
        print "The resource doesn't exist (kind : %s, id : %s)" % (kind, id)
        return HttpResponseBadRequest()

    object = Resource.objects.get(id=id)
    if type == 'skill':
        base = Skill.objects.get(resource=id)
    elif type == 'section':
        base = Section.objects.get(resource=id)
    elif type == 'coder':
        base = CodeR.objects.get(resource=id)
    else:
        print("The type given (%s)does not exist", type)

    # We delete the relation with the resource
    base.resource.remove(object)

    # If it's a "personal" resource (i.e. not a sesamath or khanacademy resource), we should also delete it from
    # Resource table, since a "personal" resource can not be used by other skill/section/coder's
    # We do not delete the other types of resources because they could be used by another skill (unlike personal resources)
    if kind == 'resource':
        object.delete()
    return HttpResponseRedirect(reverse("professor:update_pedagogical_ressources", args=(type, id_type)))


@require_POST
@user_is_professor
def validate_student_skill(request, lesson_pk, student_skill):
    """
    Validate a Skill for a Student

    :param request:
    :param lesson_pk: primary key of a Lesson
    :param student_skill: id of a StudentSkill
    :return:
    """
    # TODO: a professor can only do this on one of his students
    lesson = get_object_or_404(Lesson, pk=lesson_pk)

    student_skill = get_object_or_404(StudentSkill, id=student_skill)

    student_skill.validate(
        who=request.user,
        reason="À la main par le professeur.",
        reason_object=lesson,
    )

    return HttpResponseRedirect(
        reverse('professor:lesson_student_detail', args=(lesson.pk, student_skill.student.id,)) + "#heatmap")


@require_POST
@user_is_professor
def unvalidate_student_skill(request, lesson_pk, student_skill):
    """
    Invalidate a Skill for a Student

    :param request:
    :param lesson_pk: primary key of a Lesson
    :param student_skill: id of a StudentSkill
    :return:
    """
    # TODO: a professor can only do this on one of his students
    lesson = get_object_or_404(Lesson, pk=lesson_pk)

    student_skill = get_object_or_404(StudentSkill, id=student_skill)

    student_skill.unvalidate(
        who=request.user,
        reason="À la main par le professeur.",
        reason_object=lesson,
    )

    return HttpResponseRedirect(
        reverse('professor:lesson_student_detail', args=(lesson.pk, student_skill.student.id,)) + "#heatmap")


@require_POST
@user_is_professor
def default_student_skill(request, lesson_pk, student_skill):
    """
    Set a default value for a Student's Skill

    :param request:
    :param lesson_pk: primary key of a Lesson
    :param student_skill: id of a StudentSkill
    :return:
    """
    # TODO: a professor can only do this on one of his students
    lesson = get_object_or_404(Lesson, pk=lesson_pk)

    student_skill = get_object_or_404(StudentSkill, id=student_skill)

    student_skill.default(
        who=request.user,
        reason="À la main par le professeur.",
        reason_object=lesson,
    )

    return HttpResponseRedirect(
        reverse('professor:lesson_student_detail', args=(lesson.pk, student_skill.student.id,)) + "#heatmap")


@user_is_professor
def lesson_tests_and_skills(request, lesson_id):
    """

    :param request:
    :param lesson_id: id of a Lesson
    :return:
    """
    # TODO: a professor can only see one of his lesson

    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.user.professor not in lesson.professors.all():
        raise PermissionDenied()

    stages = {}

    for stage in lesson.stages_in_unchronological_order():
        stages[stage.id] = [x for x in stage.skills.all().values("id", "code", "name").order_by("-code")]

    return HttpResponse(json.dumps({
        "stages": stages,
    }, indent=4))


@user_is_professor
def exercice_list(request):
    return render(request, 'professor/exercice/list.haml', {
        "exercice_list": Context.objects.select_related('skill').order_by("skill__stage__level", "skill__code", "id"),
        # All the skills without any existing context
        # We use context with lower case to indicate the table Context that refers to Skills
        "skills_without_exercices": Skill.objects.filter(context__isnull=True).order_by("stage__level", "-code", "id"),
    })


@user_is_professor
def exercice_to_approve_list(request):
    return render(request, 'professor/exercice/list_to_approve.haml', {
        "exercice_list": Context.objects.filter(approved=False).select_related('skill'),
    })


# @require_POST
@user_is_professor
def students_password_page(request, pk):
    """
    Regenerate a code for every student of a lesson (to allow him/her to create a new password)
    """
    lesson = get_object_or_404(Lesson, pk=pk)

    students = []

    with transaction.atomic():
        for student in lesson.students.all():
            students.append({
                "last_name": student.user.last_name,
                "first_name": student.user.first_name,
                "username": student.user.username,
                "password": student.generate_new_code(),
            })

    return render(request, "professor/lesson/student/password_page.haml", {
        "students": students
    })


@user_is_professor
def single_student_password_page(request, lesson_pk, student_pk):
    """
    Regenerate a code for a student (to allow him/her to create a new password)
    """

    students = []

    with transaction.atomic():
        student = get_object_or_404(Student, pk=student_pk)
        students.append({
            "last_name": student.user.last_name,
            "first_name": student.user.first_name,
            "username": student.user.username,
            "password": student.generate_new_code(),
        })

    return render(request, "professor/lesson/student/password_page.haml", {
        "students": students
    })


@require_POST
@user_is_professor
def exercice_validation_form_validate_exercice(request):
    data = json.loads(request.read())

    questions = OrderedDict()
    for question in data["questions"]:
        if question["type"] == "text":
            questions[question["instructions"]] = {
                "type": question["type"],
                "answers": [x["text"] for x in question["answers"]],
            }

        elif question["type"].startswith("math"):
            questions[question["instructions"]] = {
                "type": question["type"],
                "answers": [x["latex"] for x in question["answers"] if x.get("latex")],
            }

        elif question["type"] == "graph":
            questions[question["instructions"]] = {
                "type": question["type"],
                "answers": question["answers"],
            }

        # No provided answer if corrected by a Professor
        elif question["type"] == "professor":
            questions[question["instructions"]] = {
                "type": question["type"],
                "answers": "",
            }

        elif question["type"] == "fill-text-blanks":
            temp = re.split(r'#\[\d+\]#',question["instructions"])

            i = 0
            for ans in question["answers"]:
                if i == len(temp)-2:
                    ans["text"] = [temp[i],temp[i+1]]
                else:
                    ans["text"] = [temp[i],""]
                i += 1

            questions[question["instructions"]] = {
                "type": question["type"],
                "answers": question["answers"],
            }
        elif question["type"] == "fill-table-blanks":

            i = 0
            new_table = []
            for row in question["table"]:
                temp = []
                for cell in row:
                    closed_list = {}
                    closed_list["index"]=i
                    closed_list["text"]=cell
                    if re.match(r'#\[\d+\]#',cell) is not None:
                        closed_list["blank"]=question["answers"][i]
                        i+=1
                    temp.append(closed_list)
                new_table.append(temp)

            question["table"] = new_table

            questions[question["instructions"]] = {
                "type": question["type"],
                "table": question["table"],
                "answers": question["answers"],
            }
        else:
            answers = OrderedDict()
            for x in question["answers"]:
                answers[x["text"]] = x["correct"]

            questions[question["instructions"]] = {
                "type": question["type"],
                "answers": answers,
            }

    if data["testable_online"]:
        result = validate_exercice_yaml_structure(questions)
    else:
        result = True

    if result is not True:
        return HttpResponse(json.dumps({
            "yaml": {
                "result": "error",
                "message": result,
            }
        }, indent=4), content_type="application/json")

    rendering = render(request, "professor/exercice/exercice_rendering.haml", {
        "content": "",
        "questions": questions,
    })

    return HttpResponse(json.dumps({
        "yaml": {
            "result": "success",
            "message": "L'exercice semble valide",
        },
        "rendering": rendering.content,
    }, indent=4), content_type="application/json")


@require_POST
@user_is_professor
def exercice_validation_form_submit(request, pk=None):
    data = json.load(request)
    html = data["html"]
    skill_code = data["skill_code"]
    image = None
    testable_online = data["testable_online"]

    if pk is not None:
        exercice = get_object_or_404(Context, pk=pk)
    else:
        exercice = None


    if data.get("image"):
        exercices_folder = os.path.join(settings.MEDIA_ROOT, "exercices")
        if not os.path.exists(exercices_folder):
            os.makedirs(exercices_folder)

        existing_images = {x for x in os.listdir(os.path.join(settings.BASE_DIR, "exercices"))}
        existing_images = existing_images.union({x for x in os.listdir(exercices_folder)})

        image_extension, image = data["image"].split(",", 1)

        image_extension = image_extension.split("/")[1].split(";")[0]

        for i in range(1, 1000):
            name = ("%s_%.2d.%s" % (skill_code, i, image_extension)).upper()
            if name not in existing_images:
                break
        else:
            raise Exception()

        if html:
            html = ('<img src="%sexercices/%s" class="img-responsive" />\n' % (settings.MEDIA_URL, name)) + html
        else:
            html = '<img src="%sexercices/%s" class="img-responsive" />\n' % (settings.MEDIA_URL, name)

        assert not os.path.exists(os.path.join(exercices_folder, name))
        open(os.path.join(exercices_folder, name), "w").write(b64decode(image))

    # First, Context creation
    with transaction.atomic():
        if exercice is not None:
            exercice.skill = Skill.objects.get(code=skill_code)
            exercice.context = html
            exercice.testable_online = testable_online
            exercice.save()
        else:
            exercice = Context.objects.create(
                file_name="submitted",
                skill=Skill.objects.get(code=skill_code),
                context=html,
                testable_online=testable_online,
                added_by=request.user,
            )
    # Now, delete all Questions and their links in the Context
    # To avoid duplicated Questions
    for q in exercice.get_questions():
        q.delete()
    for list_question in List_question.objects.filter(context=exercice.id):
        list_question.delete()

    # Then, Question(s) creation, and links in List_question with the Context created
    if testable_online:
        for question in data["questions"]:
            new_question_answers = None

            if question["type"] == "text":
                new_question_answers = {
                    "type": question["type"],
                    "answers": [x["text"] for x in question["answers"]],
                }
            elif question["type"] == "fill-text-blanks":
                temp = re.split(r'#\[\d+\]#',question["instructions"])

                i = 0
                for ans in question["answers"]:
                    if i == len(temp)-2:
                        ans["text"] = [temp[i],temp[i+1]]
                    else:
                        ans["text"] = [temp[i],""]
                    i += 1

                new_question_answers = {
                    "type": question["type"],
                    "answers": [x for x in question["answers"]],
                }
            elif question["type"] == "fill-table-blanks":

                i = 0
                new_table = []
                for row in question["table"]:
                    temp = []
                    for cell in row:
                        closed_list = {}
                        closed_list["index"]=i
                        closed_list["text"]=cell
                        if re.match(r'#\[\d+\]#',cell) is not None:
                            closed_list["blank"]=question["answers"][i]
                            i+=1
                        temp.append(closed_list)
                    new_table.append(temp)

                question["table"] = new_table

                new_question_answers = {
                    "type": question["type"],
                    "table": question["table"],
                    "answers": [x for x in question["answers"]],
                }
            elif question["type"].startswith("math"):
                new_question_answers = {
                    "type": question["type"],
                    "answers": [x["latex"] for x in question["answers"] if x.get("latex")],
                }

            elif question["type"] == "graph":
                answers = []

                for answer in question["answers"]:
                    if "latex" in answer:
                        del answer["latex"]
                    if "correct" in answer:
                        del answer["correct"]
                    if "text" in answer:
                        del answer["text"]
                    answers.append(answer)

                new_question_answers = {
                    "type": question["type"],
                    "answers": question["answers"],
                }

            elif question["type"] == "professor":
                new_question_answers = {
                    "type": question["type"],
                    "answers": "",
                }

            else:
                answers = CommentedMap()
                for i in question["answers"]:
                    answers[i["text"]] = i["correct"]

                new_question_answers = {
                    "type": question["type"],
                    "answers": answers,
                }
            yaml_file = ruamel.yaml.round_trip_dump(new_question_answers)

            # Add all the Questions in the Context (even the ones not modified)
            # We deleted all the Questions and their links to this Context earlier
            with transaction.atomic():
                new_question = Question.objects.create(
                    description=question["instructions"],
                    answer=yaml_file,
                    source=question["source"],
                    indication=question["indication"],
                )

            with transaction.atomic():
                link = List_question.objects.create(
                    context_id=exercice.id,
                    question_id=new_question.id,
                )



    return HttpResponse(json.dumps({
        "url": reverse('professor:exercice_detail', args=(exercice.id,)),
        "id": exercice.id,
    }))


@require_POST
@user_is_professor
def exercice_validation_form_validate_exercice_yaml(request):
    try:
        data = json.loads(request.read())
        yaml.safe_load(data["yaml"])
        exercice = yaml.load(data["yaml"], Loader=yamlordereddictloader.Loader)
    except Exception as e:
        return HttpResponse(json.dumps({
            "yaml": {
                "result": "error",
                "message": "Le format yaml n'est pas respecté: %s" % e,
            }
        }, indent=4), content_type="application/json")

    result = validate_exercice_yaml_structure(exercice)

    if result is not True:
        return HttpResponse(json.dumps({
            "yaml": {
                "result": "error",
                "message": result,
            }
        }, indent=4), content_type="application/json")

    rendering = render(request, "professor/exercice/exercice_rendering.haml", {
        "content": "",
        "questions": exercice,
    })

    return HttpResponse(json.dumps({
        "yaml": {
            "result": "success",
            "message": "L'exercice semble valide",
        },
        "rendering": rendering.content,
    }, indent=4), content_type="application/json")


@user_is_professor
def exercice_test(request, pk):
    exercice = get_object_or_404(Context, pk=pk)

    if request.method == "GET":
        return render(request, "professor/exercice/test.haml", {
            "exercice": exercice,
            "object": exercice,
        })

    assert request.method == "POST"

    return render(request, "professor/exercice/test.haml", {
        "exercice": exercice,
        "object": exercice,
        "checked_answers": exercice.check_answers(request.POST),
        "raw_answers": request.POST,
    })


@user_is_professor
def exercice_update(request, pk):
    exercice = get_object_or_404(Context, pk=pk)

    if exercice.added_by != request.user and not request.user.is_superuser:
        return redirect_to_login(request.get_full_path(), resolve_url(settings.LOGIN_URL), REDIRECT_FIELD_NAME)

    return render(request, "professor/exercice/validation_form.haml", {
        "exercice": exercice,
        "object": exercice,
        "stage_list": Stage.objects.all(),
    })


@user_is_professor
def exercice_update_json(request, pk):
    """

    :param request:
    :param pk: primary key of a Context
    :return:
    """
    context = get_object_or_404(Context, pk=pk)

    if context.added_by != request.user and not request.user.is_superuser:
        return redirect_to_login(request.get_full_path(), resolve_url(settings.LOGIN_URL), REDIRECT_FIELD_NAME)

    questions = []
    # TODO Create a type field in Question (stored with the answers for the time being)
    for question in context.get_questions():
        # Each question has a answer field, which is a text formatted with YAML,
        # containing a type and its (true/false) answers attached to it
        question_type = question.get_answer()["type"]
        answers = None

        if question_type == "graph":
            answers = question.get_answer()["answers"]
        elif question_type == "professor":
            answers = ""
        elif isinstance(question.get_answer()["answers"], list):
            answers = [{"text": key, "correct": True} for key in question.get_answer()["answers"]]
        else:  # assuming dict
            answers = [{"text": key, "correct": value} for key, value in question.get_answer()["answers"].items()]

        questions.append({
            "instructions": question.description,
            "type": question_type,
            "answers": answers,
            "source": question.source,
            "indication": question.indication,
        })

    return HttpResponse(json.dumps({
        "skillCode": context.skill.code,
        "html": context.context,
        "questions": questions,
    }))


@user_is_professor
def exercice_for_test_exercice(request, exercice_pk, test_exercice_pk):
    """
    Add an exercice for a test
    :param request:
    :param exercice_pk: primary key of an exercice
    :param test_exercice_pk: primary key of a TestExercice
    :return:
    """
    exercice = get_object_or_404(Context, pk=exercice_pk)
    test_exercice = get_object_or_404(TestExercice, pk=test_exercice_pk)

    assert test_exercice.test.can_change_exercice() or not test_exercice.exercice, "Can't write an exercice if the test has started or that the test exercice already has an exercice"

    with transaction.atomic():
        test_exercice.exercice = exercice
        if exercice.testable_online:
            test_exercice.testable_online = True
            test_exercice.test.fully_testable_online = True
        test_exercice.save()

    return HttpResponseRedirect(reverse('professor:lesson_test_online_exercices', args=(
    test_exercice.test.lesson.pk, test_exercice.test.pk,)) + "#%s" % test_exercice_pk)


@user_is_professor
def exercice_adapt_test_exercice(request, test_exercice_pk):
    """

    :param request:
    :param test_exercice_pk: primary key of a TestExercice
    :return:
    """
    test_exercice = get_object_or_404(TestExercice, pk=test_exercice_pk)
    exercice = test_exercice.exercice
    new_exercice = None

    # user shouldn't end up there in that situation but we never know
    if exercice is None:
        return HttpResponseRedirect(reverse('professor:exercice_validation_form') + "#?for_test_exercice=%s&code=%s" % (
        test_exercice_pk, test_exercice.skill))

    assert test_exercice.test.can_change_exercice(), "Can't change an exercice if the test has started"

    with transaction.atomic():
        new_exercice = Context.objects.create(
            file_name="adapted",
            context=exercice.context,
            skill=exercice.skill,
            testable_online=exercice.testable_online,
            approved=exercice.approved,
            added_by=request.user,
        )

    questions = exercice.get_questions()

    for question in questions:
        with transaction.atomic():
            link = List_question.objects.create(
                context_id=new_exercice.id,
                question_id=question.id,
            )

    return HttpResponseRedirect(
        reverse('professor:exercice_update', args=(new_exercice.id,)) + "#?for_test_exercice=%s&code=%s" % (
        test_exercice_pk, exercice.skill.code))


@user_is_professor
def exercice_remove_test_exercice(request, test_exercice_pk):
    """Removes an exercice (TestExercice) from a Test

    :param request:
    :param test_exercice_pk: primary key of a TestExercice
    :return:
    """
    test_exercice = get_object_or_404(TestExercice, pk=test_exercice_pk)
    lesson_pk = test_exercice.pk
    test_pk = test_exercice.pk
    test_exercice.delete()

    return HttpResponseRedirect(reverse('professor:lesson_test_online_exercices', args=(
        lesson_pk, test_pk,)))


@user_is_professor
def contribute_page(request):
    """
    Display a ResourceForm or submit it

    :param request:
    :return:
    """
    data = {x.short_name: x for x in Stage.objects.all()}

    if request.method == "POST":
        form = ResourceForm(request.POST, request.FILES)
    else:
        form = ResourceForm()

    data["form"] = form
    data["global_resources"] = Resource.objects.all()
    data["code_r"] = CodeR.objects.all()

    if request.method == "POST" and form.is_valid():
        gr = form.save()
        gr.added_by = request.user
        gr.save()
        return HttpResponseRedirect(reverse("professor:main-education") + "#global_resources")

    return render(request, "professor/skill/list.haml", data)


def global_resources_delete(request, pk):
    """
    Delete a Resource

    :param request:
    :param pk: primary key of a Resource
    :return:
    """
    gr = get_object_or_404(Resource, pk=pk)

    if request.user != gr.added_by:
        raise PermissionDenied()

    gr.delete()

    return HttpResponseRedirect(reverse("professor:main-education") + "#global_resources")


def main_education(request):
    return render(request, "professor/skill/main-education.haml")


def socles_competence(request):
    data = {x.short_name: x for x in Stage.objects.all()}

    data["global_resources"] = Resource.objects.all()
    data["code_r"] = CodeR.objects.all().order_by('id')

    return render(request, "professor/skill/new-list-socles.haml", data)


def enseign_pro(request):
    data = {x.short_name: x for x in Stage.objects.all()}

    data["global_resources"] = Resource.objects.all()
    data["code_r"] = CodeR.objects.all().order_by('id')

    return render(request, "professor/skill/new-list-pro.haml", data)


def enseign_techart(request):
    data = {x.short_name: x for x in Stage.objects.all()}

    data["global_resources"] = Resource.objects.all()
    data["code_r"] = CodeR.objects.all().order_by('id')

    return render(request, "professor/skill/new-list-techart.haml", data)


def enseign_trans(request):
    data = {x.short_name: x for x in Stage.objects.all()}

    data["global_resources"] = Resource.objects.all()
    data["code_r"] = CodeR.objects.all().order_by('id')
    data["section"] = Section.objects.all()
    return render(request, "professor/skill/new-list-trans.haml", data)
