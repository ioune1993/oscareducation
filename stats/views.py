from django.shortcuts import render

from .utils import user_is_superuser

from promotions.models import Professor, Student, Lesson

@user_is_superuser
def dashboard(request):
    return render(request, "stats/dashboard.haml", {
        "professors": Professor.objects.all(),
        "students": Student.objects.all(),
        "lessons": Lesson.objects.all(),
    })
