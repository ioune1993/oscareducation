from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


from .models import Lesson, Student
from .forms import LessonForm, StudentForm


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


def lesson_detail_view(request, pk):
    form = StudentForm(request.POST) if request.method == "POST" else StudentForm()

    lesson = get_object_or_404(Lesson, pk=pk)

    if form.is_valid():
        user = User()
        user.first_name = form.cleaned_data["first_name"]
        user.last_name = form.cleaned_data["last_name"]
        user.username = form.generate_student_username()
        user.email = form.generate_email(user.username)
        user.save()

        student = Student.objects.create(user=user)
        student.lesson_set.add(lesson)

        return HttpResponseRedirect(reverse("professor_lesson_detail_view", args=(lesson.pk,)))

    return render(request, "professor/lesson_detail_view.haml", {
        "lesson": lesson,
        "add_student_form": form,
    })
