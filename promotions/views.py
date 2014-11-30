from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


from .models import Lesson
from .forms import LessonForm


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
    return render(request, "professor/lesson_detail_view.haml", {
        "lesson": get_object_or_404(Lesson, pk=pk)
    })
