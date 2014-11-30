from django.shortcuts import render

from .models import Lesson


def dashboard(request):
    return render(request, "professor/dashboard.haml", {
        "lessons": Lesson.objects.filter(professors=request.user.professor)
    })
