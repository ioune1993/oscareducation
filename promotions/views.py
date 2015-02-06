import json

from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.db import transaction
from django.db.models import Count

from skills.models import Skill, StudentSkill
from examinations.models import Test, TestStudent

from .models import Lesson, Student
from .forms import LessonForm, StudentForm
from .utils import generate_random_password, user_is_professor


@user_is_professor
def dashboard(request):
    form = LessonForm(request.POST) if request.method == "POST" else LessonForm()

    if form.is_valid():
        lesson = form.save()
        lesson.professors.add(request.user.professor)
        return HttpResponseRedirect(reverse("professor_dashboard"))

    return render(request, "professor/dashboard.haml", {
        "lessons": Lesson.objects.filter(professors=request.user.professor),
        "add_lesson_form": form,
    })


@user_is_professor
def lesson_detail_view(request, pk):
    form = StudentForm(request.POST) if request.method == "POST" else StudentForm()

    lesson = get_object_or_404(Lesson, pk=pk)

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

        for skill in Skill.objects.all():
            StudentSkill.objects.create(
                student=student,
                skill=skill,
            )

        return HttpResponseRedirect(reverse("professor_lesson_detail_view", args=(lesson.pk,)))

    return render(request, "professor/lesson_detail_view.haml", {
        "lesson": lesson,
        "add_student_form": form,
    })


@user_is_professor
def student_detail_view(request, pk):
    student = get_object_or_404(Student, pk=pk)

    return render(request, "professor/student_detail_view.haml", {
        "student": student,
    })


@require_POST
@user_is_professor
def regenerate_student_password(request):
    data = json.load(request)

    student = get_object_or_404(Student, id=data["student_id"])
    new_password = generate_random_password(8)

    # TODO: a professor can only modify this for one of his students

    student.user.set_password(new_password)
    student.user.save()

    return HttpResponse(new_password)


@require_POST
@user_is_professor
def validate_student_skill(request, student_skill):
    def recursivly_validate_student_skills(student_skill):
        student_skill.acquired = datetime.now()
        student_skill.save()

        for sub_student_skill in StudentSkill.objects.filter(skill__in=student_skill.skill.depends_on.all()):
            recursivly_validate_student_skills(sub_student_skill)

    student_skill = get_object_or_404(StudentSkill, id=student_skill)

    recursivly_validate_student_skills(student_skill)

    return HttpResponseRedirect(reverse('professor_student_detail_view', args=(student_skill.student.id,)) + "#skills")


@require_POST
@user_is_professor
def unvalidate_student_skill(request, student_skill):
    def recursivly_unalidate_student_skills(student_skill):
        student_skill.acquired = None
        student_skill.tested = datetime.now()
        student_skill.save()

        for sub_student_skill in StudentSkill.objects.filter(skill__in=student_skill.skill.skill_set.all()):
            recursivly_unalidate_student_skills(sub_student_skill)

    student_skill = get_object_or_404(StudentSkill, id=student_skill)

    recursivly_unalidate_student_skills(student_skill)

    student_skill.save()

    return HttpResponseRedirect(reverse('professor_student_detail_view', args=(student_skill.student.id,)) + "#skills")


@require_POST
@user_is_professor
def default_student_skill(request, student_skill):
    student_skill = get_object_or_404(StudentSkill, id=student_skill)

    student_skill.acquired = None
    student_skill.tested = None
    student_skill.save()

    return HttpResponseRedirect(reverse('professor_student_detail_view', args=(student_skill.student.id,)) + "#skills")


@user_is_professor
def lesson_tests_and_skills(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.user.professor not in lesson.professors.all():
        raise PermissionDenied()

    return HttpResponse(json.dumps({
        "tests": [{"name": x.name, "skills": list(x.skills.all().values("code"))} for x in lesson.test_set.all()],
        "skills": [x for x in Skill.objects.annotate(num_depends=Count('depends_on')).filter(num_depends__gt=0).values("id", "code", "name")],
    }, indent=4))


@require_POST
@user_is_professor
def add_test_for_lesson(request):
    data = json.load(request)

    lesson = get_object_or_404(Lesson, id=data["lesson"])

    if request.user.professor not in lesson.professors.all():
        raise PermissionDenied()

    with transaction.atomic():
        test = Test.objects.create(
            lesson=lesson,
            name=data["name"],
        )

        for skill_id in data["skills"]:
            test.skills.add(Skill.objects.get(code=skill_id))

        for student in lesson.students.all():
            TestStudent.objects.create(
                test=test,
                student=student,
            )

        test.save()

    return HttpResponse("ok")
