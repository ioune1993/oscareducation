import json

from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.db import transaction
from django.db.models import Count

from skills.models import Skill, StudentSkill
from examinations.models import Test, TestStudent, Exercice

from .models import Lesson, Student
from .forms import LessonForm, StudentAddForm, VideoSkillForm, ExternalLinkSkillForm, ExerciceSkillForm, SyntheseForm, KhanAcademyVideoSkillForm, StudentUpdateForm, LessonUpdateForm, TestUpdateForm
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

    number_of_students = Lesson.objects.first().students.count()

    skill_to_student_skill = {}
    for student_skill in StudentSkill.objects.filter(student__lesson=lesson).select_related("skill"):
        skill_to_student_skill.setdefault(student_skill.skill, list()).append(student_skill)

    skills = []
    for stage in lesson.stages_in_unchronological_order():
        skills.extend([x for x in stage.skills.all().order_by('-code')])

    if lesson.students.count():
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
                skill.heatmap_class = "mastered_25"
            elif percentage < 0.5:
                skill.heatmap_class = "mastered_50"
            elif percentage < 0.75:
                skill.heatmap_class = "mastered_75"
            else:
                skill.heatmap_class = "mastered_100"


    return render(request, "professor/lesson/detail.haml", {
        "lesson": lesson,
        "number_of_students": number_of_students,
        "skills": skills,
    })


@user_is_professor
def lesson_add(request):
    form = LessonForm(request.POST) if request.method == "POST" else LessonForm()

    if form.is_valid():
        lesson = form.save()
        lesson.professors.add(request.user.professor)
        return HttpResponseRedirect(reverse("professor:dashboard"))

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
    form = StudentAddForm(request.POST) if request.method == "POST" else StudentAddForm()

    lesson = get_object_or_404(Lesson, pk=pk)

    # TODO: a professor can only see one of his lesson

    if form.is_valid():
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        username = form.generate_student_username()
        email = form.generate_email(username)

        user = User.objects.create_user(username=username,
                                        email=email,
                                        password=generate_random_password(15),
                                        first_name=first_name,
                                        last_name=last_name)

        student = Student.objects.create(user=user)
        student.lesson_set.add(lesson)
        # TODO send email to student here if email doesn't end in @example.com

        with transaction.atomic():
            for stage in lesson.stages_in_unchronological_order():
                for skill in stage.skills.all():
                    StudentSkill.objects.create(
                        student=student,
                        skill=skill,
                    )

        return HttpResponseRedirect(reverse("professor:lesson_detail", args=(lesson.pk,)))

    return render(request, "professor/lesson/student/add.haml", {
        "lesson": lesson,
        "add_student_form": form,
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
        return HttpResponseRedirect(reverse("professor:lesson_student_update", args=(lesson.pk, pk)))

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
        "tests": lesson.test_set.order_by('-created_at'),
    })


@user_is_professor
def lesson_test_add(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    return render(request, "professor/lesson/test/add.haml", {
        "lesson": lesson,
        "stages": lesson.stages_in_unchronological_order(),
    })


@user_is_professor
def lesson_test_update(request, lesson_pk, pk):
    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    test = get_object_or_404(Test, pk=pk)

    form = TestUpdateForm(request.POST, instance=test) if request.method == "POST" else TestUpdateForm(instance=test)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("professor:lesson_test_detail", args=(lesson.pk, test.pk,)))

    return render(request, "professor/lesson/test/update.haml", {
        "lesson": lesson,
        "test": test,
        "form": form,
    })


@user_is_professor
@require_POST
def lesson_test_close_open(request, lesson_pk, pk):
    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    test = get_object_or_404(Test, pk=pk)

    test.running = not test.running
    test.save()

    return HttpResponseRedirect(reverse("professor:lesson_test_list", args=(lesson.pk,)))


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

    if request.method == "GET":
        return render(request, "professor/skill/update_pedagogical_resources.haml", {
            "video_skill_form": VideoSkillForm(),
            "khanacademy_skill_form": KhanAcademyVideoSkillForm(),
            "exercice_skill_form": ExerciceSkillForm(),
            "external_link_skill_form": ExternalLinkSkillForm(),
            "synthese_form": SyntheseForm(),
            "object": skill,
        })

    assert request.method == "POST"

    print request.POST

    if request.POST["form_type"] == "video_skill":
        form = VideoSkillForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('professor:skill_update_pedagogical_ressources', args=(skill.code,)))

        return render(request, "professor/skill/update_pedagogical_resources.haml", {
            "video_skill_form": form,
            "khanacademy_skill_form": KhanAcademyVideoSkillForm(),
            "exercice_skill_form": ExerciceSkillForm(),
            "external_link_skill_form": ExternalLinkSkillForm(),
            "synthese_form": SyntheseForm(),
            "object": skill,
        })

    elif request.POST["form_type"] == "khanacademy_skill":
        form = KhanAcademyVideoSkillForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('professor:skill_update_pedagogical_ressources', args=(skill.code,)))

        return render(request, "professor/skill/update_pedagogical_resources.haml", {
            "video_skill_form": VideoSkillForm(),
            "khanacademy_skill_form": form,
            "exercice_skill_form": ExerciceSkillForm(),
            "external_link_skill_form": ExternalLinkSkillForm(),
            "synthese_form": SyntheseForm(),
            "object": skill,
        })

    elif request.POST["form_type"] == "exercice_skill":
        form = ExerciceSkillForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('professor:skill_update_pedagogical_ressources', args=(skill.code,)))

        return render(request, "professor/skill/update_pedagogical_resources.haml", {
            "video_skill_form": VideoSkillForm(),
            "khanacademy_skill_form": KhanAcademyVideoSkillForm(),
            "exercice_skill_form": form,
            "external_link_skill_form": ExternalLinkSkillForm(),
            "synthese_form": SyntheseForm(),
            "object": skill,
        })

    elif request.POST["form_type"] == "external_link_skill":
        form = ExternalLinkSkillForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('professor:skill_update_pedagogical_ressources', args=(skill.code,)))

        return render(request, "professor/skill/update_pedagogical_resources.haml", {
            "video_skill_form": VideoSkillForm(),
            "khanacademy_skill_form": KhanAcademyVideoSkillForm(),
            "exercice_skill_form": ExerciceSkillForm(),
            "external_link_skill_form": form,
            "synthese_form": SyntheseForm(),
            "object": skill,
        })
    elif request.POST["form_type"] == "synthese_form":
        form = SyntheseForm(request.POST)
        if form.is_valid():
            skill.oscar_synthese = form.cleaned_data["synthese"]
            skill.save()
            return HttpResponseRedirect(reverse('professor:skill_update_pedagogical_ressources', args=(skill.code,)))

        return render(request, "professor/skill/update_pedagogical_resources.haml", {
            "video_skill_form": VideoSkillForm(),
            "khanacademy_skill_form": KhanAcademyVideoSkillForm(),
            "exercice_skill_form": ExerciceSkillForm(),
            "external_link_skill_form": ExternalLinkSkillForm(),
            "synthese_form": form,
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
            TestStudent.objects.create(
                test=test,
                student=student,
            )

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
