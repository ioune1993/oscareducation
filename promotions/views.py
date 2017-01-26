# encoding: utf-8

import os
import sys
import json
import traceback

import yaml
import ruamel.yaml
import mechanize
import yamlordereddictloader

from ruamel.yaml.comments import CommentedMap

from base64 import b64decode
from collections import OrderedDict

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, resolve_url
from django.core.urlresolvers import reverse
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.views.decorators.http import require_POST
from django.db import transaction
from django.db.models import Count

from skills.models import Skill, StudentSkill, KhanAcademyVideoReference, KhanAcademyVideoSkill, SesamathSkill, SesamathReference, VideoSkill, ExerciceSkill, ExternalLinkSkill, GlobalResources, Resource, CodeR
from examinations.models import Test, TestStudent, Exercice, BaseTest
from examinations.utils import validate_exercice_yaml_structure

from .models import Lesson, Student, Stage
from .forms import LessonForm, StudentAddForm, SyntheseForm, KhanAcademyVideoReferenceForm, StudentUpdateForm, LessonUpdateForm, TestUpdateForm, SesamathReferenceForm, GlobalResourcesForm, ResourceForm, ResourceLinkForm, ResourceFileForm
from .utils import generate_random_password, user_is_professor


@user_is_professor
def dashboard(request):
    return render(request, "professor/dashboard.haml", {
        "lessons": Lesson.objects.filter(professors=request.user.professor).annotate(Count("students")).select_related("stage"),
    })


@user_is_professor
def lesson_detail(request, pk):
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
    form = LessonForm(request.POST) if request.method == "POST" else LessonForm()

    if form.is_valid():
        lesson = form.save()
        lesson.professors.add(request.user.professor)
        return HttpResponseRedirect(reverse("professor:lesson_student_add", args=(lesson.pk,)))

    return render(request, "professor/lesson/create.haml", {
        "form": form,
    })


@user_is_professor
def lesson_update(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    form = LessonUpdateForm(request.POST, instance=lesson) if request.method == "POST" else LessonUpdateForm(instance=lesson)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("professor:lesson_detail", args=(lesson.pk,)))

    return render(request, "professor/lesson/update.haml", {
        "lesson": lesson,
        "form": form,
    })


@user_is_professor
def lesson_student_add(request, pk):

    lesson = get_object_or_404(Lesson, pk=pk)

    # TODO: a professor can only see one of his lesson

    if request.method == "POST":
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
    # TODO: a professor can only see one of his students

    student = get_object_or_404(Student, pk=pk)

    return render(request, "professor/lesson/student/detail.haml", {
        "lesson": get_object_or_404(Lesson, pk=lesson_pk),
        "student": student,
    })


@user_is_professor
def lesson_student_update(request, lesson_pk, pk):
    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    student = get_object_or_404(Student, pk=pk)

    form = StudentUpdateForm(request.POST, instance=student.user) if request.method == "POST" else StudentUpdateForm(instance=student.user)

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
    # TODO: a professor can only see one of his students

    student = get_object_or_404(Student, pk=pk)
    student_test = get_object_or_404(TestStudent, pk=test_pk)

    return render(request, "professor/lesson/student/test/detail.haml", {
        "lesson": get_object_or_404(Lesson, pk=lesson_pk),
        "student": student,
        "student_test": student_test,
    })


@user_is_professor
def lesson_test_list(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    return render(request, "professor/lesson/test/list.haml", {
        "lesson": lesson,
        "all_tests": lesson.basetest_set.order_by('-created_at'),
    })


@user_is_professor
def lesson_test_add(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    return render(request, "professor/lesson/test/add.haml", {
        "lesson": lesson,
    })


@user_is_professor
def lesson_test_update(request, lesson_pk, pk):
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
    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    skill = get_object_or_404(Skill, code=skill_code)
    student_skills = StudentSkill.objects.filter(student__lesson=lesson, skill=skill).order_by("student__user__last_name", "student__user__first_name")

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
    data = json.load(request)

    student = get_object_or_404(Student, id=data["student_id"])
    new_password = student.generate_new_password()

    # TODO: a professor can only modify this for one of his students

    return HttpResponse(new_password)


@user_is_professor
def update_pedagogical_ressources(request, slug):
    skill = get_object_or_404(Skill, code=slug)

    resource_form = ResourceForm()

    personal_resource = Resource.objects.filter(added_by=request.user, section="personal_resource", skill=skill)

    khanacademy_skill_form = KhanAcademyVideoReferenceForm()
    sesamath_reference_form = SesamathReferenceForm()
    synthese_form = SyntheseForm()

    khanacademy_references = KhanAcademyVideoReference.objects.all()

    sesamath_references_manuals = SesamathReference.objects.filter(ressource_kind__iexact="manuel")
    sesamath_references_cahiers = SesamathReference.objects.filter(ressource_kind__iexact="cahier")

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

                    rlf = ResourceLinkForm({
                        "resource": resource.pk,
                        "link": link,
                        "title": title,
                        "kind": request.POST["link_kind_" + number],
                        "added_by": request.user.pk,
                    })

                    if rlf.is_valid():
                        rlf.save()
                    else:
                        raise Exception("Resource Link is unvalid: %s" % rlf.errors)

                for i in filter(lambda x: x.startswith("file_file_"), request.FILES.keys()):
                    number = i.split("_")[-1]
                    rff = ResourceFileForm({
                        "resource": resource.pk,
                        "title": request.POST["file_title_" + number],
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
        khanacademy_skill_form = KhanAcademyVideoReferenceForm(request.POST)

        if khanacademy_skill_form.is_valid():
            ref = khanacademy_skill_form.reference
            KhanAcademyVideoSkill.objects.create(
                youtube_id=ref.youtube_id,
                url="https://fr.khanacademy.org/v/%s" % ref.slug,
                skill=skill,
                added_by=request.user,
                reference=ref,
            )
            return HttpResponseRedirect(reverse('professor:skill_update_pedagogical_ressources', args=(skill.code,)))

    elif request.POST["form_type"] == "sesamath_reference":
        sesamath_reference_form = SesamathReferenceForm(request.POST)

        if sesamath_reference_form.is_valid():
            ref = SesamathReference.objects.get(id=sesamath_reference_form.cleaned_data["ref_pk"])
            SesamathSkill.objects.create(
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


@user_is_professor
def remove_pedagogical_ressources(request, kind, id):
    kind_to_model = {
        "video": VideoSkill,
        "sesamath": SesamathSkill,
        "khanacademy": KhanAcademyVideoSkill,
        "exercice": ExerciceSkill,
        "external_link": ExternalLinkSkill,
        "resource": Resource,
    }

    if kind not in kind_to_model:
        print "kind not in models list"
        return HttpResponseBadRequest()

    model = kind_to_model[kind]

    if not model.objects.filter(id=id):
        print "object doesn't exist in db for %s:%s" % (kind, id)
        return HttpResponseBadRequest()

    object = model.objects.get(id=id)

    if object.added_by != request.user:
        print "'%s' didn't added '%s', '%s' did" % (request.user, object, object.added_by)
        return HttpResponseForbidden()

    skill = object.skill

    object.delete()

    return HttpResponseRedirect(reverse("professor:skill_update_pedagogical_ressources", args=(skill.code,)))


@require_POST
@user_is_professor
def validate_student_skill(request, lesson_pk, student_skill):
    # TODO: a professor can only do this on one of his students
    lesson = get_object_or_404(Lesson, pk=lesson_pk)

    student_skill = get_object_or_404(StudentSkill, id=student_skill)

    student_skill.validate(
        who=request.user,
        reason="À la main par le professeur.",
        reason_object=lesson,
    )

    return HttpResponseRedirect(reverse('professor:lesson_student_detail', args=(lesson.pk, student_skill.student.id,)) + "#skills")


@require_POST
@user_is_professor
def unvalidate_student_skill(request, lesson_pk, student_skill):
    # TODO: a professor can only do this on one of his students
    lesson = get_object_or_404(Lesson, pk=lesson_pk)

    student_skill = get_object_or_404(StudentSkill, id=student_skill)

    student_skill.unvalidate(
        who=request.user,
        reason="À la main par le professeur.",
        reason_object=lesson,
    )

    return HttpResponseRedirect(reverse('professor:lesson_student_detail', args=(lesson.pk, student_skill.student.id,)) + "#skills")


@require_POST
@user_is_professor
def default_student_skill(request, lesson_pk, student_skill):
    # TODO: a professor can only do this on one of his students
    lesson = get_object_or_404(Lesson, pk=lesson_pk)

    student_skill = get_object_or_404(StudentSkill, id=student_skill)

    student_skill.default(
        who=request.user,
        reason="À la main par le professeur.",
        reason_object=lesson,
    )

    return HttpResponseRedirect(reverse('professor:lesson_student_detail', args=(lesson.pk, student_skill.student.id,)) + "#skills")


@user_is_professor
def lesson_tests_and_skills(request, lesson_id):
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
        "exercice_list": Exercice.objects.select_related('skill').order_by("skill__stage__level", "skill__code", "id"),
        "skills_without_exercices": Skill.objects.filter(exercice__isnull=True).order_by("skill__stage__level", "-skill__code", "id"),
    })


@user_is_professor
def exercice_to_approve_list(request):
    return render(request, 'professor/exercice/list_to_approve.haml', {
        "exercice_list": Exercice.objects.filter(approved=False).select_related('skill'),
    })


# @require_POST
@user_is_professor
def students_password_page(request, pk):
    # TODO: a professor can only do this on one of his student
    lesson = get_object_or_404(Lesson, pk=pk)

    students = []

    with transaction.atomic():
        for student in lesson.students.all():
            students.append({
                "last_name": student.user.last_name,
                "first_name": student.user.first_name,
                "username": student.user.username,
                "password": student.generate_new_password(),
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
                "answers": [x["latex"] for x in question["answers"]],
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

    rendering = render(request, "examinations/exercice_rendering.haml", {
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
        exercice = get_object_or_404(Exercice, pk=pk)
    else:
        exercice = None

    if testable_online:
        questions = CommentedMap()
        for question in data["questions"]:
            if question["type"] == "text":
                questions[question["instructions"]] = {
                    "type": question["type"],
                    "answers": [x["text"] for x in question["answers"]],
                }

            elif question["type"].startswith("math"):
                questions[question["instructions"]] = {
                    "type": question["type"],
                    "answers": [x["latex"] for x in question["answers"]],
                }

            else:
                answers = CommentedMap()
                for i in question["answers"]:
                    answers[i["text"]] = i["correct"]

                questions[question["instructions"]] = {
                    "type": question["type"],
                    "answers": answers,
                }

        yaml_file = ruamel.yaml.round_trip_dump(questions)
    else:
        yaml_file = ""

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
            html = ('<img src="%sexercices/%s" />\n' % (settings.MEDIA_URL, name)) + html
        else:
            html = '<img src="%sexercices/%s" />\n' % (settings.MEDIA_URL, name)

        assert not os.path.exists(os.path.join(exercices_folder, name))
        open(os.path.join(exercices_folder, name), "w").write(b64decode(image))

    with transaction.atomic():
        if exercice is not None:
            exercice.skill = Skill.objects.get(code=skill_code)
            exercice.answer = yaml_file
            exercice.content = html
            exercice.testable_online = testable_online

            exercice.save()
        else:
            Exercice.objects.create(
                file_name="submitted",
                skill=Skill.objects.get(code=skill_code),
                answer=yaml_file,
                content=html,
                testable_online=testable_online,
                added_by=request.user,
            )

    return HttpResponse()


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

    rendering = render(request, "examinations/exercice_rendering.haml", {
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
def exercice_update(request, pk):
    exercice = get_object_or_404(Exercice, pk=pk)

    if exercice.added_by != request.user and not request.user.is_superuser:
        return redirect_to_login(request.get_full_path(), resolve_url(settings.LOGIN_URL), REDIRECT_FIELD_NAME)

    return render(request, "professor/exercice/validation_form.haml", {
        "exercice": exercice,
        "object": exercice,
        "stage_list": Stage.objects.all(),
    })


@user_is_professor
def exercice_update_json(request, pk):
    exercice = get_object_or_404(Exercice, pk=pk)

    if exercice.added_by != request.user and not request.user.is_superuser:
        return redirect_to_login(request.get_full_path(), resolve_url(settings.LOGIN_URL), REDIRECT_FIELD_NAME)

    questions = []
    for text, data in exercice.get_questions().items():
        question_type = data["type"]

        if isinstance(data["answers"], list):
            answers = [{"text": key, "correct": True} for key in data["answers"]]
        else:  # assuming dict
            answers = [{"text": key, "correct": value} for key, value in data["answers"].items()]

        questions.append({
            "instructions": text,
            "type": question_type,
            "answers": answers,
        })

    return HttpResponse(json.dumps({
        "skillCode": exercice.skill.code,
        "html": exercice.content,
        "yaml": exercice.answer,
        "questions": questions,
    }))


@user_is_professor
def contribute_page(request):
    data = {x.short_name: x for x in Stage.objects.all()}

    if request.method == "POST":
        form = GlobalResourcesForm(request.POST, request.FILES)
    else:
        form = GlobalResourcesForm()

    data["form"] = form
    data["global_resources"] = GlobalResources.objects.all()
    data["code_r"] = CodeR.objects.all()

    if request.method == "POST" and form.is_valid():
        gr = form.save()
        gr.added_by = request.user
        gr.save()
        return HttpResponseRedirect(reverse("professor:skill_list") + "#global_resources")

    return render(request, "professor/skill/list.haml", data)


def global_resources_delete(request, pk):
    gr = get_object_or_404(GlobalResources, pk=pk)

    if request.user != gr.added_by:
        raise PermissionDenied()

    gr.delete()

    return HttpResponseRedirect(reverse("professor:skill_list") + "#global_resources")
