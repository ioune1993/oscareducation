from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from skills.models import Skill

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
        "skills": Skill.objects.order_by('-level', '-code'),
    })
