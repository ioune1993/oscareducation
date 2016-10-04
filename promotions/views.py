# encoding: utf-8

import json
import requests

import yaml
import ruamel.yaml
import yamlordereddictloader

from ruamel.yaml.comments import CommentedMap

from datetime import datetime
from base64 import b64encode
from requests.auth import HTTPBasicAuth

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.db import transaction
from django.db.models import Count

from skills.models import Skill, StudentSkill, KhanAcademyVideoReference, KhanAcademyVideoSkill, SesamathSkill, SesamathReference
from examinations.models import Test, TestStudent, Exercice, TestFromClass, TestSkillFromClass, BaseTest
from examinations.utils import validate_exercice_yaml_structure

from .models import Lesson, Student, Stage
from .forms import LessonForm, StudentAddForm, VideoSkillForm, ExternalLinkSkillForm, ExerciceSkillForm, SyntheseForm, KhanAcademyVideoReferenceForm, StudentUpdateForm, LessonUpdateForm, TestUpdateForm, SesamathReferenceForm
from .utils import generate_random_password, user_is_professor


@user_is_professor
def dashboard(request):
    form = LessonForm(request.POST) if request.method == "POST" else LessonForm()

    if form.is_valid():
        lesson = form.save()
        lesson.professors.add(request.user.professor)
        return HttpResponseRedirect(reverse("professor:dashboard"))

    return render(request, "professor/dashboard.haml", {
        "lessons": Lesson.objects.filter(professors=request.user.professor).annotate(Count("students")),
        "add_lesson_form": form,
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


            percentage = float(mastered) / total if total else 0

            if percentage < 0.25:
                skills_to_heatmap_class[skill] = "mastered_25"
            elif percentage < 0.5:
                skills_to_heatmap_class[skill] = "mastered_50"
            elif percentage < 0.75:
                skills_to_heatmap_class[skill] = "mastered_75"
            else:
                skills_to_heatmap_class[skill] = "mastered_100"


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


@user_is_professor
def lesson_test_from_class_add(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    return render(request, "professor/lesson/test/from-class/add.haml", {
        "lesson": lesson,
        "stages": lesson.stages_in_unchronological_order(),
    })


@user_is_professor
def lesson_test_from_class_fill(request, lesson_pk, pk):
    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    test_from_class = get_object_or_404(TestFromClass, pk=pk)

    if request.method == "POST":
        second_run = []
        print request.POST.items()

        with transaction.atomic():
            for key in filter(lambda x: x.startswith(("good", "bad", "unknown")), request.POST.values()):
                result, student, skill = key.split("_", 2)
                print result, student, skill
                student = Student.objects.get(pk=student)
                skill = Skill.objects.get(pk=skill)

                test_skill_from_class, _ = TestSkillFromClass.objects.get_or_create(
                    test=test_from_class,
                    student=student,
                    skill=skill,
                )

                test_skill_from_class.result = result
                test_skill_from_class.save()

                student_skill = StudentSkill.objects.get(
                    student=student,
                    skill=skill,
                )

                if result == "god":
                    student_skill.validate()
                elif result == "bad":
                    student_skill.unvalidate()

                second_run.append([result, student_skill])

            # I redo a second run here because we can end up in a situation where
            # the teacher has enter value that would be overwritten by the
            # recursive walk and we want the resulting skills to match the teacher
            # input
            for result, student_skill in second_run:
                if result == "god":
                    student_skill.acquired = datetime.now()
                    student_skill.save()
                elif result == "bad":
                    student_skill.acquired = None
                    student_skill.tested = datetime.now()
                    student_skill.save()

        return HttpResponseRedirect(reverse('professor:lesson_test_list', args=(lesson.pk,)))

    return render(request, "professor/lesson/test/from-class/fill.haml", {
        "lesson": lesson,
        "test_from_class": test_from_class,
    })


@require_POST
@user_is_professor
def lesson_test_from_class_add_json(request):
    # TODO: a professor can only do this on one of his lesson
    # TODO: use django form

    data = json.load(request)

    lesson = get_object_or_404(Lesson, id=data["lesson"])

    if request.user.professor not in lesson.professors.all():
        raise PermissionDenied()

    with transaction.atomic():
        test = TestFromClass.objects.create(
            lesson=lesson,
            name=data["name"],
        )

        for skill_id in data["skills"]:
            test.skills.add(Skill.objects.get(code=skill_id))

        test.save()

    return HttpResponse(str(test.id))


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

    video_skill_form = VideoSkillForm()
    khanacademy_skill_form = KhanAcademyVideoReferenceForm()
    sesamath_reference_form = SesamathReferenceForm()
    exercice_skill_form = ExerciceSkillForm()
    external_link_skill_form = ExternalLinkSkillForm()
    synthese_form = SyntheseForm()

    khanacademy_references = KhanAcademyVideoReference.objects.all()
    sesamath_references = SesamathReference.objects.all()

    if request.method == "GET":
        return render(request, "professor/skill/update_pedagogical_resources.haml", {
            "video_skill_form": video_skill_form,
            "khanacademy_skill_form": khanacademy_skill_form,
            "khanacademy_references": khanacademy_references,
            "sesamath_reference_form": sesamath_reference_form,
            "sesamath_references": sesamath_references,
            "exercice_skill_form": exercice_skill_form,
            "external_link_skill_form": external_link_skill_form,
            "synthese_form": synthese_form,
            "object": skill,
        })

    assert request.method == "POST"

    if request.POST["form_type"] == "video_skill":
        video_skill_form = VideoSkillForm(request.POST)
        if video_skill_form.is_valid():
            r = video_skill_form.save()
            r.add_by = request.user
            r.save()
            return HttpResponseRedirect(reverse('professor:skill_update_pedagogical_ressources', args=(skill.code,)))

    elif request.POST["form_type"] == "khanacademy_skill":
        khanacademy_skill_form = KhanAcademyVideoReferenceForm(request.POST)

        if khanacademy_skill_form.is_valid():
            ref = KhanAcademyVideoReference.objects.get(id=khanacademy_skill_form.cleaned_data["ref_pk"])
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
            )
            return HttpResponseRedirect(reverse('professor:skill_update_pedagogical_ressources', args=(skill.code,)))

    elif request.POST["form_type"] == "exercice_skill":
        exercice_skill_form = ExerciceSkillForm(request.POST, request.FILES)
        if exercice_skill_form.is_valid():
            r = exercice_skill_form.save()
            r.add_by = request.user
            r.save()
            return HttpResponseRedirect(reverse('professor:skill_update_pedagogical_ressources', args=(skill.code,)))

    elif request.POST["form_type"] == "external_link_skill":
        external_link_skill_form = ExternalLinkSkillForm(request.POST)
        if external_link_skill_form.is_valid():
            r = external_link_skill_form.save()
            r.add_by = request.user
            r.save()
            return HttpResponseRedirect(reverse('professor:skill_update_pedagogical_ressources', args=(skill.code,)))

    elif request.POST["form_type"] == "synthese_form":
        synthese_form = SyntheseForm(request.POST)
        if synthese_form.is_valid():
            skill.oscar_synthese = synthese_form.cleaned_data["synthese"]
            skill.modified_by = request.user
            skill.save()
            return HttpResponseRedirect(reverse('professor:skill_update_pedagogical_ressources', args=(skill.code,)))

    return render(request, "professor/skill/update_pedagogical_resources.haml", {
        "video_skill_form": video_skill_form,
        "khanacademy_skill_form": khanacademy_skill_form,
        "khanacademy_references": khanacademy_references,
        "sesamath_reference_form": sesamath_reference_form,
        "sesamath_references": sesamath_references,
        "exercice_skill_form": exercice_skill_form,
        "external_link_skill_form": external_link_skill_form,
        "synthese_form": synthese_form,
        "object": skill,
    })


@require_POST
@user_is_professor
def validate_student_skill(request, lesson_pk, student_skill):
    # TODO: a professor can only do this on one of his students
    lesson = get_object_or_404(Lesson, pk=lesson_pk)

    student_skill = get_object_or_404(StudentSkill, id=student_skill)

    student_skill.validate()

    return HttpResponseRedirect(reverse('professor:lesson_student_detail', args=(lesson.pk, student_skill.student.id,)) + "#skills")


@require_POST
@user_is_professor
def unvalidate_student_skill(request, lesson_pk, student_skill):
    # TODO: a professor can only do this on one of his students
    lesson = get_object_or_404(Lesson, pk=lesson_pk)

    student_skill = get_object_or_404(StudentSkill, id=student_skill)

    student_skill.unvalidate()

    return HttpResponseRedirect(reverse('professor:lesson_student_detail', args=(lesson.pk, student_skill.student.id,)) + "#skills")


@require_POST
@user_is_professor
def default_student_skill(request, lesson_pk, student_skill):
    # TODO: a professor can only do this on one of his students
    lesson = get_object_or_404(Lesson, pk=lesson_pk)

    student_skill = get_object_or_404(StudentSkill, id=student_skill)

    student_skill.default()

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


@user_is_professor
def exercice_list(request):
    return render(request, 'professor/exercice/list.haml', {
        "exercice_list": Exercice.objects.select_related('skill'),
        "skills_without_exercices": Skill.objects.filter(exercice__isnull=True),
    })


#@require_POST
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

    questions = {}
    for question in data["questions"]:
        if question["type"] == "text":
            questions[question["instructions"]] = {
                "type": question["type"],
                "answers": [x["text"] for x in question["answers"]],
            }

        else:
            questions[question["instructions"]] = {
                "type": question["type"],
                "answers": {x["text"]: x["correct"] for x in question["answers"]},
            }

    result = validate_exercice_yaml_structure(questions)

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
def exercice_validation_form_pull_request(request):
    data = json.load(request)
    html = data["html"]
    skill_code = data["skill_code"]

    if data.get("image"):
        image_extension, image = data["image"].split(",", 1)

        image_extension = image_extension.split("/")[1].split(";")[0]

    questions = CommentedMap()
    for question in data["questions"]:
        if question["type"] == "text":
            questions[question["instructions"]] = {
                "type": question["type"],
                "answers": [x["text"] for x in question["answers"]],
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

    existing_files = [x["name"] for x in requests.get("https://api.github.com/repos/psycojoker/oscar/contents/exercices/").json()]

    existing_branches = [x["name"] for x in requests.get("https://api.github.com/repos/oscardemo/oscar/branches").json()]

    for i in range(1, 100):
        base_name = ("%s_%.2d" % (skill_code, i)).upper()
        if base_name + ".yaml" not in existing_files and base_name not in existing_branches:
            break
    else:
        raise Exception()

    master_sha = [x["object"]["sha"] for x in requests.get("https://api.github.com/repos/oscardemo/oscar/git/refs/heads").json() if x["ref"] == "refs/heads/master"][0]

    requests.post("https://api.github.com/repos/oscardemo/oscar/git/refs", data=json.dumps({
            "ref": "refs/heads/%s" % base_name,
            "sha": master_sha
        }),
        auth=HTTPBasicAuth(settings.OSCAR_GITHUB_LOGIN, settings.OSCAR_GITHUB_PASSWORD))

    requests.put("https://api.github.com/repos/oscardemo/oscar/contents/exercices/%s.yaml" % base_name, data=json.dumps({
        "message": "yaml for new exercice for %s" % skill_code,
        "content": b64encode(yaml_file),
        "branch": base_name}),
        auth=HTTPBasicAuth(settings.OSCAR_GITHUB_LOGIN, settings.OSCAR_GITHUB_PASSWORD))

    if image:
        if html:
            html = ('<img src="/static/exercices/%s.%s" />\n' % (base_name, image_extension)) + html
        else:
            html = '<img src="/static/exercices/%s.%s" />\n' % (base_name, image_extension)

        requests.put("https://api.github.com/repos/oscardemo/oscar/contents/exercices/%s.%s" % (base_name, image_extension), data=json.dumps({
            "message": "image for new exercice for %s" % skill_code,
            "content": image,
            "branch": base_name}),
            auth=HTTPBasicAuth(settings.OSCAR_GITHUB_LOGIN, settings.OSCAR_GITHUB_PASSWORD))

    if html:
        requests.put("https://api.github.com/repos/oscardemo/oscar/contents/exercices/%s.html" % base_name, data=json.dumps({
            "message": "html for new exercice for %s" % skill_code,
            "content": b64encode(html.encode("Utf-8")),
            "branch": base_name}),
            auth=HTTPBasicAuth(settings.OSCAR_GITHUB_LOGIN, settings.OSCAR_GITHUB_PASSWORD))

    answer = requests.post("https://api.github.com/repos/psycojoker/oscar/pulls", data=json.dumps({
        "title": "New exercice for %s by %s" % (skill_code, request.user.username),
        "head": "oscardemo:%s" % base_name,
        "base": "master",
    }),
            auth=HTTPBasicAuth(settings.OSCAR_GITHUB_LOGIN, settings.OSCAR_GITHUB_PASSWORD)).json()

    return HttpResponse(answer["html_url"])


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


@require_POST
@user_is_professor
def exercice_validation_form_pull_request_yaml(request):
    content = json.load(request)
    yaml = content["yaml"]
    html = content["html"]
    skill_code = content["skill_code"]

    existing_files = [x["name"] for x in requests.get("https://api.github.com/repos/psycojoker/oscar/contents/exercices/").json()]

    existing_branches = [x["name"] for x in requests.get("https://api.github.com/repos/oscardemo/oscar/branches").json()]

    for i in range(1, 100):
        base_name = ("%s_%.2d" % (skill_code, i)).upper()
        if base_name + ".yaml" not in existing_files and base_name not in existing_branches:
            break
    else:
        raise Exception()

    master_sha = [x["object"]["sha"] for x in requests.get("https://api.github.com/repos/oscardemo/oscar/git/refs/heads").json() if x["ref"] == "refs/heads/master"][0]

    requests.post("https://api.github.com/repos/oscardemo/oscar/git/refs", data=json.dumps({
            "ref": "refs/heads/%s" % base_name,
            "sha": master_sha
        }),
        auth=HTTPBasicAuth(settings.OSCAR_GITHUB_LOGIN, settings.OSCAR_GITHUB_PASSWORD))

    requests.put("https://api.github.com/repos/oscardemo/oscar/contents/exercices/%s.yaml" % base_name, data=json.dumps({
        "message": "yaml for new exercice for %s" % skill_code,
        "content": b64encode(yaml.encode("Utf-8")),
        "branch": base_name}),
        auth=HTTPBasicAuth(settings.OSCAR_GITHUB_LOGIN, settings.OSCAR_GITHUB_PASSWORD))

    if html:
        requests.put("https://api.github.com/repos/oscardemo/oscar/contents/exercices/%s.html" % base_name, data=json.dumps({
            "message": "html for new exercice for %s" % skill_code,
            "content": b64encode(html.encode("Utf-8")),
            "branch": base_name}),
            auth=HTTPBasicAuth(settings.OSCAR_GITHUB_LOGIN, settings.OSCAR_GITHUB_PASSWORD))

    answer = requests.post("https://api.github.com/repos/psycojoker/oscar/pulls", data=json.dumps({
        "title": "New exercice for %s by %s" % (skill_code, request.user.username),
        "head": "oscardemo:%s" % base_name,
        "base": "master",
    }),
            auth=HTTPBasicAuth(settings.OSCAR_GITHUB_LOGIN, settings.OSCAR_GITHUB_PASSWORD)).json()

    return HttpResponse(answer["html_url"])


@user_is_professor
def contribute_page(request):
    stages = {x.short_name: x for x in Stage.objects.all()}

    return render(request, "professor/skill/list.haml", stages)
